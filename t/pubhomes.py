#!/usr/bin/env python3
# PUBLISH homes-nuevo.html as homes.html (backup of the old page first).
import os, re, shutil, time, subprocess
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
n, live = W + 'homes-nuevo.html', W + 'homes.html'
if not os.path.exists(n):
    print('No existe la vista previa, no se cambio nada'); raise SystemExit
s = open(n, encoding='utf-8', errors='surrogateescape').read()
s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
if 'noindex' in s or s.count('<article class="listing"') < 50 or '</html>' not in s:
    print('Algo no se ve bien, no se publico'); raise SystemExit
shutil.copy(live, '/root/respaldos/homes.html-' + TS)
open(live, 'w', encoding='utf-8', errors='surrogateescape').write(s)
shutil.move(n, '/root/respaldos/homes-nuevo.html-publicada-' + TS)
print('Respaldo: /root/respaldos/homes.html-' + TS)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('PUBLICADA: https://www.propertiesincostarica.com/homes.html')
