#!/usr/bin/env python3
# mountain-nuevo.html: banner = Atenas #3902 mountain and pool view (photo 20), then PUBLISH as mountain.html (backup first).
import os, re, shutil, time, subprocess
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
n, live = W + 'mountain-nuevo.html', W + 'mountain.html'
if not os.path.exists(n):
    print('No existe la vista previa, no se cambio nada'); raise SystemExit
s = open(n, encoding='utf-8', errors='surrogateescape').read()
pic = ('<picture><img src="https://cdn.propertiesincostarica.com/properties/Images/family-estate/opt/20.jpg" alt="Atenas mountain view home with pool" '
       'width="1326" height="892" fetchpriority="high" decoding="async" style="object-fit:cover;object-position:center 45%"></picture>')
s = re.sub(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, s, count=1, flags=re.S)
s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
if 'noindex' in s or s.count('<article class="listing"') < 50 or '</html>' not in s or 'family-estate/opt/20.jpg' not in s:
    print('Algo no se ve bien, no se publico'); raise SystemExit
shutil.copy(live, '/root/respaldos/mountain.html-' + TS)
open(live, 'w', encoding='utf-8', errors='surrogateescape').write(s)
shutil.move(n, '/root/respaldos/mountain-nuevo.html-publicada-' + TS)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('PUBLICADA: https://www.propertiesincostarica.com/mountain.html  (respaldo: /root/respaldos/mountain.html-' + TS + ')')
