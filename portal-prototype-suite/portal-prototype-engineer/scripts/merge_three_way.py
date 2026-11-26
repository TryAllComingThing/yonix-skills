"""True base/ours/theirs 3-way merge using git merge-file; fail closed on conflicts.
Never overwrite input files; caller must review candidate output.
"""
import argparse,subprocess,tempfile,json,sys,hashlib
from pathlib import Path
from common import emit,sha256
p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--ours',required=True);p.add_argument('--theirs',required=True);p.add_argument('--output',required=True);p.add_argument('--report');a=p.parse_args()
paths=[Path(getattr(a,k)) for k in ('base','ours','theirs')]
if any(not x.is_file() for x in paths):sys.exit('BLOCKED: missing input')
out=Path(a.output)
if out.resolve() in [x.resolve() for x in paths]:sys.exit('BLOCKED: output may not overwrite input')
with tempfile.TemporaryDirectory() as d:
 d=Path(d)
 for name,path in zip(('base','ours','theirs'),paths):(d/name).write_bytes(path.read_bytes())
 result=subprocess.run(['git','merge-file','-p','-L','OURS','-L','BASE','-L','THEIRS',str(d/'ours'),str(d/'base'),str(d/'theirs')],capture_output=True)
 status='CLEAN_CANDIDATE' if result.returncode==0 else 'CONFLICT_BLOCKED' if result.returncode>0 else 'ERROR'
 if status=='CLEAN_CANDIDATE':out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(result.stdout)
 report={'status':status,'input_sha256':{k:sha256(v) for k,v in zip(('base','ours','theirs'),paths)},'output':str(out) if status=='CLEAN_CANDIDATE' else None,'candidate_sha256':sha256(out) if status=='CLEAN_CANDIDATE' else None,'conflict_markers':result.stdout.count(b'<<<<<<<'),'requires_review':True,'stderr':result.stderr.decode(errors='replace')}
 emit(report,a.report)
 sys.exit(0 if status=='CLEAN_CANDIDATE' else 2)
