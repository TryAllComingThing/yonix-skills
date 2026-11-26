"""Narrow, explicit M2 diagnostic auto-repair: unified API doc layout or code contrast.
Creates a candidate copy; never overwrites the input. No claim of generic CSS remediation.
"""
import argparse,asyncio,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--kind',choices=['layout','contrast'],required=True);p.add_argument('--report',required=True);a=p.parse_args()
src=Path(a.input);dst=Path(a.output)
if src.resolve()==dst.resolve():p.error('input and output must differ')
s=src.read_text()
if '.m369-doc-shell' not in s or '.m369-doc-body' not in s:p.error('required document component not found')
async def check(path):
 from playwright.async_api import async_playwright
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.set_content(path.read_text(),wait_until='domcontentloaded')
  try:await page.get_by_text('登 录',exact=True).first.click(timeout=2000)
  except Exception:pass
  await page.evaluate("""()=>{S.page='POR-11';S.lang='zh';S.theme='steady-blue';render();m369OpenDoc('chat','svc-chat')}""")
  v=await page.evaluate("""()=>{const e=document.querySelector('.m369-doc-body'),p=e?.querySelector('pre');return {bodyWidth:e?.getBoundingClientRect().width,codeBg:p?getComputedStyle(p).backgroundColor:null,codeColor:p?getComputedStyle(p).color:null,visible:!!e&&e.getBoundingClientRect().height>0}}""")
  v['errors']=errors;await browser.close();return v
before=asyncio.run(check(src));bad=(before['bodyWidth'] or 0)<600 if a.kind=='layout' else before['codeBg']!='rgb(17, 24, 39)'
if not bad:
 Path(a.report).write_text(json.dumps({'status':'NOT_REPRODUCED','before':before},indent=2));sys.exit(1)
if a.kind=='layout':
 css='''<style id="pe-m2-layout-repair">
.s719.v721.m369-compact-support .s719-columns{display:block!important;min-width:0!important}
.s719.v721.m369-compact-support .s719-columns>.s719-section{width:100%!important;max-width:none!important;min-width:0!important}
.s719.v721.m369-compact-support .s719-guide{display:block!important;width:100%!important;min-width:0!important}
.s719.v721.m369-compact-support .m369-doc-shell{display:grid!important;grid-template-columns:220px minmax(0,1fr)!important;width:100%!important;gap:24px!important}
.s719.v721.m369-compact-support .m369-doc-body{min-width:0!important;width:100%!important}
@media(max-width:800px){.s719.v721.m369-compact-support .m369-doc-shell{grid-template-columns:minmax(0,1fr)!important}}
</style>'''
else:
 css='''<style id="pe-m2-code-repair">
.s719.v721.m369-compact-support .m369-doc-body pre,.s719.v721.m369-compact-support .m369-doc-body pre code{background:#111827!important;color:#e5edf8!important;-webkit-text-fill-color:#e5edf8!important;text-shadow:none!important}
</style>'''
if '</head>' not in s:p.error('HTML head closing tag not found')
dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(s.replace('</head>',css+'</head>',1))
after=asyncio.run(check(dst));ok=after['bodyWidth']>600 if a.kind=='layout' else after['codeBg']=='rgb(17, 24, 39)' and after['codeColor']=='rgb(229, 237, 248)'
report={'kind':a.kind,'status':'REPAIRED_VERIFIED' if ok and not after['errors'] else 'FAIL','input':str(src),'candidate':str(dst),'before':before,'after':after,'method':'narrow selector-based CSS candidate, independent of known-good source; needs maintainable upstream integration'}
Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(0 if report['status']=='REPAIRED_VERIFIED' else 1)
