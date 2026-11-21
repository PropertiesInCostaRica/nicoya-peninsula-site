#!/usr/bin/env python3
# long_term_rentals.html: swap River Park (#4237) and Lavish Beach & Golf (#3760) cards
import re, shutil, subprocess, time
P = '/var/www/propertiesincostarica.com/web/long_term_rentals.html'
A = 'santa_ana/for_rent/spacious-condo.html'
B = 'tambor/for_rent/lavish-vacation-rental.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
art = re.compile(r'(<!--[^>]*INI[^>]*-->\s*)?<article class="listing".*?</article>(\s*<!--[^>]*FIN[^>]*-->)?', re.S)
ms = list(art.finditer(s))
ia = [i for i, m in enumerate(ms) if A in m.group(0)]
ib = [i for i, m in enumerate(ms) if B in m.group(0)]
if len(ia) != 1 or len(ib) != 1:
    raise SystemExit('No encontre cada tarjeta una sola vez, no se cambio nada (%d, %d)' % (len(ia), len(ib)))
a, b = sorted([ms[ia[0]], ms[ib[0]]], key=lambda m: m.start())
s2 = s[:a.start()] + b.group(0) + s[a.end():b.start()] + a.group(0) + s[b.end():]
bk = '/root/respaldos/long_term_rentals-' + time.strftime('%Y%m%d-%H%M%S') + '.html'
shutil.copy2(P, bk)
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
order = [i for i, m in enumerate(art.finditer(s2)) if A in m.group(0) or B in m.group(0)]
print('Posiciones ahora (Lavish, River Park):', [i + 1 for i in order])
print('Respaldo: ' + bk)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
