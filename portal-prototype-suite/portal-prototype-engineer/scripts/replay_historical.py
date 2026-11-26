"""Read-only historical version replay. Historical known-good comparisons != autonomous repair."""
import argparse,json,hashlib,sys,asyncio
from pathlib import Path
from common import emit
p=argparse.ArgumentParser(description='Compare historical defect signatures; optionally execute real browser probes')
p.add_argument('--cases',required=True);p.add_argument('--output');p.add_argument('--browser',action='store_true');p.add_argument('--executable-path',default='/usr/bin/chromium');a=p.parse_args()
manifest=json.loads(Path(a.cases).read_text());out=[]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def probe_source(case):
 bad=Path(case['bad']);good=Path(case['good']);r={'id':case['id'],'kind':case.get('kind','signature'),'bad':str(bad),'good':str(good)}
 if not bad.exists() or not good.exists():return {**r,'status':'NOT_TESTED','reason':'historical file unavailable'}
 b=bad.read_text(encoding='utf8');g=good.read_text(encoding='utf8')
 r.update(bad_sha256=digest(bad),good_sha256=digest(good),source_unchanged=(b==g))
 if case.get('kind')=='fork':
  r['status']='BLOCKED' if b!=g else 'NO_DIVERGENCE';r['reason']='Divergent historical branches require explicit merge; do not silently pick a newer filename';return r
 if case.get('kind')=='text_count':
  needle=case['needle'];bc=b.count(needle);gc=g.count(needle)
  r.update(needle=needle,bad_count=bc,good_count=gc,status='PATCH_REPLAY_SOURCE_CONFIRMED' if bc>gc else 'NOT_REPRODUCED',reason='Count reduction in historical source; not a visual localization test');return r
 if case.get('kind')=='css_inventory':
  import re
  n1=len(re.findall(r'!important\b',b));n2=len(re.findall(r'!important\b',g))
  r.update(bad_important=n1,good_important=n2,status='DETECTED' if n1 else 'NOT_REPRODUCED',reason='CSS override inventory only, not evidence of redundant rules');return r
 old=case.get('bad_absent');new=case.get('good_present')
 if old and old in b:r['status']='NOT_REPRODUCED';r['reason']='expected absent marker already in bad baseline';return r
 if new and new not in g:r['status']='NOT_REPRODUCED';r['reason']='expected known-good marker missing';return r
 if b==g:r['status']='NOT_REPRODUCED';r['reason']='files identical';return r
 r['status']='PATCH_REPLAY_SOURCE_CONFIRMED';r['reason']='Historical fix signature differs as expected; browser validation separate; no autonomous repair performed';return r
async def browser_probes(cases,results):
 try:from playwright.async_api import async_playwright
 except ImportError:
  for r in results:r['browser']='NOT_TESTED: Playwright missing'
  return
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path=a.executable_path,args=['--no-sandbox'])
  for c,r in zip(cases,results):
   if c.get('kind') not in ('api_layout','api_code','dialog') or r['status']!='PATCH_REPLAY_SOURCE_CONFIRMED':continue
   measurements={}
   for role in ('bad','good'):
    page=await browser.new_page(viewport={'width':1440,'height':900})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    try:
     await page.set_content(Path(c[role]).read_text(encoding='utf8'),wait_until='domcontentloaded',timeout=45000)
     try:await page.get_by_text('登 录',exact=True).first.click(timeout=2500)
     except Exception:pass
     await page.evaluate("""()=>{if(typeof S!=='undefined'&&typeof render==='function'){S.page='POR-11';S.lang='zh';S.theme='steady-blue';render();if(typeof m369OpenDoc==='function')m369OpenDoc('chat','svc-chat');}}""")
     if c['kind']=='api_layout':
      measurements[role]=await page.evaluate("""()=>{const e=document.querySelector('.m369-doc-body');const x=document.querySelector('.m369-doc-shell');return {body_width:e?.getBoundingClientRect().width||0,shell_width:x?.getBoundingClientRect().width||0,grid:x?getComputedStyle(x).gridTemplateColumns:null,visible:!!e&&e.getBoundingClientRect().height>0}}""")
     elif c['kind']=='api_code':
      measurements[role]=await page.evaluate("""()=>{const e=document.querySelector('.m369-doc-body pre');const s=e?getComputedStyle(e):null;return {exists:!!e,background:s?.backgroundColor||null,color:s?.color||null}}""")
     else:
      await page.evaluate("""()=>{S.page='POR-04';S.modal='password';render()}""")
      measurements[role]=await page.evaluate("""()=>{const e=document.querySelector('.modal .modal-head > button.btn,.m319-modal .m319-modal-close,.m339-close,.m340-close');const r=e?.getBoundingClientRect(),s=e?getComputedStyle(e):null;return {rules:!!document.getElementById('m364-dialog-actions'),button:!!e,width:r?.width,height:r?.height,font:s?.fontSize,border:s?.borderWidth}}""")
     measurements[role]['page_errors']=errors
    except Exception as ex:measurements[role]={'error':str(ex)}
    finally:await page.close()
   r['browser_measurements']=measurements
   if c['kind']=='api_layout':
    b=measurements['bad'].get('body_width',0);g=measurements['good'].get('body_width',0)
    r['browser']='PASS' if g>600 and g>b*1.5 else 'FAIL_OR_NOT_REPRODUCED'
   elif c['kind']=='api_code':r['browser']='PASS' if measurements['good'].get('background')=='rgb(17, 24, 39)' and measurements['bad'].get('background')!='rgb(17, 24, 39)' else 'FAIL_OR_NOT_REPRODUCED'
   else:r['browser']='PASS' if measurements['good'].get('button') and abs(measurements['good'].get('width',0)-32)<1 and abs(measurements['good'].get('height',0)-32)<1 and measurements['good'].get('font')=='18px' else 'FAIL_OR_NOT_REPRODUCED'
  await browser.close()
for c in manifest['cases']:out.append(probe_source(c))
if a.browser:asyncio.run(browser_probes(manifest['cases'],out))
report={'suite':'Prototype Engineering Expert V1.1','method':'historical version fingerprint and known-good regression signature; NOT autonomous repair','cases':out,'counts':{k:sum(r['status']==k for r in out) for k in sorted(set(r['status'] for r in out))},'autonomous_repair_verified':False,'limitations':['Historical fixes are supplied; detection and replay do not demonstrate autonomous source patching','Source marker alone does not prove browser behavior','Visual screenshot-to-DOM localization and multi-theme full regression not exercised by this runner']}
emit(report,a.output)
if any(r['status'] in ('NOT_REPRODUCED','NOT_TESTED') or r.get('browser')=='FAIL_OR_NOT_REPRODUCED' for r in out):sys.exit(1)
