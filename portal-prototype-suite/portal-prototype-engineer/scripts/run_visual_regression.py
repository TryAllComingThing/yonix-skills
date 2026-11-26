"""Pixel-level screenshot comparison; requires baseline PNG and Pillow.
Browser capture is separate. Does NOT equate render checks with visual checks.
"""
import argparse,sys
from pathlib import Path
from common import emit
p=argparse.ArgumentParser(description='Compare baseline and candidate PNGs pixel-by-pixel')
p.add_argument('--baseline',required=True);p.add_argument('--candidate',required=True);p.add_argument('--diff');p.add_argument('--threshold',type=float,default=0.001,help='Maximum fraction of changed pixels (default .001)');p.add_argument('--output');a=p.parse_args()
try:from PIL import Image,ImageChops
except ImportError:sys.exit('NOT_RUN: install Pillow for actual pixel comparison (pip install pillow)')
for name in (a.baseline,a.candidate):
 if not Path(name).is_file():sys.exit('NOT_RUN: screenshot not found: '+name)
b=Image.open(a.baseline).convert('RGBA');c=Image.open(a.candidate).convert('RGBA')
if b.size!=c.size:
 emit({'status':'FAIL','reason':'image dimensions differ','baseline_size':b.size,'candidate_size':c.size},a.output);sys.exit(1)
# Ignore alpha channel, but not RGB. Exact pixels are intentionally strict.
b=b.convert('RGB');c=c.convert('RGB');d=ImageChops.difference(b,c)
mask=d.convert('L').point(lambda x:255 if x else 0)
changed=sum(count for count,value in (mask.getcolors(b.width*b.height) or []) if value != 0)
ratio=changed/(b.width*b.height)
if a.diff:d.save(a.diff)
status='PASS' if ratio<=a.threshold else 'FAIL'
emit({'status':status,'changed_pixels':changed,'total_pixels':b.width*b.height,'changed_ratio':ratio,'threshold':a.threshold,'diff':a.diff,'note':'Pixel comparison only; human review required for intended changes'},a.output)
sys.exit(0 if status=='PASS' else 1)
