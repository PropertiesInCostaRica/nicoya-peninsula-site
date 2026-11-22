#!/usr/bin/env python3
# Publish the new All Listings page with a Palacio Tropical (Tambor Oceanfront Estate) banner photo, with backup.
import shutil, subprocess, time, re
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
new = open(W + 'listings-nuevo.html', encoding='utf-8', errors='surrogateescape').read()
IMG = 'https://cdn.propertiesincostarica.com/properties/Images/palacio-tropical/opt2/photo-1.jpg'
pic = ('<picture><img src="' + IMG + '" alt="" width="1672" height="941" fetchpriority="high" decoding="async" '
       'style="object-fit:cover;object-position:center 55%"></picture>')
new, n = re.subn(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, new, count=1, flags=re.S)
new = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
if not n or 'lst-feat' not in new or 'noindex' in new:
    raise SystemExit('Algo no esta bien, no se cambio nada')
shutil.copy2(W + 'listings.html', '/root/respaldos/listings-viejo-' + ts + '.html')
open(W + 'listings.html', 'w', encoding='utf-8', errors='surrogateescape').write(new)
shutil.move(W + 'listings-nuevo.html', '/root/respaldos/listings-nuevo-' + ts + '.html')
print('Listings publicada con foto de Palacio Tropical: https://www.propertiesincostarica.com/listings.html')
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
