#!/usr/bin/env python3
# #3751: pool views first, contact line ends at "Klaudia Nabialek", video removed, no two photo rows in a row. Backup first.
import re, shutil, time
P = '/var/www/propertiesincostarica.com/web/properties/nicoya_peninsula/for_sale/abundance.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
s = s.replace('contact Klaudia Nabialek with Properties in Costa Rica on WhatsApp at +506 8629 3756.', 'contact Klaudia Nabialek.')
s = re.sub(r'\s*<iframe id="video".*?</iframe>', '', s, flags=re.S)
s = re.sub(r'\s*<a class="sold" href="#video">Watch video</a>', '', s)
# pool views first: photos 24, 25 and 11 open the gallery
POOL = ['24', '25', '11']
anch = {}
for n in POOL:
    m = re.search(r'\s*<a href="[^"]*/turn-key-ocean-view-estate/opt/' + n + r'\.jpg">.*?</a>', s, re.S)
    if m:
        anch[n] = m.group(0).strip()
        s = s[:m.start()] + s[m.end():]
if anch:
    s = s.replace('<p class="photo">', '<p class="photo">\n' + '\n'.join(anch[n] for n in POOL if n in anch), 1)
# join photo rows that are right next to each other into one row
def join(m):
    a, b = m.group(1), m.group(2)
    return '<p class="photo">' + a.rstrip() + '\n' + b.strip() + '\n</p>'
n = 1
while n:
    s, n = re.subn(r'<p class="photo">((?:(?!</p>).)*?)</p>\s*<p class="photo">((?:(?!</p>).)*?)</p>', join, s, flags=re.S)
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('LISTO: https://www.propertiesincostarica.com/properties/nicoya_peninsula/for_sale/abundance.html')
