#!/usr/bin/env python3
# Change the banner (hero) photo of a new design page.  Usage: python3 hero.py <page> <image-url> "<alt>"
import re, sys, os, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
page, url, alt = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'Costa Rica'
p = W + page
s = open(p, encoding='utf-8', errors='surrogateescape').read()
m = re.search(r'(<section class="sp-hero"[^>]*>\s*<picture>\s*<img )([^>]*)(>)', s)
if not m: raise SystemExit('ERROR: no encontre el banner en ' + page)
a = m.group(2)
a = re.sub(r'src="[^"]*"', 'src="%s"' % url, a, 1)
a = re.sub(r'alt="[^"]*"', 'alt="%s"' % alt, a, 1)
a = re.sub(r'object-position:[^;"]*', 'object-position:center 55%', a)
B = '/root/respaldos/hero-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True); shutil.copy2(p, B + page.replace('/', '_'))
s = s[:m.start(2)] + a + s[m.end(2):]
open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('Banner cambiado en ' + page + '. LISTO')
