import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestReplay(unittest.TestCase):
 def test_historical_signature_and_blocked_fork(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);a=d/'a.html';b=d/'b.html';a.write_text('<html>old</html>');b.write_text('<html>new marker</html>')
   m=d/'cases.json';m.write_text(json.dumps({'cases':[{'id':'patch','bad':str(a),'good':str(b),'bad_absent':'marker','good_present':'marker'},{'id':'fork','kind':'fork','bad':str(a),'good':str(b)}]}))
   p=subprocess.run([sys.executable,str(ROOT/'scripts/replay_historical.py'),'--cases',str(m)],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr)
   r=json.loads(p.stdout)
   self.assertEqual(r['cases'][0]['status'],'PATCH_REPLAY_SOURCE_CONFIRMED')
   self.assertEqual(r['cases'][1]['status'],'BLOCKED')
   self.assertFalse(r['autonomous_repair_verified'])
 def test_missing_baseline_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);m=d/'cases.json';m.write_text(json.dumps({'cases':[{'id':'missing','bad':str(d/'missing'),'good':str(d/'also-missing')}]}))
   p=subprocess.run([sys.executable,str(ROOT/'scripts/replay_historical.py'),'--cases',str(m)],capture_output=True,text=True)
   self.assertNotEqual(p.returncode,0)
   self.assertEqual(json.loads(p.stdout)['cases'][0]['status'],'NOT_TESTED')
if __name__=='__main__':unittest.main()
