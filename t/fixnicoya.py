#!/usr/bin/env python3
# Nicoya page: new travel sentence (faster now, ferries and Cobano airport) and spacing fix. Backup first.
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
F = W + 'nicoya_peninsula_real_estate.html'
s = open(F, encoding='utf-8', errors='surrogateescape').read()
pat = r"It\s+normally\s+takes\s+longer\s+to\s+travel\s+to\s+the\s+Southern\s+Nicoya\s+Peninsula\s+than\s+to\s+other\s+parts\s+of\s+Costa\s+Rica,\s+but\s+it\s+doesn.t\s+matter\s+since\s+the\s+area\s+has"
new = "Getting to the Southern Nicoya Peninsula is now quicker than to many other parts of Costa Rica, with the Paquera and Naranjo ferries and short flights to C&oacute;bano airport, and the area has"
s2, n = re.subn(pat, new, s, count=1)
s2 = s2.replace('Paquera,<a href="https://www.propertiesincostarica.com/naranjo_real_estate.html">', 'Paquera, <a href="https://www.propertiesincostarica.com/naranjo_real_estate.html">')
s2 = s2.replace('Naranjo</a>,<a href="https://www.propertiesincostarica.com/samara_real_estate.html">', 'Naranjo</a>, <a href="https://www.propertiesincostarica.com/samara_real_estate.html">')
if not n: raise SystemExit('No encontre la frase')
B = '/root/respaldos/nicoya_peninsula_real_estate-' + time.strftime('%Y%m%d%H%M%S') + '.html'
shutil.copy2(F, B)
open(F, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
print('LISTO. Frase corregida. Respaldo: ' + B)
