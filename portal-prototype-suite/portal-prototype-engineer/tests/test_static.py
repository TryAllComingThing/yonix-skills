import json,subprocess,sys,unittest,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';F=ROOT/'tests'/'fixtures'
class TestStatic(unittest.TestCase):
 def run_script(self,name,*args):
  p=subprocess.run([sys.executable,str(S/name),*map(str,args)],capture_output=True,text=True)
  self.assertEqual(p.returncode,0,p.stderr+' '+p.stdout)
  return json.loads(p.stdout)
 def test_inventory(self):
  data=self.run_script('inspect_project.py',F);self.assertGreaterEqual(data['file_count'],1)
 def test_css_audit(self):
  data=self.run_script('inspect_css.py',F);self.assertGreaterEqual(data['counts']['hardcoded_hex_color'],1)
 def test_token_audit(self):
  data=self.run_script('check_design_tokens.py',F);self.assertIn('--brand',data['declared']);self.assertNotIn('--brand',data['unresolved_locally'])
 def test_components(self):
  data=self.run_script('check_components.py',F);self.assertEqual(data['standalone_html_controls'][str(F/'sample.html')]['button_tags'],2)
 def test_evidence(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'manifest.json';subprocess.run([sys.executable,str(S/'build_evidence.py'),str(F),'--output',str(out)],check=True)
   self.assertEqual(json.loads(out.read_text())['acceptance'],'NOT_ASSESSED')
if __name__=='__main__':unittest.main()
