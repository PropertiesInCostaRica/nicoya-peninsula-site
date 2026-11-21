#!/usr/bin/env python3
# Add the Whale Bay Villa card at the top of homes/ocean_view_homes.html
import re, glob, shutil, subprocess, time
W = '/var/www/propertiesincostarica.com/web/'
P = W + 'homes/ocean_view_homes.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
if 'whale-bay-villa' in s:
    raise SystemExit('Ya estaba, no se cambio nada')
art = re.compile(r'(<!--[^>]*INI[^>]*-->\s*)?<article class="listing".*?</article>(\s*<!--[^>]*FIN[^>]*-->)?', re.S)
card = None
for f in sorted(glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*')):
    if f == P or 'whale-bay-villa.html' in f:
        continue
    t = open(f, encoding='utf-8', errors='surrogateescape').read()
    for m in art.finditer(t):
        if 'whale-bay-villa.html' in m.group(0):
            card = m.group(0); src = f; break
    if card:
        break
if not card:
    raise SystemExit('No encontre la tarjeta de Whale Bay')
first = art.search(s)
if not first:
    raise SystemExit('No encontre tarjetas en la pagina')
# make relative links absolute so they work from /homes/
card = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:)', r'\1="/', card)
indent = s[s.rfind('\n', 0, first.start()) + 1:first.start()]
bk = '/root/respaldos/ocean_view_homes-' + time.strftime('%Y%m%d-%H%M%S') + '.html'
shutil.copy2(P, bk)
s2 = s[:first.start()] + card + '\n' + indent + s[first.start():]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
print('Tarjeta copiada de: ' + src)
print('Tarjetas ahora: %d' % len(re.findall(r'<article class="listing"', s2)))
print('Respaldo: ' + bk)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
