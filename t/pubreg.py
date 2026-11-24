#!/usr/bin/env python3
# Banner = Hacienda Pinilla villa #4012, then PUBLISH region_and_price/index-nuevo.html as index.html (backup first).
import os, re, shutil, time, subprocess
W = '/var/www/propertiesincostarica.com/web/region_and_price/'
TS = time.strftime('%Y%m%d-%H%M%S')
n, live = W + 'index-nuevo.html', W + 'index.html'
if not os.path.exists(n):
    print('No existe la vista previa, no se cambio nada'); raise SystemExit
s = open(n, encoding='utf-8', errors='surrogateescape').read()
pic = ('<picture><img src="https://cdn.propertiesincostarica.com/properties/Images/turnkey-beach-villa/opt/photo-15.jpg" alt="Hacienda Pinilla villa with pool at dusk" '
       'width="1200" height="800" fetchpriority="high" decoding="async" style="object-fit:cover;object-position:center 60%"></picture>')
s = re.sub(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, s, count=1, flags=re.S)
s = s.replace('.sp-hero picture img{filter:brightness(.9) saturate(1.1)}', '.sp-hero picture img{filter:brightness(1.05) saturate(1.1)}')
s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
if 'noindex' in s or 'rp-card' not in s or '</html>' not in s or 'turnkey-beach-villa' not in s:
    print('Algo no se ve bien, no se publico'); raise SystemExit
shutil.copy(live, '/root/respaldos/region_and_price_index.html-' + TS)
open(live, 'w', encoding='utf-8', errors='surrogateescape').write(s)
shutil.move(n, '/root/respaldos/region_and_price_index-nuevo.html-publicada-' + TS)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('PUBLICADA: https://www.propertiesincostarica.com/region_and_price/index.html  (respaldo con fecha ' + TS + ')')
