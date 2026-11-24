#!/usr/bin/env python3
# PUBLISH long_term_rentals-nuevo.html as long_term_rentals.html (backup of the old page first).
import os, re, shutil, time, subprocess
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
n, live = W + 'long_term_rentals-nuevo.html', W + 'long_term_rentals.html'
if not os.path.exists(n):
    print('No existe la vista previa, no se cambio nada'); raise SystemExit
s = open(n, encoding='utf-8', errors='surrogateescape').read()
s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
if 'noindex' in s or s.count('<article class="listing"') < 50 or '</html>' not in s:
    print('Algo no se ve bien, no se publico'); raise SystemExit
shutil.copy(live, '/root/respaldos/long_term_rentals.html-' + TS)
open(live, 'w', encoding='utf-8', errors='surrogateescape').write(s)
shutil.move(n, '/root/respaldos/long_term_rentals-nuevo.html-publicada-' + TS)
print('Respaldo: /root/respaldos/long_term_rentals.html-' + TS)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('PUBLICADA: https://www.propertiesincostarica.com/long_term_rentals.html')
