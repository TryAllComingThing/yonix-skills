"""Browser matrix: page x theme, selector assertions, errors, screenshots, optional pixel baselines.
Fail closed on missing routes/themes/selectors and missing baseline when required.
"""
import argparse,asyncio,json,sys
from pathlib import Path
from PIL import Image,ImageChops
from playwright.async_api import async_playwright
p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--output-dir',required=True);p.add_argument('--executable-path',default='/usr/bin/chromium');a=p.parse_args()
contract=json.loads(Path(a.contract).read_text());out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
async def run():
 rows=[]
 async with async_playwright() as pw:
  b=await pw.chromium.launch(executable_path=a.executable_path,args=['--no-sandbox'])
  page=await b.new_page(viewport=contract.get('viewport',{'width':1440,'height':900}),device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  
  if contract.get('html'):
   await page.set_content(Path(contract['html']).read_text(),wait_until='domcontentloaded')
  else:await page.goto(contract['url'],wait_until='domcontentloaded')
  if contract.get('setup_js'):await page.evaluate(contract['setup_js'])
  for route in contract['pages']:
   for theme in contract['themes']:
    errors.clear()
    await page.evaluate("""({route,theme,routeJs,themeJs})=>{(new Function('route',routeJs))(route);(new Function('theme',themeJs))(theme)}""",{'route':route,'theme':theme,'routeJs':contract['route_js'],'themeJs':contract['theme_js']})
    await page.wait_for_timeout(contract.get('settle_ms',120))
    assertions=[]
    for selector in contract.get('required_selectors',[]):
     found=await page.locator(selector).count();visible=bool(found and await page.locator(selector).first.is_visible())
     assertions.append({'selector':selector,'visible':visible})
    name=f'{route}__{theme}'.replace('/','_');shot=out/(name+'.png');await page.screenshot(path=str(shot),full_page=contract.get('full_page',False))
    diff=None;baseline=contract.get('baseline_dir')
    if baseline:
     ref=Path(baseline)/(name+'.png')
     if ref.exists():
      im1=Image.open(ref).convert('RGB');im2=Image.open(shot).convert('RGB')
      if im1.size==im2.size:
       d=ImageChops.difference(im1,im2);changed=sum(1 for pixel in d.getdata() if max(pixel)>contract.get('pixel_tolerance',0));diff={'changed_pixels':changed,'ratio':round(changed/(im1.width*im1.height),6),'baseline':str(ref)}
      else:diff={'error':'DIMENSION_MISMATCH'}
     else:diff={'error':'BASELINE_MISSING'}
    passed=not errors and all(v['visible'] for v in assertions) and (diff is None or ('ratio' in diff and diff['ratio']<=contract.get('max_diff_ratio',0)))
    rows.append({'page':route,'theme':theme,'status':'PASS' if passed else 'FAIL','assertions':assertions,'page_errors':list(errors),'screenshot':str(shot),'diff':diff})
  await b.close()
 report={'status':'PASS' if all(r['status']=='PASS' for r in rows) else 'FAIL','cases':len(rows),'passed':sum(r['status']=='PASS' for r in rows),'rows':rows,'note':'Visual pixel baselines optional; absent baseline means runtime-only checks, not visual regression.'}
 (out/'matrix.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({'status':report['status'],'cases':report['cases'],'passed':report['passed'],'report':str(out/'matrix.json')}))
 return report['status']=='PASS'
if __name__=='__main__':sys.exit(0 if asyncio.run(run()) else 1)
