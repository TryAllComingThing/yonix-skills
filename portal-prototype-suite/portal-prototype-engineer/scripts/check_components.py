import argparse,re,collections
from pathlib import Path
from common import files,emit
p=argparse.ArgumentParser(description='Inventory Vue components and duplicate names')
p.add_argument('project');p.add_argument('--output');a=p.parse_args();r=Path(a.project)
if not r.exists():p.error('path not found')
vue=files(r,{'.vue'});counts=collections.Counter(f.stem.lower() for f in vue)
html=files(r,{'.html'})
controls={}
for f in html:
 s=f.read_text(encoding='utf-8',errors='replace')
 controls[str(f)]={'button_tags':len(re.findall(r'<button\b',s,re.I)),'dialog_roles':len(re.findall(r'role=["\']dialog',s,re.I))}
emit({'vue_components':[str(f) for f in vue],'duplicate_component_names':[k for k,v in counts.items() if v>1],'standalone_html_controls':controls,'limitation':'Inventory only; no AST, dependency graph, runtime component state or handler validation'},a.output)
