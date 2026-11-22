#!/usr/bin/env python3
# Publish the new Seller Financing page (financing-nuevo.html -> financing.html), with backup.
import shutil, subprocess, time, re
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
new = open(W + 'financing-nuevo.html', encoding='utf-8', errors='surrogateescape').read()
new2 = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
if 'sp-hero' not in new2 or 'noindex' in new2:
    raise SystemExit('Algo no esta bien, no se cambio nada')
shutil.copy2(W + 'financing.html', '/root/respaldos/financing-viejo-' + ts + '.html')
open(W + 'financing.html', 'w', encoding='utf-8', errors='surrogateescape').write(new2)
shutil.move(W + 'financing-nuevo.html', '/root/respaldos/financing-nuevo-' + ts + '.html')
print('Seller Financing publicada: https://www.propertiesincostarica.com/financing.html')
print('Respaldo de la pagina vieja: /root/respaldos/financing-viejo-' + ts + '.html')
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
