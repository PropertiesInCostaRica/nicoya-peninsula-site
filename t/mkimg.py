#!/usr/bin/env python3
# Builds mail blast images (banner with ID/price + 2 photo strip) like the #3902 blast
import os, subprocess, sys
try:
    from PIL import Image
except ImportError:
    os.system('pip3 install "Pillow<8" >/dev/null 2>&1 || apt-get install -y python3-pil >/dev/null 2>&1')
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit('ERROR: no pude instalar Pillow (PIL). Avisale a Claude.')
from PIL import ImageDraw
if not hasattr(ImageDraw.ImageDraw, 'textsize'):
    def _ts(self, t, font=None):
        b = self.textbbox((0, 0), t, font=font); return (b[2] - b[0], b[3] - b[1])
    ImageDraw.ImageDraw.textsize = _ts
T = 'https://www.properties-in-costa-rica.com/t/'
W = '/var/www/propertiesincostarica.com/web/emails/images/'
TMP = '/root/mkimg/'
os.makedirs(TMP, exist_ok=True)
def get(url, name):
    p = TMP + name
    if subprocess.call(['wget', '-q', '-O', p, url]) != 0: raise SystemExit('No pude bajar ' + url)
    return p
FB = get(T + 'LSB.ttf', 'LSB.ttf'); FR = get(T + 'LSR.ttf', 'LSR.ttf')
from PIL import Image, ImageDraw, ImageFont
GOLD=(210,172,65)
def cover(im,w,h,fy=0.5):
    im=im.convert('RGB'); r=max(w/im.width,h/im.height)
    im=im.resize((int(im.width*r+.5),int(im.height*r+.5)),Image.LANCZOS)
    x=(im.width-w)//2; y=int((im.height-h)*fy)
    return im.crop((x,y,x+w,y+h))
def spaced(d,xy,t,f,fill,sp=2,anchor_center=False,W=0):
    tw=sum(d.textsize(c,font=f)[0]+sp for c in t)-sp
    x,y=xy
    if anchor_center: x=(W-tw)//2
    for c in t:
        d.text((x,y),c,font=f,fill=fill); x+=d.textsize(c,font=f)[0]+sp
    return tw
def hero(src,out,idc,price,FB,FR,fy=0.5):
    W,H=1200,638
    im=cover(Image.open(src),W,H,fy).convert('RGBA')
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    d.rectangle((0,0,W,62),fill=(255,255,255,70))
    d.rectangle((0,0,W,62),fill=(0,0,0,35))
    for y in range(H-230,H):
        a=int(215*((y-(H-230))/230.0)**1.4); d.line((0,y,W,y),fill=(0,0,0,a))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(FR,34); spaced(d,(0,11),'ID CODE: '+idc,f1,(255,255,255),2,True,W)
    f2=ImageFont.truetype(FB,30); spaced(d,(42,500),'SALES PRICE:',f2,(255,255,255),2)
    f3=ImageFont.truetype(FB,48); spaced(d,(42,542),price,f3,GOLD,1)
    d.rectangle((812,503,1158,594),fill=GOLD)
    f4=ImageFont.truetype(FR,31); tw=d.textsize('VIEW DETAILS',font=f4)[0]+2*11
    spaced(d,(812+(346-tw)//2,530),'VIEW DETAILS',f4,(255,255,255),2)
    im.convert('RGB').save(out,quality=86,optimize=True,progressive=True)
def strip(a,b,out,fa=0.5,fb=0.5):
    W,H,g=1200,399,12; w=(W-g)//2
    im=Image.new('RGB',(W,H),(255,255,255))
    im.paste(cover(Image.open(a),w,H,fa),(0,0)); im.paste(cover(Image.open(b),w,H,fb),(W-w,0))
    im.save(out,quality=86,optimize=True,progressive=True)
C = 'https://cdn.propertiesincostarica.com/properties/Images/'
JOBS = [
  ('3751', C + 'turn-key-ocean-view-estate/opt/24.jpg', 0.5, '#3751', 'US$1,200,000', C + 'turn-key-ocean-view-estate/opt/11.jpg', C + 'turn-key-ocean-view-estate/opt/31.jpg'),
  ('4220', C + 'renovated-hotel/opt/photo-1.jpg', 0.45, '#4220', 'US$780,000', C + 'renovated-hotel/opt/photo-21.jpg', C + 'renovated-hotel/opt/photo-6.jpg'),
]
for code, h, fy, idc, price, a, b in JOBS:
    d = W + code + '/'
    os.makedirs(d, exist_ok=True)
    hero(get(h, code + 'h.jpg'), d + 'hero.jpg', idc, price, FB, FR, fy)
    strip(get(a, code + 'a.jpg'), get(b, code + 'b.jpg'), d + 'pictures2.jpg')
    print('OK https://www.propertiesincostarica.com/emails/images/' + code + '/hero.jpg')
    print('OK https://www.propertiesincostarica.com/emails/images/' + code + '/pictures2.jpg')
print('LISTO')
