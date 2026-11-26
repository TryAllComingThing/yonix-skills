"""Read-only Vue DOM owner tracing via Vue runtime dev metadata + optional source index.
Production/minified Vue may not expose owner or file path; fail closed.
"""
import argparse,asyncio,json,sys,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--url');p.add_argument('--html');p.add_argument('--selector',required=True);p.add_argument('--project');p.add_argument('--setup-js');p.add_argument('--output');p.add_argument('--executable-path',default='/usr/bin/chromium');a=p.parse_args()
from playwright.async_api import async_playwright
async def run():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path=a.executable_path,args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':900})
  
  if a.html:await page.set_content(Path(a.html).read_text(),wait_until='domcontentloaded')
  elif a.url:await page.goto(a.url,wait_until='domcontentloaded')
  else:raise ValueError('Provide --url or --html')
  if a.setup_js:await page.evaluate(a.setup_js)
  data=await page.evaluate("""sel=>{let el=document.querySelector(sel);if(!el)return {status:'ELEMENT_NOT_FOUND'};let chain=[],cursor=el;while(cursor&&!cursor.__vueParentComponent)cursor=cursor.parentElement;let c=cursor?.__vueParentComponent||null;let depth=0;while(c&&depth++<15){const t=c.type||{};chain.push({name:t.name||t.__name||null,file:t.__file||null,uid:c.uid});c=c.parent}return {status:chain.length?'RUNTIME_OWNER_FOUND':'RUNTIME_OWNER_UNAVAILABLE',tag:el.tagName,text:(el.textContent||'').trim().slice(0,160),chain}}""",a.selector)
  await browser.close()
 if a.project and data.get('chain'):
  base=Path(a.project).resolve();files={str(f.resolve()):f for f in base.rglob('*.vue') if 'node_modules' not in f.parts}
  for item in data['chain']:
   f=item.get('file');item['source_verified']=False
   if f:
    target=Path(f).resolve() if Path(f).is_absolute() else (base/f).resolve()
    if str(target) in files:item['source_verified']=True;item['source_path']=str(target)
    else:
     matches=[str(x) for x in files if x.endswith('/'+f.lstrip('/'))]
     if len(matches)==1:item['source_verified']=True;item['source_path']=matches[0]
  data['status']='SOURCE_TRACED' if data['chain'][0].get('source_verified') else 'SOURCE_UNVERIFIED'
 data['read_only']=True;data['note']='Vue dev runtime __file metadata is not guaranteed; a matched component file is not a precise template line mapping. Do not auto-patch dynamic SFC.'
 if a.output:Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(json.dumps(data,ensure_ascii=False))
 return data['status']=='SOURCE_TRACED'
if __name__=='__main__':sys.exit(0 if asyncio.run(run()) else 2)
