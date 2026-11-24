#!/usr/bin/env python3
# caribbean-nuevo.html (PREVIEW only): same format as Beach page.
# 2 featured cards on top, the rest as the smaller list. Square area buttons. Removes repeated area button.
import re, shutil, time
p = '/var/www/propertiesincostarica.com/web/caribbean-nuevo.html'
s = open(p, encoding='utf-8', errors='surrogateescape').read()
shutil.copy(p, '/root/respaldos/caribbean-nuevo.html-' + time.strftime('%Y%m%d-%H%M%S'))
m = re.search(r'<section class="featured_listing_of titulo_categoria" id="gotoProperties">.*?</section>\n?', s, flags=re.S)
if not m:
    print('No encontre la seccion, no se cambio nada'); raise SystemExit
cards = re.findall(r'<article class="listing".*?</article>', m.group(0), flags=re.S)
w = lambda x: '<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->'
new = ('<section class="featured_listing_of titulo_categoria" id="gotoProperties">\n'
       '<h2><a name="properties_of_the_month" id="properties_of_the_month"></a>Featured Caribbean Properties of the Month</h2>\n'
       + '\n'.join(w(x) for x in cards[:2]) + '\n</section>\n'
       + '\n'.join(w(x) for x in cards[2:]) + '\n')
s = s[:m.start()] + new + s[m.end():]
# repeated area button
pm = re.search(r'<div class="car-areas">.*?</div>', s, flags=re.S)
if pm:
    seen = set(); out = []
    for a in re.findall(r'<a href="[^"]+">[^<]*</a>', pm.group(0)):
        h = re.search(r'href="([^"]+)"', a).group(1)
        if h not in seen:
            seen.add(h); out.append(a)
    s = s[:pm.start()] + '<div class="car-areas"><span>Explore by area:</span>' + ''.join(out) + '</div>' + s[pm.end():]
s = s.replace('border-radius:20px;padding:6px 14px', 'border-radius:3px;padding:8px 14px')
open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Destacadas: 2, lista: %d' % (len(cards) - 2))
print('LISTO: https://www.propertiesincostarica.com/caribbean-nuevo.html')
