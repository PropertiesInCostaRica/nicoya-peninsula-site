#!/usr/bin/env python3
# Add the Whale Bay Villa card at the top of the ocean view, sea side and ocean front pages
import re, glob, shutil, subprocess, time
W = '/var/www/propertiesincostarica.com/web/'
PAGES = [W + 'homes/ocean_view_homes.html', W + 'homes/sea_side_homes.html', W + 'homes/ocean_front_homes.html']
art = re.compile(r'(<!--[^>]*INI[^>]*-->\s*)?<article class="listing".*?</article>(\s*<!--[^>]*FIN[^>]*-->)?', re.S)
card = None
for f in sorted(glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*')):
    if f in PAGES or 'whale-bay-villa.html' in f:
        continue
    t = open(f, encoding='utf-8', errors='surrogateescape').read()
    for m in art.finditer(t):
        if 'whale-bay-villa.html' in m.group(0):
            card = m.group(0); src = f; break
    if card:
        break
if not card:
    raise SystemExit('No encontre la tarjeta de Whale Bay')
print('Tarjeta copiada de: ' + src)
card = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:)', r'\1="/', card)
for P in PAGES:
    name = P.split('/')[-1]
    s = open(P, encoding='utf-8', errors='surrogateescape').read()
    if 'whale-bay-villa.html' in s:
        print(name + ': ya estaba'); continue
    first = art.search(s)
    if not first:
        print(name + ': sin tarjetas, no se cambio'); continue
    indent = s[s.rfind('\n', 0, first.start()) + 1:first.start()]
    bk = '/root/respaldos/' + name + '-' + time.strftime('%Y%m%d-%H%M%S')
    shutil.copy2(P, bk)
    s2 = s[:first.start()] + card + '\n' + indent + s[first.start():]
    open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
    print('%s: agregada, tarjetas ahora %d' % (name, len(re.findall(r'<article class="listing"', s2))))
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
