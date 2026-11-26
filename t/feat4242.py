#!/usr/bin/env python3
# Tamarindo page: put #4242 first in FEATURED; the card it replaces moves to the top of the list
import re, shutil, time, os
W = '/var/www/propertiesincostarica.com/web/'
F = W + 'tamarindo-real-estate.html'
KEY = 'guanacaste/for_sale/modern-tropical-pool-home.html'
s = open(F, encoding='utf-8', errors='surrogateescape').read()
shutil.copy2(F, '/root/respaldos/tamarindo-real-estate.html.' + time.strftime('%Y%m%d%H%M'))
blk = re.compile(r'<!--#+INI#+-->\s*<article class="listing">.*?</article>\s*<!--#+FIN#+-->', re.S)
i = s.index('featured_listing_of'); a = s.rfind('<section', 0, i); e = s.index('</section>', i)
sec = s[a:e]
feat = [m for m in blk.finditer(sec)]
if any(KEY in m.group(0) for m in feat): raise SystemExit('Ya esta en Featured')
rest = s[e:]
m4 = next(m for m in blk.finditer(rest) if KEY in m.group(0))
card = m4.group(0)
rest = rest[:m4.start()] + rest[m4.end():]
out = feat[-1]   # second featured card goes down to the list
sec2 = sec[:out.start()] + sec[out.end():]
h = sec2.index('</h2>') + 5
sec2 = sec2[:h] + '\n\n' + card + sec2[h:]
j = rest.index('</section>') + len('</section>')
rest = rest[:j] + '\n' + out.group(0) + '\n' + rest[j:]
s = s[:a] + sec2 + rest
open(F, 'w', encoding='utf-8', errors='surrogateescape').write(s)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('Featured Tamarindo: #4242 primero. La tarjeta que salio de Featured quedo de primera en la lista.')
print('LISTO')
