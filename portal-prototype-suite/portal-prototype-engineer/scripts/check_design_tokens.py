import argparse,re
from pathlib import Path
from common import files,emit
p=argparse.ArgumentParser(description='Check CSS custom property declarations and references')
p.add_argument('project');p.add_argument('--output');a=p.parse_args();r=Path(a.project)
if not r.exists():p.error('path not found')
css='\n'.join(f.read_text(encoding='utf-8',errors='replace') for f in files(r,{'.css','.vue','.html'}))
css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
declared=set(re.findall(r'(--[\w-]+)\s*:',css));used=set(re.findall(r'var\(\s*(--[\w-]+)',css))
# External theme stylesheets may provide declarations: unknown rather than definitive failure.
emit({'declared':sorted(declared),'used':sorted(used),'unresolved_locally':sorted(used-declared),'unused_locally':sorted(declared-used),'limitation':'Static local check; external stylesheets, JS runtime injection and CSS fallback values are not resolved'},a.output)
