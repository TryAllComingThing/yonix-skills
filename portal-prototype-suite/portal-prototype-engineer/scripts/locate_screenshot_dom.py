"""Map a screenshot region in viewport coordinates to DOM candidates.
Candidate ranking only; never automatically edit without human confirmation.
"""
import argparse,asyncio,json,sys
from pathlib import Path
from common import emit
p=argparse.ArgumentParser()
p.add_argument('--html',required=True);p.add_argument('--region',required=True,help='JSON {x,y,width,height} in viewport pixels');p.add_argument('--setup-js');p.add_argument('--output');p.add_argument('--screenshot');p.add_argument('--executable-path',default='/usr/bin/chromium');a=p.parse_args()
try:from playwright.async_api import async_playwright
except ImportError:sys.exit('NOT_RUN: playwright unavailable')
async def run():
 async with async_playwright() as pw:
  b=await pw.chromium.launch(executable_path=a.executable_path,args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':1440,'height':900});await page.set_content(Path(a.html).read_text(),wait_until='domcontentloaded')
  if a.setup_js:await page.evaluate(a.setup_js)
  if a.screenshot:await page.screenshot(path=a.screenshot)
  data=await page.evaluate('''(region)=>{
   const x=region.x,y=region.y,w=region.width,h=region.height;
   const all=[...document.querySelectorAll('body *')];const out=[];
   for(const el of all){const r=el.getBoundingClientRect();if(r.width<4||r.height<4)continue;
    const ix=Math.max(0,Math.min(x+w,r.right)-Math.max(x,r.left)),iy=Math.max(0,Math.min(y+h,r.bottom)-Math.max(y,r.top));if(!ix||!iy)continue;
    const inter=ix*iy,area=r.width*r.height,roi=w*h,cover=inter/roi,purity=inter/area;
    if(cover<.10)continue;
    const style=getComputedStyle(el);if(style.visibility==='hidden'||style.display==='none')continue;
    let path=el.tagName.toLowerCase();if(el.id)path+='#'+CSS.escape(el.id);else if(el.classList.length)path+='.'+[...el.classList].slice(0,2).map(x=>CSS.escape(x)).join('.');
    const text=(el.innerText||'').replace(/\\s+/g,' ').slice(0,110);
    out.push({selector:path,text,rect:{x:r.x,y:r.y,width:r.width,height:r.height},cover:+cover.toFixed(3),purity:+purity.toFixed(3),score:+(cover*.25+purity*.75).toFixed(3)});
   }
   return out.sort((a,b)=>b.score-a.score).slice(0,25)
  }''',json.loads(a.region))
  await b.close()
 emit({'status':'CANDIDATES_ONLY' if data else 'NOT_LOCATED','region':json.loads(a.region),'candidates':data,'requires_confirmation':True,'note':'Bounding-box localization; red pixels in annotated screenshot are not automatically segmented; screenshot must use same viewport and scroll position'},a.output)
 return bool(data)
if __name__=='__main__':sys.exit(0 if asyncio.run(run()) else 1)
