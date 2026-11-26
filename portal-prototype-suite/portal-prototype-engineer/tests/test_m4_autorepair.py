import unittest, tempfile, subprocess, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/diagnose_repair_verify.py'
FIXTURE=ROOT/'tests/fixtures/warehouse-operations.html'
class M4Autorepair(unittest.TestCase):
 def run_tool(self,src,out,evidence,intent,region,target=None,selector=None,replacement=None):
  args=[sys.executable,str(SCRIPT),'--input',str(src),'--output',str(out),'--evidence-dir',str(evidence),'--intent',intent,'--region',json.dumps(region)]
  if target:args+=['--target-text',target]
  if selector:args+=['--selector',selector]
  if replacement:args+=['--replacement',replacement,'--allow-shared','--setup-js',"document.documentElement.dataset.theme='night'"]
  return subprocess.run(args,capture_output=True,text=True,timeout=70)
 def test_warehouse_static_text_removal(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td);src=d/'input.html';out=d/'candidate.html';ev=d/'evidence'
   s=FIXTURE.read_text().replace('<div id="task-count">1</div>','<div id="task-count">1</div><p id="demo-note">仅供演示</p>')
   src.write_text(s)
   # Obtain actual DOM target coordinates instead of assuming screenshot pixels.
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':900});page.set_content(s)
    r=page.locator('#demo-note').bounding_box();b.close()
   region={k:r[k] for k in ('x','y','width','height')}
   result=self.run_tool(src,out,ev,'remove-text',region,target='仅供演示')
   self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   self.assertNotIn('仅供演示',out.read_text());self.assertIn('id="task-count"',out.read_text())
   self.assertTrue((ev/'before.png').exists());self.assertTrue((ev/'after.png').exists());self.assertTrue((ev/'diff.png').exists())
   self.assertEqual(json.loads((ev/'result.json').read_text())['status'],'CANDIDATE_VERIFIED_REVIEW_REQUIRED')
 def test_ambiguous_static_text_blocks(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td);src=d/'input.html';out=d/'candidate.html';ev=d/'evidence'
   s=FIXTURE.read_text().replace('<div id="task-count">1</div>','<p>仅供演示</p><p>仅供演示</p><div id="task-count">1</div>');src.write_text(s)
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':900});page.set_content(s);r=page.get_by_text('仅供演示').first.bounding_box();b.close()
   result=self.run_tool(src,out,ev,'remove-text',{k:r[k] for k in ('x','y','width','height')},target='仅供演示')
   self.assertNotEqual(result.returncode,0);self.assertFalse(out.exists())
 def test_theme_source_repair(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td);src=d/'input.html';out=d/'candidate.html';ev=d/'evidence'
   s=FIXTURE.read_text().replace('.action{background:var(--brand);','.action{background-color:#1554b4;')
   src.write_text(s)
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1440,'height':900});page.set_content(s);r=page.locator('#new-task').bounding_box();b.close()
   result=self.run_tool(src,out,ev,'theme-color',{k:r[k] for k in ('x','y','width','height')},selector='.action',replacement='var(--brand)')
   self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   self.assertIn('background-color:var(--brand)',out.read_text())
 def test_input_not_overwritten(self):
  with tempfile.TemporaryDirectory() as td:
   d=Path(td);src=d/'input.html';src.write_text(FIXTURE.read_text())
   result=self.run_tool(src,src,d/'ev','remove-text',{'x':0,'y':0,'width':10,'height':10},target='abc')
   self.assertNotEqual(result.returncode,0)
if __name__=='__main__':unittest.main()
