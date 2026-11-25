#!/usr/bin/env python3
# Change #4107 price to US$700,000 on the property page and every listing card
import re, os, glob, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/'; os.makedirs(B, exist_ok=True)
st = time.strftime('%Y%m%d%H%M')
NEW = '<s>US$335,000</s> Reduced to US$315,000'
PAGE = W + 'properties/orotina/for_sale/investment-opportunity.html'
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s): open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
s = rd(PAGE)
t = re.sub(r'(<!-- InstanceBeginEditable name="price" -->).*?(<!-- InstanceEndEditable -->)',
           lambda m: m.group(1) + 'Sales Price: ' + NEW + m.group(2), s, flags=re.S)
if t != s:
    shutil.copy2(PAGE, B + 'investment-opportunity.html.' + st); wr(PAGE, t)
    print('Pagina de la propiedad: precio cambiado a ' + NEW)
else:
    print('OJO: no encontre el precio en la pagina de la propiedad')
def fixcard(m):
    c = m.group(0)
    if 'orotina/for_sale/investment-opportunity.html' not in c: return c
    return re.sub(r'<li>(\s*<strong>)?\s*Sales Price:.*?</li>', lambda m: '<li>' + ('<strong>' if m.group(1) else '') + 'Sales Price: ' + NEW + ('</strong>' if m.group(1) else '') + '</li>', c, count=1, flags=re.S)
n = 0
for f in sorted(glob.glob(W + '*.htm*') + glob.glob(W + 'region_and_price/*.htm*')):
    s = rd(f)
    if 'orotina/for_sale/investment-opportunity.html' not in s or '<article' not in s: continue
    t = re.sub(r'<article class="listing".*?</article>', fixcard, s, flags=re.S)
    if t != s:
        shutil.copy2(f, B + os.path.basename(f) + '.' + st); wr(f, t); n += 1
        print('Tarjeta actualizada en', f[len(W):])
print('%d paginas con la tarjeta actualizada' % n)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
