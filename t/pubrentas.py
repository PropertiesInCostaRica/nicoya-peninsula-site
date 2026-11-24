#!/usr/bin/env python3
# PUBLISH the 5 rental previews. Backup of each old page first.
import os, re, shutil, time, subprocess
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
for rel in ['vacation_rentals.html', 'long-term-rentals-furnished.html', 'long-term-rentals-unfurnished.html', 'long_term_rentals_2.html', 'luxury_rentals.htm']:
    live, n = W + rel, W + re.sub(r'\.(html?)$', r'-nuevo.\1', rel)
    if not os.path.exists(n):
        print(rel + ': no hay vista previa, se salta'); continue
    s = open(n, encoding='utf-8', errors='surrogateescape').read()
    s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
    if 'noindex' in s or '<article class="listing"' not in s or '</html>' not in s:
        print(rel + ': algo no se ve bien, NO se publico'); continue
    shutil.copy(live, '/root/respaldos/' + rel + '-' + TS)
    open(live, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    shutil.move(n, '/root/respaldos/' + os.path.basename(n) + '-publicada-' + TS)
    print('PUBLICADA: https://www.propertiesincostarica.com/' + rel)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO. Respaldos en /root/respaldos con la fecha ' + TS)
