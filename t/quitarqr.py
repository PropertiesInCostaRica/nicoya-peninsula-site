#!/usr/bin/env python3
# Remove the QR code from the footer of every page (and the Dreamweaver templates). Backup of each changed file.
import os, re, time, tarfile
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
QR = re.compile(r'\s*<div id="qr">\s*<img[^>]*qr\.jpg[^>]*>\s*</div>', re.I)
changed = []
for root, dirs, files in os.walk(W):
    dirs[:] = [d for d in dirs if d not in ('blog', 'Images', 'images', '.git', 'cgi', 'css', 'js')]
    for f in files:
        if not re.search(r'\.(html?|dwt)$', f): continue
        p = os.path.join(root, f)
        try: s = open(p, encoding='utf-8', errors='surrogateescape').read()
        except Exception: continue
        if 'qr.jpg' not in s: continue
        s2 = QR.sub('', s)
        if s2 != s:
            changed.append((p, s, s2))
bk = '/root/respaldos/qr-' + ts + '.tgz'
with tarfile.open(bk, 'w:gz') as t:
    for p, _, _ in changed: t.add(p, arcname=p[len(W):])
for p, _, s2 in changed:
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
print('Paginas sin QR ahora: %d' % len(changed))
print('Plantillas incluidas: %d' % sum(1 for p, _, _ in changed if p.endswith('.dwt')))
print('Respaldo de todas: ' + bk)
import subprocess; subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
