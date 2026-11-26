import argparse,re
from pathlib import Path
from common import files,emit
p=argparse.ArgumentParser(description='Heuristic CSS audit; not a CSS parser or computed-style test')
p.add_argument('project');p.add_argument('--output');a=p.parse_args();r=Path(a.project)
if not r.exists():p.error('path not found')
findings=[]
for f in files(r,{'.css','.vue','.html'}):
 s=f.read_text(encoding='utf-8',errors='replace')
 if f.suffix!='.css':
  s='\n'.join(re.findall(r'<style\b[^>]*>(.*?)</style>',s,re.I|re.S))
 for pattern,kind in [(r'!important\b','important_override'),(r'#[0-9a-fA-F]{3,8}\b','hardcoded_hex_color'),(r'\b(?:rgb|rgba|hsl|hsla)\s*\(','literal_color')]:
  for m in re.finditer(pattern,s):
   findings.append({'file':str(f),'line':s.count('\n',0,m.start())+1,'kind':kind,'value':m.group(0)})
emit({'scope':str(r),'findings':findings,'counts':{k:sum(x['kind']==k for x in findings) for k in ('important_override','hardcoded_hex_color','literal_color')},'limitation':'Regex inventory only; excludes inline styles, media semantics and runtime computed styles'},a.output)
