"""Computed-style runtime theme checks with explicit selector/property contracts.
Checks variation, semantic color contrast and render errors. Not a pixel diff.
"""
import argparse,asyncio,json,sys
from pathlib import Path
from common import emit
p=argparse.ArgumentParser()
p.add_argument('--html',required=True);p.add_argument('--contract',required=True);p.add_argument('--output');p.add_argument('--screenshots');p.add_argument('--executable-path',default='/usr/bin/chromium')
a=p.parse_args()
try:from playwright.async_api import async_playwright
except ImportError:sys.exit('NOT_RUN: playwright unavailable')
contract=json.loads(Path(a.contract).read_text());themes=contract['themes'];selectors=contract['selectors']
async def run():
 rows=[];errors=[]
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path=a.executable_path,args=['--no-sandbox'])
  page=await browser.new_page(viewport=contract.get('viewport',{'width':1440,'height':900}))
  page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content(Path(a.html).read_text(),wait_until='domcontentloaded')
  if contract.get('setup_js'):await page.evaluate(contract['setup_js'])
  for theme in themes:
   if contract.get('theme_js'):
    await page.evaluate('([code,theme])=>{(new Function("theme",code))(theme)}',[contract['theme_js'],theme])
   else:await page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
   await page.evaluate('()=>document.fonts.ready')
   for item in selectors:
    row=await page.evaluate('''(c)=>{const e=document.querySelector(c.selector);if(!e)return {exists:false};const r=e.getBoundingClientRect(),s=getComputedStyle(e);const style={};for(const p of c.properties)style[p]=s.getPropertyValue(p).trim();return {exists:true,visible:r.width>0&&r.height>0,width:r.width,height:r.height,style}}''',item)
    rows.append({'theme':theme,'selector':item['selector'],**row})
   if a.screenshots:
    Path(a.screenshots).mkdir(parents=True,exist_ok=True)
    await page.screenshot(path=str(Path(a.screenshots)/(theme+'.png')))
  await browser.close()
 failures=[]
 for item in selectors:
  rs=[r for r in rows if r['selector']==item['selector']]
  if any(not r.get('exists') or not r.get('visible') for r in rs):failures.append({'selector':item['selector'],'reason':'missing_or_invisible'});continue
  for prop in item.get('must_vary',[]):
   if len(set(r['style'][prop] for r in rs))<2:failures.append({'selector':item['selector'],'property':prop,'reason':'theme_invariant'})
  for theme,expected in item.get('expected',{}).items():
   rr=next((r for r in rs if r['theme']==theme),None)
   for prop,value in expected.items():
    if rr is None or rr['style'].get(prop)!=value:failures.append({'selector':item['selector'],'theme':theme,'property':prop,'expected':value,'actual':rr['style'].get(prop) if rr else None})
  if item.get('contrast_min'):
   for r in rs:
    ratio=contrast(r['style'].get('color',''),r['style'].get('background-color',''))
    r['contrast_ratio']=ratio
    if ratio is None or ratio<item['contrast_min']:failures.append({'selector':item['selector'],'theme':r['theme'],'reason':'contrast_below_threshold_or_unresolved_background','ratio':ratio})
 report={'status':'PASS' if not failures and not errors else 'FAIL','themes':themes,'measurements':rows,'failures':failures,'page_errors':errors,'note':'Only declared selectors/states were checked; transparent backgrounds require explicit effective background in contract'}
 emit(report,a.output)
 return not failures and not errors

def contrast(fg,bg):
 import re
 def parse(v):
  if v=='transparent':return None
  m=re.fullmatch(r'rgba?\(([^)]*)\)',v)
  if not m:return None
  nums=[float(x.strip()) for x in m.group(1).split(',')]
  if len(nums)>3 and nums[3]<1:return None
  return [n/255 for n in nums[:3]]
 f=parse(fg);b=parse(bg)
 if f is None or b is None:return None
 def luminance(rgb):
  x=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
  return sum(v*w for v,w in zip(x,[.2126,.7152,.0722]))
 x,y=sorted([luminance(f),luminance(b)],reverse=True)
 return round((x+.05)/(y+.05),3)
if __name__=='__main__':sys.exit(0 if asyncio.run(run()) else 1)
