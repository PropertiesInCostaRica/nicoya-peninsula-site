#!/usr/bin/env python3
# Publish the new FAQ page (faq-nuevo.html -> faq.html), with backup.
import shutil, subprocess, time, re
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
new = open(W + 'faq-nuevo.html', encoding='utf-8', errors='surrogateescape').read()
new2 = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
if 'sp-hero' not in new2 or 'noindex' in new2 or new2.count('<details>') < 20:
    raise SystemExit('Algo no esta bien, no se cambio nada')
shutil.copy2(W + 'faq.html', '/root/respaldos/faq-viejo-' + ts + '.html')
open(W + 'faq.html', 'w', encoding='utf-8', errors='surrogateescape').write(new2)
shutil.move(W + 'faq-nuevo.html', '/root/respaldos/faq-nuevo-' + ts + '.html')
print('FAQ publicada: https://www.propertiesincostarica.com/faq.html')
print('Preguntas: %d' % new2.count('<details>'))
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
