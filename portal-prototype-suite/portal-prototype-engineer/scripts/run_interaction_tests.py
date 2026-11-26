"""Playwright scenario runner with actual assertions and screenshots."""
import argparse,asyncio,json,sys
from pathlib import Path
from common import emit
p=argparse.ArgumentParser(description='Run browser interaction scenarios from JSON')
p.add_argument('--url',help='http(s) URL');p.add_argument('--html',help='Local HTML to load with set_content, for offline test fixtures');p.add_argument('--scenario',required=True);p.add_argument('--output');p.add_argument('--screenshots',default='screenshots');p.add_argument('--browser',choices=['chromium','firefox','webkit'],default='chromium');p.add_argument('--executable-path',help='Optional browser executable path');a=p.parse_args()
try:from playwright.async_api import async_playwright
except ImportError:sys.exit('NOT_RUN: pip install playwright && python -m playwright install chromium')
if not a.url and not a.html:p.error('provide --url or --html')
sc=json.loads(Path(a.scenario).read_text(encoding='utf-8'));Path(a.screenshots).mkdir(parents=True,exist_ok=True)
async def run():
 results=[];errors=[]
 async with async_playwright() as pw:
  browser=await getattr(pw,a.browser).launch(headless=True,**({'executable_path':a.executable_path} if a.executable_path else {}),args=['--no-sandbox'] if a.browser=='chromium' else [])
  page=await browser.new_page(viewport=sc.get('viewport',{'width':1440,'height':900}))
  page.on('pageerror',lambda e:errors.append(str(e)))
  try:
   if a.html:await page.set_content(Path(a.html).read_text(encoding='utf-8'),wait_until='domcontentloaded',timeout=30000)
   else:await page.goto(a.url,wait_until='domcontentloaded',timeout=30000)
   for i,step in enumerate(sc['steps']):
    try:
     op=step['action'];loc=page.locator(step['selector']) if 'selector' in step else None
     if op=='click':await loc.click()
     elif op=='fill':await loc.fill(step['value'])
     elif op=='visible':assert await loc.is_visible(),f'not visible: {step["selector"]}'
     elif op=='hidden':assert await loc.count()==0 or not await loc.is_visible(),f'not hidden: {step["selector"]}'
     elif op=='text':assert step['value'] in await loc.inner_text(),f'text missing: {step["value"]}'
     elif op=='url':assert step['value'] in page.url,f'URL mismatch: {page.url}'
     elif op=='screenshot':await page.screenshot(path=str(Path(a.screenshots)/(step.get('name',str(i))+'.png')),full_page=True)
     elif op=='press':await loc.press(step['value'])
     else:raise ValueError('unknown action: '+op)
     results.append({'step':i,'action':op,'status':'PASS'})
    except Exception as e:results.append({'step':i,'action':step.get('action'),'status':'FAIL','error':str(e)});break
  except Exception as e:results.append({'step':'navigation','status':'FAIL','error':str(e)})
  await browser.close()
 status='PASS' if results and all(x['status']=='PASS' for x in results) and not errors else 'FAIL'
 emit({'status':status,'url':a.url,'html':a.html,'steps':results,'page_errors':errors,'scenario':a.scenario},a.output)
 return status=='PASS'
sys.exit(0 if asyncio.run(run()) else 1)
