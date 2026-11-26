import argparse, json, subprocess
from pathlib import Path
from common import files,sha256,emit
p=argparse.ArgumentParser(description='Read-only project inventory and baseline fingerprint')
p.add_argument('project');p.add_argument('--output');a=p.parse_args()
r=Path(a.project).resolve()
if not r.exists():p.error('project does not exist')
fs=files(r,{'.html','.vue','.ts','.tsx','.js','.jsx','.css','.json','.md','.yaml','.yml'})
manifest={}
for name in ['package.json','package-lock.json','pnpm-lock.yaml','yarn.lock','design-system/DESIGN.md','DESIGN.md']:
 f=r/name
 if f.is_file():manifest[name]={'sha256':sha256(f),'bytes':f.stat().st_size}
framework=[]
if (r/'package.json').exists():
 try:
  pkg=json.loads((r/'package.json').read_text());deps={**pkg.get('dependencies',{}),**pkg.get('devDependencies',{})}
  framework=[x for x in ('vue','vite','react','next','nuxt','pinia','typescript') if x in deps]
 except Exception:pass
try:
 g=subprocess.run(['git','-C',str(r),'status','--porcelain'],capture_output=True,text=True,timeout=5)
 dirty=g.stdout.splitlines() if g.returncode==0 else None
 commit=subprocess.run(['git','-C',str(r),'rev-parse','HEAD'],capture_output=True,text=True,timeout=5)
 revision=commit.stdout.strip() if commit.returncode==0 else None
except Exception:dirty=revision=None
emit({'project':str(r),'file_count':len(fs),'framework':framework,'authority':manifest,'git_commit':revision,'git_dirty_files':dirty,'sample_files':[str(f.relative_to(r)) for f in fs[:100]],'warning':'Inventory only; does not select authoritative baseline among diverging artifacts'},a.output)
