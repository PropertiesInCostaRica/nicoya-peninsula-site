#!/usr/bin/env python3
# #3751 to the NEW DESIGN: uses the Whale Bay Villa page as the design shell and moves in all of #3751's content.
# Run AFTER mp3751.py. Backup first.
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/properties/'
P = W + 'nicoya_peninsula/for_sale/abundance.html'
SHELL = W + 'puntarenas/for_sale/whale-bay-villa.html'
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def get(s, n):
    a = s.index('<!-- InstanceBeginEditable name="%s" -->' % n)
    a = s.index('-->', a) + 3
    return s[a:s.index('<!-- InstanceEndEditable -->', a)]
def put(s, n, val):
    a = s.index('<!-- InstanceBeginEditable name="%s" -->' % n)
    a = s.index('-->', a) + 3
    e = s.index('<!-- InstanceEndEditable -->', a)
    return s[:a] + val + s[e:]
s = rd(P)
def words(x):
    x = x.replace('<p><strong>Exclusive listing.</strong> A beautifully', '<p>A beautifully')
    x = x.replace('Exclusive: masterfully', 'Masterfully')
    x = x.replace('Detached Guest House |', 'Detached GUESTHOUSE |')
    x = x.replace('<p><strong>Guest House</strong></p>', '<p><strong>GUESTHOUSE</strong></p>')
    return x
if 'hd--v2' in s or 'new_site.css' in s:
    s2 = words(s)
    if s2 != s:
        shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
        open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
        print('LISTO: textos corregidos')
    else:
        print('Ya tiene el diseno nuevo')
    raise SystemExit
if 'TnLrCVA42E3' not in s:
    print('Primero corre mp3751.py'); raise SystemExit
out = rd(SHELL)
for n in ['doctitle', 'head', 'title', 'code', 'price', 'features', 'content', 'hidden']:
    out = put(out, n, get(s, n))
dt = get(out, 'doctitle')
dt = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + 'Masterfully Crafted Ocean View Estate in Tango Mar, ID CODE: #3751' + m.group(2), dt)
dt = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + 'Masterfully crafted ocean view estate in Tango Mar with a 3 bedroom main house, a 2 bedroom guest casita and a 5 x 15 m pool. US$1,200,000.' + m.group(2), dt)
dt = dt.replace('turn-key-ocean-view-estate/opt/4.jpg', 'turn-key-ocean-view-estate/opt/24.jpg')
out = put(out, 'doctitle', dt)
if 'Masterfully Crafted' not in out or 'whale-bay' in get(out, 'content'):
    print('Algo no se ve bien, no se cambio nada'); raise SystemExit
out = words(out)
shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(out)
print('LISTO: #3751 con el diseno nuevo https://www.propertiesincostarica.com/properties/nicoya_peninsula/for_sale/abundance.html')
