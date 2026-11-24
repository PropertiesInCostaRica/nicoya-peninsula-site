#!/usr/bin/env python3
# PUBLISH the 7 Caribbean area previews (-nuevo.html). Backup of each old page first.
# Also removes "More listings will be added soon" from Tortuguero.
import os, re, shutil, time, subprocess
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
PAGES = ['puerto-viejo-real-estate.html', 'cocles-chiquita-real-estate.html', 'manzanillo-real-estate.html',
         'cahuita-real-estate.html', 'hone-creek-carbon.html', 'tortuguero-real-estate.html', 'guapiles-real-estate.html']
for rel in PAGES:
    live, n = W + rel, W + rel.replace('.html', '-nuevo.html')
    if not os.path.exists(n):
        print(rel + ': no hay vista previa, se salta'); continue
    s = open(n, encoding='utf-8', errors='surrogateescape').read()
    s = re.sub(r'<p[^>]*>\s*<strong>\s*More listings will be added soon.*?</p>\s*', '', s, flags=re.S)
    s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
    if 'noindex' in s or '<article class="listing"' not in s or '</html>' not in s:
        print(rel + ': algo no se ve bien, NO se publico'); continue
    shutil.copy(live, '/root/respaldos/' + rel + '-' + TS)
    open(live, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    shutil.move(n, '/root/respaldos/' + rel.replace('.html', '-nuevo.html') + '-publicada-' + TS)
    print('PUBLICADA: https://www.propertiesincostarica.com/' + rel)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO. Respaldos en /root/respaldos con la fecha ' + TS)
