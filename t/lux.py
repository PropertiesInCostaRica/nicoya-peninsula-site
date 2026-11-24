#!/usr/bin/env python3
# luxury_rentals-nuevo.htm (PREVIEW): adds The Ultimate Event Beachfront Estate at Tambor as first featured rental.
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
P = W + 'luxury_rentals-nuevo.htm'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
if 'tambor/for_rent/ultimate-estate.html' in s:
    print('Ya estaba'); raise SystemExit
src = open(W + 'long_term_rentals.html', encoding='utf-8', errors='surrogateescape').read()
m = re.search(r'<article class="listing"(?:(?!</article>).)*?tambor/for_rent/ultimate-estate\.html(?:(?!</article>).)*?</article>', src, re.S)
if not m:
    print('No encontre la tarjeta, no se cambio nada'); raise SystemExit
shutil.copy(P, '/root/respaldos/luxury_rentals-nuevo.htm-' + time.strftime('%Y%m%d-%H%M%S'))
w = lambda x: '<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->'
sec = re.search(r'(<section class="featured_listing_of titulo_categoria" id="gotoProperties">\s*<h2>[^<]*</h2>\s*)(.*?)(</section>\n?)', s, re.S)
cards = re.findall(r'<article class="listing".*?</article>', sec.group(2), re.S)
new = sec.group(1) + w(m.group(0)) + '\n' + w(cards[0]) + '\n' + sec.group(3) + '\n'.join(w(x) for x in cards[1:]) + '\n'
s = s[:sec.start()] + new + s[sec.end():]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Agregada como primera destacada. LISTO: https://www.propertiesincostarica.com/luxury_rentals-nuevo.htm')
