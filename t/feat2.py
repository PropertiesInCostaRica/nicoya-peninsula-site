#!/usr/bin/env python3
# FEATURED on the Nicoya Peninsula and Tambor pages: #3751 and Casa Leon del Mar (#4228).
# The cards that were featured before move to the top of the list. Backup first.
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
CARD = r'(?:<!--#+INI#+-->\s*)?<article class="listing">(?:(?!</article>).)*?</article>(?:\s*<!--#+FIN#+-->)?'
w = lambda x: '<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->\n'
inner = lambda x: re.search(r'<article class="listing">.*</article>', x, re.S).group(0)
WANT = ['for_sale/abundance.html', 'for_sale/ocean-setting.html']
for rel in ['nicoya_peninsula_real_estate.html', 'tambor_real_estate.html']:
    p = W + rel
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    got = {}
    for key in WANT:
        for c in re.finditer(CARD, s, re.S):
            if key in c.group(0):
                got[key] = inner(c.group(0))
                s = s[:c.start()] + s[c.end():]
                break
    if len(got) < 2:
        print(rel + ': no encontre las dos tarjetas, sin cambio'); continue
    sec = re.search(r'(<section class="featured_listing_of[^>]*>\s*<h2>.*?</h2>\s*)(.*?)(</section>)', s, re.S)
    before = [inner(x.group(0)) for x in re.finditer(CARD, sec.group(2), re.S)]
    rest = re.sub(CARD, '', sec.group(2), flags=re.S)
    low = [x for x in before if 'free-standing-bungalow' in x]
    before = [x for x in before if 'free-standing-bungalow' not in x]
    new = sec.group(1) + w(got[WANT[0]]) + w(got[WANT[1]]) + rest + sec.group(3) + '\n' + ''.join(w(x) for x in before)
    s = s[:sec.start()] + new + s[sec.end():]
    if low:
        # Casa Mango goes lower: last available card, before the sold ones
        pos = None
        for c in re.finditer(CARD, s, re.S):
            if c.start() > sec.start() and re.search(r'Sold!|SOLD|Under Contract', c.group(0)):
                pos = c.start(); break
        if pos is None:
            ce = s.index('<!-- InstanceEndEditable -->', s.index('<!-- InstanceBeginEditable name="content" -->'))
            pos = s.rfind('</article>', 0, ce)
            pos = s.find('-->', s.find('<!--', pos)) + 3 if s.find('<!--#', pos) != -1 and s.find('<!--#', pos) < ce else pos + 10
        s = s[:pos] + w(low[0]) + s[pos:]
        print(rel + ': Casa Mango mas abajo')
    shutil.copy(p, '/root/respaldos/' + rel + '-' + TS)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    print(rel + ': destacadas #3751 y Casa Leon del Mar')
print('LISTO')
