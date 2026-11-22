#!/usr/bin/env python3
# Publish the new Articles page (articles/index-nuevo.htm -> articles/index.htm), with backup.
import shutil, subprocess, time, re
W = '/var/www/propertiesincostarica.com/web/articles/'
ts = time.strftime('%Y%m%d-%H%M%S')
new = open(W + 'index-nuevo.htm', encoding='utf-8', errors='surrogateescape').read()
new2 = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
if 'sp-hero' not in new2 or 'noindex' in new2 or 'whose-name-property-title' not in new2:
    raise SystemExit('Algo no esta bien, no se cambio nada')
shutil.copy2(W + 'index.htm', '/root/respaldos/articles-index-viejo-' + ts + '.htm')
open(W + 'index.htm', 'w', encoding='utf-8', errors='surrogateescape').write(new2)
shutil.move(W + 'index-nuevo.htm', '/root/respaldos/articles-index-nuevo-' + ts + '.htm')
print('Articles publicada: https://www.propertiesincostarica.com/articles/index.htm')
print('Respaldo de la pagina vieja: /root/respaldos/articles-index-viejo-' + ts + '.htm')
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
