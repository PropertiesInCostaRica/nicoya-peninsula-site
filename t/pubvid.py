#!/usr/bin/env python3
# Publish the new Videos page (videos/index-nuevo.html -> videos/index.html), with backup.
import shutil, subprocess, time, re
W = '/var/www/propertiesincostarica.com/web/videos/'
ts = time.strftime('%Y%m%d-%H%M%S')
new = open(W + 'index-nuevo.html', encoding='utf-8', errors='surrogateescape').read()
new = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
if 'sp-hero' not in new or 'noindex' in new:
    raise SystemExit('Algo no esta bien, no se cambio nada')
shutil.copy2(W + 'index.html', '/root/respaldos/videos-index-viejo-' + ts + '.html')
open(W + 'index.html', 'w', encoding='utf-8', errors='surrogateescape').write(new)
shutil.move(W + 'index-nuevo.html', '/root/respaldos/videos-index-nuevo-' + ts + '.html')
print('Videos publicada: https://www.propertiesincostarica.com/videos/index.html')
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
