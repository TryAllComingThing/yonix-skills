"""M4 guarded screenshot-region -> DOM -> static-source -> candidate -> browser acceptance.
Supports only removal of unique, non-interactive static HTML leaf text or replacement
of a unique CSS declaration. Never modifies input. Does not use model hallucinations.
"""
import argparse, asyncio, hashlib, json, re, sys
from pathlib import Path
from html import unescape

parser=argparse.ArgumentParser()
parser.add_argument('--input',required=True)
parser.add_argument('--intent',required=True,choices=['remove-text','theme-color'])
parser.add_argument('--region',required=True,help='viewport screenshot rectangle JSON')
parser.add_argument('--target-text',help='exact visible text for remove-text')
parser.add_argument('--selector',help='unique selector for theme-color')
parser.add_argument('--property',default='background-color')
parser.add_argument('--replacement',help='CSS value for theme-color, must use var(--...)')
parser.add_argument('--allow-shared',action='store_true',help='explicitly permit shared selector modification; verify all matches')
parser.add_argument('--setup-js',help='read-only page state setup script; trusted local code only')
parser.add_argument('--output',required=True)
parser.add_argument('--evidence-dir',required=True)
parser.add_argument('--viewport-width',type=int,default=1440)
parser.add_argument('--viewport-height',type=int,default=900)
parser.add_argument('--executable-path',default='/usr/bin/chromium')
a=parser.parse_args()
source=Path(a.input).resolve();dest=Path(a.output).resolve();evidence=Path(a.evidence_dir)
if source==dest:parser.error('candidate cannot overwrite source')
if a.intent=='remove-text' and not a.target_text:parser.error('--target-text required')
if a.intent=='theme-color' and (not a.selector or not re.fullmatch(r'var\(--[\w-]+\)',a.replacement or '')):parser.error('theme repair requires --selector and --replacement var(--token)')
if a.viewport_width<320 or a.viewport_height<320:parser.error('invalid viewport')
try:from playwright.async_api import async_playwright
except ImportError:sys.exit('NOT_RUN: playwright unavailable')

def sha(s):return hashlib.sha256(s.encode()).hexdigest()

def static_edit(src,probe):
 if a.intent=='remove-text':
  # Restrict to simple leaf text nodes; don't remove controls or scripts/styles.
  from bs4 import BeautifulSoup, NavigableString
  soup=BeautifulSoup(src,'html.parser');matches=[]
  for node in soup.find_all(string=True):
   if not isinstance(node,NavigableString) or node.parent.name in ('script','style','title','noscript'):continue
   if str(node).strip()!=a.target_text:continue
   el=node.parent
   if el.name in ('button','a','input','label','select','option') or el.find(['button','a','input','select','textarea']):continue
   matches.append(el)
  if len(matches)!=1:return None,{'reason':'static text not unique or unsafe','static_matches':len(matches)}
  el=matches[0]
  # Exact source byte edit, no soup serialization. Require full leaf tag occurrence unique.
  fragment=str(el);count=src.count(fragment)
  if count!=1:return None,{'reason':'source fragment not unique','fragment_matches':count}
  if probe['text']!=a.target_text:return None,{'reason':'DOM text does not match source target'}
  if not (probe['tag']==el.name and (not el.get('id') or probe['id']==el.get('id'))):return None,{'reason':'DOM/source element mismatch'}
  return src.replace(fragment,'',1),{'operation':'remove static leaf element','source_fragment':fragment[:300]}
 # CSS only if exact selector and declaration unique, no override stacking.
 selector=re.escape(a.selector)
 rx=re.compile(r'(?P<head>(?:^|[{}\n])\s*'+selector+r'\s*\{)(?P<body>[^{}]*)(?P<tail>\})',re.M)
 rules=list(rx.finditer(src))
 if len(rules)!=1:return None,{'reason':'CSS rule not unique','rules':len(rules)}
 m=rules[0];prop=re.escape(a.property)
 drx=re.compile(r'(?P<pre>(?:^|;)\s*'+prop+r'\s*:\s*)(?P<value>[^;!}]+)(?P<important>\s*!important)?(?=\s*(?:;|$))',re.M)
 decl=list(drx.finditer(m.group('body')))
 if len(decl)!=1:return None,{'reason':'CSS declaration not unique','declarations':len(decl)}
 d=decl[0];old=d.group('value').strip()
 if old==a.replacement:return None,{'reason':'already correct'}
 changed=m.group('body')[:d.start('value')]+a.replacement+m.group('body')[d.end('value'):]
 return src[:m.start('body')]+changed+src[m.end('body'):],{'operation':'replace declaration in source rule','selector':a.selector,'property':a.property,'before':old,'after':a.replacement}

async def main():
 evidence.mkdir(parents=True,exist_ok=True)
 try:roi=json.loads(a.region)
 except Exception as e:raise ValueError('invalid region JSON') from e
 if not all(isinstance(roi.get(k),(int,float)) and roi[k]>=0 for k in ('x','y','width','height')) or roi['width']<4 or roi['height']<4:raise ValueError('invalid rectangle')
 original=source.read_text();errors=[];result={'status':'BLOCKED','intent':a.intent,'source':str(source),'source_sha256':sha(original),'region':roi,'candidate':str(dest),'stages':{}}
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path=a.executable_path,args=['--no-sandbox'])
  async def open_page(html):
   page=await browser.new_page(viewport={'width':a.viewport_width,'height':a.viewport_height},device_scale_factor=1)
   page.on('pageerror',lambda e:errors.append(str(e)))
   await page.set_content(html,wait_until='domcontentloaded')
   if a.setup_js:await page.evaluate(a.setup_js)
   return page
  before=await open_page(original)
  await before.screenshot(path=str(evidence/'before.png'),animations='disabled')
  probe=await before.evaluate('''({roi,selector,intent})=>{
   const el=document.elementFromPoint(roi.x+roi.width/2,roi.y+roi.height/2);
   if(!el)return null;
   const candidates=[el,...[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.x<=roi.x+roi.width/2&&r.right>=roi.x+roi.width/2&&r.y<=roi.y+roi.height/2&&r.bottom>=roi.y+roi.height/2})];
   const e=intent==='theme-color'?(selector?document.querySelector(selector):null):candidates.find(x=>x.children.length===0&&x.textContent.trim())||el;
   if(!e)return null;const r=e.getBoundingClientRect(),s=getComputedStyle(e);
   return {tag:e.tagName.toLowerCase(),id:e.id,text:e.textContent.trim(),className:typeof e.className==='string'?e.className:'',rect:{x:r.x,y:r.y,width:r.width,height:r.height},background:s.backgroundColor,color:s.color,selectorMatches:selector?document.querySelectorAll(selector).length:null,centerTarget:e===el||e.contains(el)};
  }''',{'roi':roi,'selector':a.selector,'intent':a.intent})
  result['stages']['locate']={'probe':probe,'status':'PASS' if probe else 'FAIL'}
  if not probe:
   await before.close();await browser.close();return result
  rect=probe['rect'];cx=roi['x']+roi['width']/2;cy=roi['y']+roi['height']/2
  if not (rect['x']<=cx<=rect['x']+rect['width'] and rect['y']<=cy<=rect['y']+rect['height']):
   result['stages']['locate']['status']='FAIL';result['stages']['locate']['reason']='selector does not overlap screenshot region'
   await before.close();await browser.close();return result
  if a.intent=='theme-color' and probe['selectorMatches']!=1 and not a.allow_shared:
   result['stages']['locate']['status']='FAIL';result['stages']['locate']['reason']='ambiguous selector'
   await before.close();await browser.close();return result
  modified,trace=static_edit(original,probe);result['stages']['source_trace']=trace
  if modified is None:
   await before.close();await browser.close();return result
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(modified)
  result['stages']['candidate']={'status':'CREATED','candidate_sha256':sha(modified)}
  after=await open_page(modified)
  await after.screenshot(path=str(evidence/'after.png'),animations='disabled')
  if a.intent=='remove-text':
   old_count=await before.evaluate('(text)=>[...document.querySelectorAll("body *")].filter(e=>e.children.length===0&&e.textContent.trim()===text).length',a.target_text)
   new_count=await after.evaluate('(text)=>[...document.querySelectorAll("body *")].filter(e=>e.children.length===0&&e.textContent.trim()===text).length',a.target_text)
   ok=old_count==1 and new_count==0
   verification={'old_text_count':old_count,'new_text_count':new_count}
  else:
   new=await after.evaluate('''({sel,prop})=>{const e=document.querySelector(sel);return e?getComputedStyle(e).getPropertyValue(prop).trim():null}''',{'sel':a.selector,'prop':a.property})
   old=await before.evaluate('''({sel,prop})=>{const e=document.querySelector(sel);return e?getComputedStyle(e).getPropertyValue(prop).trim():null}''',{'sel':a.selector,'prop':a.property})
   ok=old!=new and bool(new)
   verification={'old_computed':old,'new_computed':new,'changed':old!=new}
  # Also verify page remains structurally viable and has no new errors.
  new_page=await after.evaluate('''()=>({bodyVisible:document.body.getBoundingClientRect().height>0,scrollWidth:document.documentElement.scrollWidth,viewportWidth:innerWidth})''')
  ok=ok and new_page['bodyVisible'] and new_page['scrollWidth']<=new_page['viewportWidth']+2 and not errors
  result['stages']['browser_acceptance']={'status':'PASS' if ok else 'FAIL',**verification,**new_page,'page_errors':errors}
  result['status']='CANDIDATE_VERIFIED_REVIEW_REQUIRED' if ok else 'CANDIDATE_FAILED'
  await before.close();await after.close();await browser.close()
 # Report pixel differences but never treat them as proof of intended change alone.
 try:
  from PIL import Image,ImageChops
  b=Image.open(evidence/'before.png').convert('RGB');c=Image.open(evidence/'after.png').convert('RGB');d=ImageChops.difference(b,c);d.save(evidence/'diff.png')
  mask=d.convert('L').point(lambda x:255 if x else 0)
  counts=mask.getcolors(b.width*b.height) or []
  result['stages']['visual_evidence']={'changed_pixels':sum(n for n,v in counts if v),'total_pixels':b.width*b.height,'diff':'diff.png'}
 except Exception as e:result['stages']['visual_evidence']={'status':'NOT_RUN','reason':str(e)}
 return result

if __name__=='__main__':
 try:res=asyncio.run(main())
 except Exception as e:res={'status':'ERROR','error':str(e)}
 evidence.mkdir(parents=True,exist_ok=True)
 (evidence/'result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
 print(json.dumps(res,ensure_ascii=False,indent=2))
 sys.exit(0 if res['status']=='CANDIDATE_VERIFIED_REVIEW_REQUIRED' else 2)
