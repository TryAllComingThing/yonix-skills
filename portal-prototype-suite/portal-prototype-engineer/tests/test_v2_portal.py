import json, pathlib, subprocess, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class PortalV2Tests(unittest.TestCase):
 def test_spec_fixture_build(self):
  with tempfile.TemporaryDirectory() as d:
   output=pathlib.Path(d)/'portal.html'
   p=subprocess.run([sys.executable,str(ROOT/'scripts/build_portal_fixture.py'),'--spec',str(ROOT/'tests/scenarios/portal-create.json'),'--output',str(output)],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr)
   s=output.read_text()
   self.assertIn('模型服务',s);self.assertIn('data-route="catalog"',s);self.assertIn('detailDialog',s)
 def test_coverage_two_equal_gates(self):
  s=(ROOT/'references/portal-acceptance.md').read_text()
  self.assertIn('A: Requirement',s);self.assertIn('B: Screenshot',s)
 def test_preserved_legacy_tools(self):
  for name in ['trace_vue_dom.py','detect_red_annotations.py','run_regression_matrix.py','merge_three_way.py']:
   self.assertTrue((ROOT/'scripts'/name).exists())
if __name__=='__main__':unittest.main()
