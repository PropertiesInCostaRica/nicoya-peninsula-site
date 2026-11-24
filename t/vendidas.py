#!/usr/bin/env python3
# Puts SOLD / RENTED listings back at the BOTTOM of the pages redesigned today.
# Takes the cards from the old page backups in /root/respaldos. Backup of each page first.
import os, re, glob, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
R = '/root/respaldos/'
TS = time.strftime('%Y%m%d-%H%M%S')
bk = R + 'vendidas-' + TS + '/'
os.makedirs(bk)
SALE = ['caribbean.html', 'puerto-viejo-real-estate.html', 'cocles-chiquita-real-estate.html', 'manzanillo-real-estate.html',
        'cahuita-real-estate.html', 'hone-creek-carbon.html', 'tortuguero-real-estate.html', 'guapiles-real-estate.html',
        'homes.html', 'mountain.html']
RENT = ['long_term_rentals.html', 'vacation_rentals.html', 'long-term-rentals-furnished.html',
        'long-term-rentals-unfurnished.html', 'long_term_rentals_2.html', 'luxury_rentals.htm']
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def cards(s): return [c for c in re.findall(r'<article class="listing".*?</article>', s, re.S) if 'href=' in c]
def href(c): return re.search(r'href="([^"?#]+)', c).group(1)
def old_page(rel):
    best = None
    for f in sorted(glob.glob(R + rel + '-2*')):
        if '-nuevo' in f or not os.path.isfile(f): continue
        t = rd(f)
        if 'car-css' in t: continue
        best = t
    return best
for rel in SALE + RENT:
    p = W + rel
    if not os.path.exists(p):
        print(rel + ': no existe'); continue
    old = old_page(rel)
    if not old:
        print(rel + ': no encontre respaldo viejo, se salta'); continue
    s = rd(p)
    if 'car-css' not in s:
        print(rel + ': no tiene el diseno nuevo, se salta'); continue
    have = set(href(c) for c in cards(s))
    gone = [c for c in cards(old) if href(c) not in have]
    if not gone:
        print(rel + ': 0 para agregar'); continue
    word = 'Rented!' if rel in RENT else 'Sold!'
    tag = '<li><div class="sold">' + word + ' Looking for similar properties? <a href="/contact.html">Contact Us</a></div></li>'
    out = []
    for c in gone:
        if not re.search(r'Sold!|Rented!|>\s*SOLD\b|>\s*RENTED\b', c):
            c2, n = re.subn(r'<li>(?:(?!</li>).)*?Price(?:(?!</li>).)*?</li>', tag, c, count=1, flags=re.S)
            c = c2 if n else re.sub(r'(<ul>)', lambda m: m.group(1) + tag, c, count=1)
        out.append('<!--###################INI#####################-->\n' + c + '\n<!--###################FIN#####################-->')
    i = s.rfind('</article>')
    j = s.find('<!--###################FIN', i)
    i = s.find('-->', j) + 3 if 0 < j < i + 40 else i + 10
    shutil.copy(p, bk + rel)
    s = s[:i] + '\n' + '\n'.join(out) + s[i:]
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    print('%s: %d al final (%s)' % (rel, len(gone), word))
print('LISTO. Respaldo en ' + bk)
