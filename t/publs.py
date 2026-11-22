#!/usr/bin/env python3
# Publish the new Links and San Jose Attractions pages, with backups.
import shutil, subprocess, time, re, os
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
for prev, live in [('links-nuevo.html', 'links.html'), ('info/sanjose-nuevo.html', 'info/sanjose.html')]:
    if not os.path.exists(W + prev):
        print(live + ': no hay vista previa'); continue
    new = open(W + prev, encoding='utf-8', errors='surrogateescape').read()
    new = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
    if 'sp-hero' not in new or 'noindex' in new:
        print(live + ': algo no esta bien, no se cambio'); continue
    shutil.copy2(W + live, '/root/respaldos/' + live.replace('/', '__') + '-viejo-' + ts)
    open(W + live, 'w', encoding='utf-8', errors='surrogateescape').write(new)
    shutil.move(W + prev, '/root/respaldos/' + prev.replace('/', '__') + '-' + ts)
    print('Publicada: https://www.propertiesincostarica.com/' + live)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
