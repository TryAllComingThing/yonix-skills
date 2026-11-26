"""Validator mutation tests: intentionally corrupt a complete temporary suite."""
import importlib.util, pathlib, tempfile, shutil, unittest
P=pathlib.Path(__file__).with_name('validate_suite.py')
spec=importlib.util.spec_from_file_location('validate_suite',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SuiteTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.root=pathlib.Path(self.tmp.name)/'suite'
  shutil.copytree(P.parent.parent,self.root,ignore=shutil.ignore_patterns('__pycache__'))
 def tearDown(self):self.tmp.cleanup()
 def test_valid(self):self.assertEqual(m.validate(self.root)[0],[])
 def test_missing(self):
  (self.root/'templates/page-spec.md').unlink()
  self.assertTrue(any('MISSING' in e for e in m.validate(self.root)[0]))
 def test_malformed_frontmatter(self):
  p=self.root/'skills/prototype-ux-design/SKILL.md';p.write_text('bad')
  self.assertTrue(any('FRONTMATTER' in e for e in m.validate(self.root)[0]))
 def test_duplicate_name(self):
  p=self.root/'skills/prototype-ux-design/SKILL.md';s=p.read_text();s=s.replace('name: prototype-ux-design','name: prototype-orchestrator',1);p.write_text(s)
  self.assertTrue(any('DUPLICATE' in e for e in m.validate(self.root)[0]))
 def test_invalid_script(self):
  (self.root/'scripts/audit_html.py').write_text('def (')
  self.assertTrue(any('PYTHON' in e for e in m.validate(self.root)[0]))
if __name__=='__main__':unittest.main()
