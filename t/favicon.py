#!/usr/bin/env python3
# Install the new PCR favicon (option C) on the website. Backup of the old one first.
import urllib.request, shutil, os, time
W = '/var/www/propertiesincostarica.com/web/'
B = 'https://www.properties-in-costa-rica.com/t/fav/'
ts = time.strftime('%Y%m%d-%H%M%S')
bk = '/root/respaldos/favicon-' + ts + '/'
os.makedirs(bk, exist_ok=True)
for f in ['favicon.png', 'favicon.ico', 'apple-touch-icon.png', 'favicon-192.png', 'favicon-512.png']:
    if os.path.exists(W + f): shutil.copy2(W + f, bk + f)
    data = urllib.request.urlopen(B + f).read()
    open(W + f, 'wb').write(data)
    st = os.stat(W + 'index.html'); os.chown(W + f, st.st_uid, st.st_gid); os.chmod(W + f, 0o644)
    print('Instalado: %s (%d bytes)' % (f, len(data)))
for i in (1, 2, 3):
    p = W + 'favicon-ver-%d.ico' % i
    if os.path.exists(p): shutil.move(p, bk + os.path.basename(p))
print('Copias temporales quitadas. Respaldo del favicon viejo en ' + bk)
print('LISTO')
