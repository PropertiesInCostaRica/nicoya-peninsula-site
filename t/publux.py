#!/usr/bin/env python3
# Removes the repeated "Sold!" line, then PUBLISHES luxury_estates_in_costa_rica-nuevo.html (backup of the old page first).
import os, re, shutil, time, subprocess
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
n, live = W + 'luxury_estates_in_costa_rica-nuevo.html', W + 'luxury_estates_in_costa_rica.html'
if not os.path.exists(n):
    print('No existe la vista previa, no se cambio nada'); raise SystemExit
s = open(n, encoding='utf-8', errors='surrogateescape').read()
tag = '<li><div class="sold">Sold! Looking for similar properties? <a href="/contact.html">Contact Us</a></div></li>'
def fix(m):
    c = m.group(0)
    if tag in c and c.replace(tag, '', 1).count('Sold!') >= 1:
        return c.replace(tag, '', 1)
    return c
s = re.sub(r'<article class="listing".*?</article>', fix, s, flags=re.S)
s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
if 'noindex' in s or s.count('<article class="listing"') < 30 or '</html>' not in s:
    print('Algo no se ve bien, no se publico'); raise SystemExit
shutil.copy(live, '/root/respaldos/luxury_estates_in_costa_rica.html-' + TS)
open(live, 'w', encoding='utf-8', errors='surrogateescape').write(s)
shutil.move(n, '/root/respaldos/luxury_estates_in_costa_rica-nuevo.html-publicada-' + TS)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('PUBLICADA: https://www.propertiesincostarica.com/luxury_estates_in_costa_rica.html  (respaldo con fecha ' + TS + ')')
