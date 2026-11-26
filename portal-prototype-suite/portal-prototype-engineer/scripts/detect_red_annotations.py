"""Detect saturated red rectangular annotations. Never infer target automatically from ambiguous boxes."""
import argparse,json,sys
from pathlib import Path
import cv2
p=argparse.ArgumentParser();p.add_argument('--image',required=True);p.add_argument('--output');p.add_argument('--min-area',type=int,default=350);a=p.parse_args()
im=cv2.imread(a.image)
if im is None:sys.exit('Cannot read screenshot')
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
mask=cv2.bitwise_or(cv2.inRange(hsv,(0,110,100),(12,255,255)),cv2.inRange(hsv,(168,110,100),(179,255,255)))
mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)))
contours,_=cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
boxes=[]
for c in contours:
 x,y,w,h=cv2.boundingRect(c)
 if w*h<a.min_area or w<12 or h<12:continue
 area=cv2.contourArea(c); perimeter=cv2.arcLength(c,True)
 if perimeter==0:continue
 # Outline rectangles have low filled area and red pixels along edges.
 fill=area/(w*h); region=mask[y:y+h,x:x+w]; border=cv2.countNonZero(region[:max(2,min(5,h//6)),:])+cv2.countNonZero(region[-max(2,min(5,h//6)):,:])+cv2.countNonZero(region[:, :max(2,min(5,w//6))])+cv2.countNonZero(region[:, -max(2,min(5,w//6)):])
 if border<max(20,(w+h)//4):continue
 boxes.append({'x':x,'y':y,'width':w,'height':h,'area':w*h,'fill':round(fill,3)})
boxes.sort(key=lambda b:b['area'],reverse=True)
# Suppress nested contours from thick outlines.
result=[]
for b in boxes:
 if any(abs(b['x']-z['x'])<8 and abs(b['y']-z['y'])<8 and abs(b['width']-z['width'])<16 and abs(b['height']-z['height'])<16 for z in result):continue
 result.append(b)
status='ONE_REGION' if len(result)==1 else ('AMBIGUOUS' if result else 'NOT_FOUND')
report={'status':status,'regions':result,'image_dimensions':{'width':im.shape[1],'height':im.shape[0]},'requires_confirmation':True,'note':'Coordinates are screenshot pixels; scale/scroll must match browser capture. Only saturated red outlines supported.'}
if a.output:Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False))
sys.exit(0 if status=='ONE_REGION' else 2)
