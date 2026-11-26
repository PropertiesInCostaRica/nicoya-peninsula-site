#!/usr/bin/env python3
# Whale Bay Villa #4241: the owners say it is NOT an infinity pool. Fix the page and its cards.
import re, os, glob, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
PAGE = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
B = '/root/respaldos/fixpool4241-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s): open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
def fix(t):
    t = re.sub(r'\b[Aa]n infinity edge pool', lambda m: 'A pool' if m.group(0)[0] == 'A' else 'a pool', t)
    t = re.sub(r'\binfinity edge pool', 'pool', t)
    t = re.sub(r'\bInfinity edge pool', 'Pool', t)
    t = re.sub(r'\bInfinity [Ee]dge\b', 'Ocean view pool', t)
    t = re.sub(r'\binfinity pool', 'pool', t)
    t = re.sub(r'\bInfinity [Pp]ool', 'Pool', t)
    return t
s = rd(PAGE); n = len(re.findall(r'infinity', s, re.I))
shutil.copy2(PAGE, B + 'whale-bay-villa.html'); s = fix(s); wr(PAGE, s)
print('Pagina: %d cambios, quedan %d' % (n, len(re.findall(r'infinity', s, re.I))))
c = 0
for p in glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*'):
    if '/properties/' in p: continue
    t = rd(p)
    if 'whale-bay-villa.html' not in t or not re.search('infinity', t, re.I): continue
    new = re.sub(r'<article class="listing".*?</article>', lambda m: fix(m.group(0)) if 'whale-bay-villa.html' in m.group(0) else m.group(0), t, flags=re.S)
    if new != t:
        shutil.copy2(p, B + p[len(W):].replace('/', '_')); wr(p, new); c += 1
        print('Tarjeta corregida: ' + p[len(W):])

# Kitchen photos from the owners' Airbnb listing
import subprocess
from PIL import Image
IMG = W + 'properties/Images/whale-bay-villa-2/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/whale-bay-villa-2/opt/'
AB = 'https://a0.muscache.com/im/pictures/hosting/Hosting-987599427898041723/original/'
KIT = {'k1': AB + '03df42dd-39cd-41de-981b-662d63aa2578.jpeg', 'k2': AB + 'af736bd0-fe88-41a7-9383-04ccf1ba1458.jpeg', 'k3': AB + '9be213f2-f06e-423a-8cbb-13a26f4f9aef.jpeg'}
ok = []
for k, u in sorted(KIT.items()):
    tmp = '/root/kit_' + k + '.jpg'
    subprocess.call(['wget', '-q', '-U', 'Mozilla/5.0', '-O', tmp, u + '?im_w=1600'])
    if not os.path.exists(tmp) or os.path.getsize(tmp) < 10000:
        print('AVISO: no pude bajar la foto de cocina ' + k); continue
    im = Image.open(tmp).convert('RGB')
    if im.width > 1600: im = im.resize((1600, int(im.height * 1600.0 / im.width)), Image.LANCZOS)
    im.save(IMG + 'photo-%s.jpg' % k, quality=84, optimize=True, progressive=True)
    tw, th = 500, 374
    r = max(float(tw) / im.width, float(th) / im.height)
    t = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
    x = (t.width - tw) // 2; y = (t.height - th) // 2
    os.makedirs(IMG + 'thumbs', exist_ok=True)
    t.crop((x, y, x + tw, y + th)).save(IMG + 'thumbs/photo-%s.jpg' % k, quality=82, optimize=True)
    os.remove(tmp); ok.append(k)
s = rd(PAGE)
if ok and 'photo-k1.jpg' not in s:
    alt = 'Whale Bay Villa kitchen, Villas del Mar, Tambor, Costa Rica'
    row = '<p class="photo">\n' + ''.join('<a href="%sphoto-%s.jpg"><img src="%sthumbs/photo-%s.jpg" alt="%s" width="250" height="187"></a>' % (CDN, k, CDN, k, alt) for k in ok) + '\n</p>'
    i = s.find('The kitchen has granite counters')
    j = s.find('</p>', i) + 4 if i >= 0 else -1
    if j > 3:
        s = s[:j] + '\n' + row + s[j:]; wr(PAGE, s); print('Fotos de cocina agregadas: %d' % len(ok))
    else: print('OJO: no encontre el texto de la cocina')
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO (%d paginas con tarjeta)' % c)
