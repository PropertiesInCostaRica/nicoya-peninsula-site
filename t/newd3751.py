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
if 'hd--v2' in s or 'new_site.css' in s:
    print('Ya tiene el diseno nuevo'); raise SystemExit
if 'TnLrCVA42E3' not in s:
    print('Primero corre mp3751.py'); raise SystemExit
out = rd(SHELL)
for n in ['doctitle', 'head', 'title', 'code', 'price', 'features', 'content', 'hidden']:
    out = put(out, n, get(s, n))
if 'Masterfully Crafted' not in out or 'whale-bay' in get(out, 'content'):
    print('Algo no se ve bien, no se cambio nada'); raise SystemExit
shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(out)
print('LISTO: #3751 con el diseno nuevo https://www.propertiesincostarica.com/properties/nicoya_peninsula/for_sale/abundance.html')
