#!/usr/bin/env python3
# Publish the new Residential Lots page (residential_lots-nuevo.html -> residential_lots.html), with backup.
import shutil, subprocess, time, re
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
new = open(W + 'residential_lots-nuevo.html', encoding='utf-8', errors='surrogateescape').read()
new2 = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
if 'sp-hero' not in new2 or 'noindex' in new2 or new2.count('<article class="listing"') < 100:
    raise SystemExit('Algo no esta bien, no se cambio nada')
shutil.copy2(W + 'residential_lots.html', '/root/respaldos/residential_lots-viejo-' + ts + '.html')
open(W + 'residential_lots.html', 'w', encoding='utf-8', errors='surrogateescape').write(new2)
shutil.move(W + 'residential_lots-nuevo.html', '/root/respaldos/residential_lots-nuevo-' + ts + '.html')
print('Residential Lots publicada: https://www.propertiesincostarica.com/residential_lots.html')
print('Propiedades: %d' % new2.count('<article class="listing"'))
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
