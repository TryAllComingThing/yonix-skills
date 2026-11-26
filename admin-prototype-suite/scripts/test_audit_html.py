"""Unit tests for the read-only static HTML auditor."""
import importlib.util
from pathlib import Path
import unittest
import shutil
import subprocess
import sys
import tempfile

spec = importlib.util.spec_from_file_location('audit_html', Path(__file__).with_name('audit_html.py'))
audit_html = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_html)

class TestAuditHtml(unittest.TestCase):
    def test_js_not_requested(self):
        r=audit_html.audit('<script>let x=1;</script>')
        self.assertEqual(r['js_syntax']['status'],'NOT_RUN')

    @unittest.skipUnless(shutil.which('node'),'Node.js missing')
    def test_js_valid(self):
        r=audit_html.audit('<script>const x = 1;</script>',check_js=True)
        self.assertEqual(r['js_syntax']['status'],'PASS')
        self.assertEqual(r['js_syntax']['checked'],1)

    @unittest.skipUnless(shutil.which('node'),'Node.js missing')
    def test_js_invalid(self):
        r=audit_html.audit('<script>const = ;</script>',check_js=True)
        self.assertEqual(r['js_syntax']['status'],'FAIL')
        self.assertEqual(r['gate_g0'],'FAIL')

    def test_cli_strict_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'bad.html';f.write_text('<div id="a"></div><div id="a"></div>')
            run=subprocess.run([sys.executable,str(Path(__file__).with_name('audit_html.py')),str(f),'--strict'],capture_output=True,text=True)
            self.assertEqual(run.returncode,2)

    def test_clean_html(self):
        r = audit_html.audit('<html><body><div id="a"></div></body></html>')
        self.assertEqual(r['gate_g0'], 'PASS')
        self.assertEqual(r['script_tags'], 0)

    def test_duplicate_ids(self):
        r = audit_html.audit('<div id="same"></div><span id="same"></span>')
        self.assertEqual(r['duplicate_ids']['same'], 2)
        self.assertEqual(r['gate_g0'], 'FAIL')

    def test_script_and_risks(self):
        r = audit_html.audit('<script>window.render = function(){}; el.innerHTML = "x";</script>')
        self.assertEqual(r['render_assignments'], 1)
        self.assertEqual(r['innerHTML_mentions'], 1)
        self.assertEqual(r['gate_g0'], 'PASS_WITH_WARNINGS')

    def test_external_and_handler(self):
        r = audit_html.audit('<script src="a.js"></script><link href="x.css"><button onclick="go()">OK</button>')
        self.assertEqual(r['external_dependencies'], ['a.js', 'x.css'])
        self.assertEqual(r['inline_event_handlers'], 1)

if __name__ == '__main__':
    unittest.main()
