import argparse,json,datetime
from pathlib import Path
from common import files,sha256,emit
p=argparse.ArgumentParser(description='Produce verifiable artifact manifest, without inventing test results')
p.add_argument('project');p.add_argument('--reports',nargs='*',default=[]);p.add_argument('--output',required=True);p.add_argument('--baseline');a=p.parse_args();r=Path(a.project)
if not r.exists():p.error('project not found')
reports=[]
for x in a.reports:
 f=Path(x)
 if not f.exists():p.error('report missing: '+x)
 try:content=json.loads(f.read_text())
 except Exception:content={'unparsed':True}
 reports.append({'path':str(f),'sha256':sha256(f),'reported_status':content.get('status','UNKNOWN')})
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'project':str(r.resolve()),'baseline':a.baseline,'files':[{'path':str(f.relative_to(r)) if r.is_dir() else f.name,'sha256':sha256(f)} for f in files(r)],'reports':reports,'acceptance':'NOT_ASSESSED','warning':'This manifest does not claim tests were run; inspect reports for evidence'}
emit(manifest,a.output)
