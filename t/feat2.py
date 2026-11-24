#!/usr/bin/env python3
# #3751 goes to the top as FEATURED on the Nicoya Peninsula and Tambor pages. Backup first.
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
CARD = r'(?:<!--#+INI#+-->\s*)?<article class="listing">(?:(?!</article>).)*?</article>(?:\s*<!--#+FIN#+-->)?'
w = lambda x: '<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->\n'
for rel, keep in [('nicoya_peninsula_real_estate.html', 1), ('tambor_real_estate.html', 1)]:
    p = W + rel
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    m = None
    for c in re.finditer(CARD, s, re.S):
        if 'for_sale/abundance.html' in c.group(0):
            m = c; break
    if not m:
        print(rel + ': no encontre #3751'); continue
    card = re.search(r'<article class="listing">.*</article>', m.group(0), re.S).group(0)
    s = s[:m.start()] + s[m.end():]
    sec = re.search(r'(<section class="featured_listing_of[^>]*>\s*<h2>.*?</h2>\s*)(.*?)(</section>)', s, re.S)
    inside = [re.search(r'<article class="listing">.*</article>', x.group(0), re.S).group(0) for x in re.finditer(CARD, sec.group(2), re.S)]
    stay, out = inside[:keep], inside[keep:]
    if rel == 'tambor_real_estate.html' and len(inside) >= 2:
        stay, out = inside[1:2], inside[:1] + inside[2:]
    rest = re.sub(CARD, '', sec.group(2), flags=re.S)
    new = sec.group(1) + w(card) + ''.join(w(x) for x in stay) + rest + sec.group(3) + '\n' + ''.join(w(x) for x in out)
    s = s[:sec.start()] + new + s[sec.end():]
    shutil.copy(p, '/root/respaldos/' + rel + '-' + TS)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    print(rel + ': #3751 destacada arriba')
print('LISTO')
