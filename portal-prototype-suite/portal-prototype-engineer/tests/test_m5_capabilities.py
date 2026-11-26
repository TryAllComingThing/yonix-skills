import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[1]
class M5(unittest.TestCase):
 def run_script(self,name,*args):
  return subprocess.run([sys.executable,str(BASE/'scripts'/name),*map(str,args)],capture_output=True,text=True,timeout=90)
 def test_red_single_and_ambiguous(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'x.png'
   for n in (1,2):
    im=Image.new('RGB',(500,400),'white');d=ImageDraw.Draw(im)
    d.rectangle((20,20,190,130),outline='red',width=4)
    if n==2:d.rectangle((220,160,440,320),outline='red',width=4)
    im.save(p)
    r=self.run_script('detect_red_annotations.py','--image',p)
    self.assertEqual(r.returncode,0 if n==1 else 2,r.stdout+r.stderr)
    self.assertEqual(json.loads(r.stdout)['status'],'ONE_REGION' if n==1 else 'AMBIGUOUS')
 def test_vue_owner_simulated(self):
  r=self.run_script('trace_vue_dom.py','--html',BASE/'tests/fixtures/vue-runtime-simulated.html','--selector','[data-testid="save"]','--project',BASE/'tests/fixtures')
  self.assertEqual(r.returncode,0,r.stdout+r.stderr)
  self.assertEqual(json.loads(r.stdout)['status'],'SOURCE_TRACED')
 def test_vue_missing_metadata_blocked(self):
  r=self.run_script('trace_vue_dom.py','--html',BASE/'tests/fixtures/sample.html','--selector','body','--project',BASE/'tests/fixtures')
  self.assertEqual(r.returncode,2,r.stdout+r.stderr)
  self.assertEqual(json.loads(r.stdout)['status'],'RUNTIME_OWNER_UNAVAILABLE')
