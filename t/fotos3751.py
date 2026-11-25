#!/usr/bin/env python3
# Replace #3751 photos with Klaudia's new photos (Google Drive), 3 per row, pool first
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
PAGE = W + 'properties/nicoya_peninsula/for_sale/abundance.html'
D = W + 'properties/Images/turn-key-ocean-view-estate/new/'
os.makedirs(D + 'thumbs', exist_ok=True)
TMP = '/root/fotos3751/'; os.makedirs(TMP, exist_ok=True)
URL = 'https://cdn.propertiesincostarica.com/properties/Images/turn-key-ocean-view-estate/new/'
ID = {
 1:'1LI0hxr1pIdOQzdLv3bo71Xwyp3hY7ZrE', 2:'1kbUWcp60EMNjvaOyOk9dqmFdWYD36vPt', 3:'1-AmrlPdEG8hfr1whO0i9WdHn5iq6zMmW',
 4:'1ApMGsyaN23uYPv4wQGCL0NskRQ_C98gv', 5:'1-ZMla6_4smBs380oBe4kdyIOYNAQBNs9', 6:'1kg8GUIBZaQKEAE3T7cJE8x9m79qL-tQV',
 7:'1fnGorjRBr1MIk-tJb0_IBwJyNlS-mzfF', 8:'1PjWIwVxHYI5Fgy982vnqpwfP7HuldlOY', 9:'1EgQux3V9N4-nPLhiMJN3aN7hKiN9AcMv',
 10:'1xR6po0SNby3yHDRFff03MITVSAreMWyd', 11:'1AOe3AfWTx5LD2TYaSKvMPfNXXXf2LN_h', 12:'1vNALE6VP-kxTZUNq-yR2J9ndXFgCJIAq',
 14:'14M4z5rzyk_f1tHJZ4Lk3A7FMN01e37h4', 15:'1TJjaQ_pE_hsyR9MI5P1QORjEv_IOMVQJ', 16:'1T_XODGz5njF11IWsB5-Ghg20nmS7CkkZ',
 17:'1O1MZ7lX6Zm5auour9xPDNsSAluGiY9ws', 18:'19ufioBdw-CiCDS6fzTO7k6F2e8oBflpt', 19:'1oUoVhRCqNWsdKjHA7BLsKjxa3vQxgm2w',
 20:'1AysE1c3H4FwBBuxrxJqSi8y04MBsHxKl', 21:'1Td_--wECY-ehBvOjevVV9EDWLLCvpzc6', 23:'1VVEwo_8KXv3Up7ZhdZOcjnwfgCUV8yT2',
 24:'1Uj3p35X09RbGg_0qhqvMQ7SdtOn7gl2C', 25:'1_-D3BIjFsDkLNp9uHMs0zevfdSIDZHJS', 27:'1i1PfgRhiObDeaNtQ_CVNqvAVMQnSeqsa',
 28:'1wigHEgvjUPL1T_w08GJXjTvGqREp_QKT', 29:'1lvuui3vu-tJXbjwtRSvUc5vafRctHlmq', 31:'1nYvXC4_xu2_ZJsqKI0DIPCJy8eiwe7h4',
 32:'1e-VOtgeUOL-Hf6fisRryXIEmK2a68q8G', 33:'1wKkrTvd3S3EH76JIJPYdlkPfojUkA9Im', 34:'1wdpLi-kbAswjklKML91-SCk9Qst1E6NE',
 35:'1jc2Kfq9Zsr9YFloqIveWr8dxAMLKOSiA', 36:'1QlM8R2_pVZrc3PzGCQHm1-rEDoOwBkqh', 37:'1D1yj8zW-G0fQ0W8c0nYCs_vZSBs2DlGz',
 39:'1dzJZ_-ir4ex51hnn7X47UcEM2X61i_LL',
}
GROUPS = [
 ('START', [[2, 5, 29], [1, 18, 19]]),
 ('outdoor dining and lounging.</p>', [[17, 9, 3], [16, 15, 11]]),
 ('Both wings open onto the pool terrace.</p>', [[12, 14, 4]]),
 ('a telephone and a safe.</p>', [[25, 27, 21], [20, 23, 24]]),
 ('prepare their own meals.</p>', [[10, 39, 6]]),
 ('its own water storage tank with a pump.</p>', [[7, 8, 28]]),
 ('boat trips to Tortuga Island are also within reach for day trips.</p>', [[31, 32, 36], [33, 34], [35, 37]]),
]
ALT = 'Ocean view estate, pool, guest casita, Tango Mar, Nicoya Peninsula, house for sale, Costa Rica'
def get(n):
    p = TMP + '%d.src' % n
    if not os.path.exists(p) or os.path.getsize(p) < 10000:
        u = 'https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t' % ID[n]
        if subprocess.call(['wget', '-q', '-O', p, u]) != 0 or os.path.getsize(p) < 10000:
            raise SystemExit('ERROR: no pude bajar la foto %d de Drive (revisa que la carpeta este compartida con el link)' % n)
    return p
def conv(n, k):
    im = Image.open(get(n))
    if ImageOps and hasattr(ImageOps, 'exif_transpose'):
        try: im = ImageOps.exif_transpose(im)
        except Exception: pass
    im = im.convert('RGB')
    if im.width > 1600:
        im = im.resize((1600, int(im.height * 1600.0 / im.width)), Image.LANCZOS)
    im.save(D + '%d.jpg' % k, quality=84, optimize=True, progressive=True)
    tw, th = 500, 374
    r = max(float(tw) / im.width, float(th) / im.height)
    t = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
    x = (t.width - tw) // 2; y = (t.height - th) // 2
    t.crop((x, y, x + tw, y + th)).save(D + 'thumbs/%d.jpg' % k, quality=82, optimize=True)
k = 0; html = {}
for anchor, rows in GROUPS:
    out = []
    for ri, row in enumerate(rows):
        a = ''
        for n in row:
            k += 1; conv(n, k)
            a += '<a href="%s%d.jpg"><img src="%sthumbs/%d.jpg" alt="%s" width="250" height="187"></a>' % (URL, k, URL, k, ALT)
        if anchor == 'START' and ri == 0:
            a += '\n<span class="to_enlarge">Click on the pictures to enlarge</span>'
        out.append('<p class="photo">\n' + a + '\n</p>')
    html[anchor] = '\n'.join(out)
print('%d fotos nuevas listas' % k)
s = open(PAGE, encoding='utf-8', errors='surrogateescape').read()
shutil.copy2(PAGE, '/root/respaldos/abundance.html.' + time.strftime('%Y%m%d%H%M'))
a = s.index('<!-- InstanceBeginEditable name="content" -->') + len('<!-- InstanceBeginEditable name="content" -->')
e = s.index('<!-- InstanceEndEditable -->', a)
c = s[a:e]
c = re.sub(r'\s*<p class="photo">.*?</p>', '', c, flags=re.S)
c = '\n' + html['START'] + c
for anchor, _ in GROUPS[1:]:
    if anchor not in c: raise SystemExit('ERROR: no encontre el texto: ' + anchor)
    c = c.replace(anchor, anchor + '\n\n' + html[anchor], 1)
s = s[:a] + c + s[e:]
s = s.replace('turn-key-ocean-view-estate/opt/24.jpg', 'turn-key-ocean-view-estate/new/1.jpg')
open(PAGE, 'w', encoding='utf-8', errors='surrogateescape').write(s)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('Pagina #3751 actualizada: https://www.propertiesincostarica.com/properties/nicoya_peninsula/for_sale/abundance.html')

# ---- Mail blast images (same #3902 format) with the new photos ----
from PIL import ImageDraw
if not hasattr(ImageDraw.ImageDraw, 'textsize'):
    def _ts(self, t, font=None):
        b = self.textbbox((0, 0), t, font=font); return (b[2] - b[0], b[3] - b[1])
    ImageDraw.ImageDraw.textsize = _ts
from PIL import ImageDraw, ImageFont
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

FB = TMP + 'LSB.ttf'; FR = TMP + 'LSR.ttf'
subprocess.call(['wget', '-q', '-O', FB, 'https://www.properties-in-costa-rica.com/t/LSB.ttf'])
subprocess.call(['wget', '-q', '-O', FR, 'https://www.properties-in-costa-rica.com/t/LSR.ttf'])
E = W + 'emails/images/3751/'; os.makedirs(E, exist_ok=True)
hero(D + '1.jpg', E + 'hero.jpg', '#3751', 'US$1,200,000', FB, FR, 0.5)
strip(D + '6.jpg', D + '22.jpg', E + 'pictures2.jpg')
print('Mail blast #3751: imagenes nuevas listas')
print('LISTO')
