import unittest,subprocess,tempfile,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts';F=ROOT/'tests/fixtures';SC=ROOT/'tests/scenarios'
class Closure(unittest.TestCase):
 def call(self,name,*args):return subprocess.run([sys.executable,str(S/name),*map(str,args)],capture_output=True,text=True,timeout=90)
 def test_runtime_themes_blind_domain(self):
  p=self.call('check_runtime_themes.py','--html',F/'warehouse-operations.html','--contract',SC/'warehouse-themes.json')
  self.assertEqual(p.returncode,0,p.stdout+p.stderr)
  r=json.loads(p.stdout);self.assertEqual(r['status'],'PASS');self.assertEqual(len(r['measurements']),4)
 def test_runtime_themes_negative(self):
  with tempfile.TemporaryDirectory() as d:
   h=Path(d)/'broken.html';h.write_text((F/'warehouse-operations.html').read_text().replace('background:var(--brand)','background:#1554b4'))
   p=self.call('check_runtime_themes.py','--html',h,'--contract',SC/'warehouse-themes.json')
   self.assertNotEqual(p.returncode,0);self.assertEqual(json.loads(p.stdout)['status'],'FAIL')
 def test_dom_locator_blind_domain(self):
  p=self.call('locate_screenshot_dom.py','--html',F/'warehouse-operations.html','--region','{"x":240,"y":110,"width":170,"height":50}')
  self.assertEqual(p.returncode,0,p.stderr)
  r=json.loads(p.stdout);self.assertTrue(r['requires_confirmation']);self.assertTrue(r['candidates'])
 def test_three_way_clean_and_conflict(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);base=d/'base';ours=d/'ours';theirs=d/'theirs';out=d/'out'
   base.write_text('alpha\nbeta\ngamma\ndelta\n');ours.write_text('ALPHA\nbeta\ngamma\ndelta\n');theirs.write_text('alpha\nbeta\ngamma\nDELTA\n')
   p=self.call('merge_three_way.py','--base',base,'--ours',ours,'--theirs',theirs,'--output',out)
   self.assertEqual(p.returncode,0,p.stderr+p.stdout);self.assertIn('ALPHA',out.read_text());self.assertIn('DELTA',out.read_text())
   theirs.write_text('OTHER\nbeta\ngamma\ndelta\n');out.unlink()
   p=self.call('merge_three_way.py','--base',base,'--ours',ours,'--theirs',theirs,'--output',out)
   self.assertNotEqual(p.returncode,0);self.assertFalse(out.exists());self.assertEqual(json.loads(p.stdout)['status'],'CONFLICT_BLOCKED')
 def test_interaction_blind_domain(self):
  p=self.call('run_interaction_tests.py','--html',F/'warehouse-operations.html','--scenario',SC/'warehouse-interaction.json','--executable-path','/usr/bin/chromium')
  self.assertEqual(p.returncode,0,p.stdout+p.stderr);self.assertEqual(len(json.loads(p.stdout)['steps']),6)
if __name__=='__main__':unittest.main()
