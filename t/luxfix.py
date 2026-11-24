#!/usr/bin/env python3
# luxury_estates preview: removes the repeated "Sold!" line on the 2 sold cards.
import re, shutil, time
P = '/var/www/propertiesincostarica.com/web/luxury_estates_in_costa_rica-nuevo.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
tag = '<li><div class="sold">Sold! Looking for similar properties? <a href="/contact.html">Contact Us</a></div></li>'
n = [0]
def fix(m):
    c = m.group(0)
    if tag in c and c.replace(tag, '', 1).count('Sold!') >= 1:
        n[0] += 1
        return c.replace(tag, '', 1)
    return c
s2 = re.sub(r'<article class="listing".*?</article>', fix, s, flags=re.S)
shutil.copy(P, '/root/respaldos/luxury_estates_in_costa_rica-nuevo.html-' + time.strftime('%Y%m%d-%H%M%S'))
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
print('Arregladas: %d. LISTO' % n[0])
