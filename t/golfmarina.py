#!/usr/bin/env python3
# PREVIEW homes/ocean_front_homes-nuevo.html (noindex), new design. Live page NOT changed.
# Run AFTER feat2.py. Featured: the 2 cards in the page's featured section. Sold cards go to the bottom.
import re, os
W = '/var/www/propertiesincostarica.com/web/'
REL = 'golf_marina.html'
INTRO = 'Homes, villas and lots in Costa Rica\'s golf and marina communities, from Los Delfines in Tambor to Reserva Conchal, Hacienda Pinilla, Flamingo and Los Sue&ntilde;os.'
ADD = []
FALLBACK = 'https://cdn.propertiesincostarica.com/properties/Images/investment-villa/opt/photo-1.jpg'
CSS = ('<style id="car-css">.sp-hero picture img{filter:brightness(.95) saturate(1.1)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 1px 3px rgba(0,0,0,.9),0 2px 12px rgba(0,0,0,.7)}'
       '.car-more{clear:both;margin-top:30px}</style>\n')
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def region(s, n):
    a = s.find('<!-- InstanceBeginEditable name="%s" -->' % n)
    if a < 0:
        a = s.find('<!-- #BeginEditable "%s" -->' % n)
        if a < 0: return None
        a = s.index('-->', a) + 3
        e = s.find('<!-- #EndEditable -->', a)
        return s[a:e] if e > 0 else None
    a = s.index('-->', a) + 3
    e = s.find('<!-- InstanceEndEditable -->', a)
    return s[a:e] if e > 0 else None
def put(s, n, val):
    a = s.index('<!-- InstanceBeginEditable name="%s" -->' % n)
    a = s.index('-->', a) + 3
    e = s.index('<!-- InstanceEndEditable -->', a)
    return s[:a] + val + s[e:]
def page_of(card):
    m = re.search(r'href="(?:https?://www\.propertiesincostarica\.com)?(?:\.\./|/)?(properties/[^"?#]+\.html?)', card)
    if not m: return None
    f = W + m.group(1)
    return rd(f) if os.path.exists(f) else None
def gone(card):
    if re.search(r'>\s*(SOLD|RENTED)\b', card): return True
    t = page_of(card)
    if not t: return False
    pr = region(t, 'price') or ''
    return bool(re.search(r'<title>\s*(SOLD|RENTED)', t, re.I) or '<p class="sold">' in t or re.search(r'\bSOLD\b|Sold!|Rented!', pr))
def hero_of(cards):
    for c in cards:
        t = page_of(c)
        if t:
            m = re.search(r'https://cdn\.propertiesincostarica\.com/properties/Images/[^"\']+/opt\d?/photo-1\.jpg', t)
            if m: return m.group(0)
    return FALLBACK
def balance(h):
    for tag in ('div', 'section', 'article'):
        while len(re.findall(r'</%s>' % tag, h)) > len(re.findall(r'<%s[\s>]' % tag, h)):
            i = h.rfind('</%s>' % tag)
            h = h[:i] + h[i + len(tag) + 3:]
    return h
s = rd(W + REL)
c = region(s, 'content') or ''
cards = re.findall(r'<article class="listing".*?</article>', c, flags=re.S)
cards = [x for x in cards if 'href=' in x]
fs = re.search(r'<section class="featured_listing_of.*?</section>', c, re.S)
feat = re.findall(r'<article class="listing".*?</article>', fs.group(0), re.S) if fs else []
others = [x for x in cards if x not in feat]
if not feat:
    feat = [x for x in others if not gone(x)][:2]
    others = [x for x in others if x not in feat]
# bring in the beachfront listings that are missing here
ids = set(re.findall(r'ID CODE: #(\d+)', c))
for m in ([] if True else re.finditer(r'x', '')):
    x = m.group(0); i = re.search(r'ID CODE: #(\d+)', x)
    if 'href=' in x and i and i.group(1) not in ids:
        ids.add(i.group(1)); others.append(x); print('Agregada de Beachfront: #' + i.group(1))
for rel in ADD:
    if os.path.exists(W + rel) and not any(('/' + rel + '"') in x for x in cards):
        h = rd(W + 'homes.html')
        m = re.search(r'<article class="listing"(?:(?!</article>).)*?href="/' + re.escape(rel) + r'".*?</article>', h, re.S)
        if m: others.append(m.group(0)); print('Agregada: ' + rel)
sold = [x for x in others if gone(x)]
tag = '<li><div class="sold">Sold! Looking for similar properties? <a href="/contact.html">Contact Us</a></div></li>'
def mark(x):
    if re.search(r'Sold!|>\s*SOLD\b', x): return x
    y, n = re.subn(r'<li>(?:(?!</li>).)*?Price(?:(?!</li>).)*?</li>', tag, x, count=1, flags=re.S)
    return y if n else re.sub(r'(<ul>)', lambda m: m.group(1) + tag, x, count=1)
sold = [mark(x) for x in sold]
def cid(x):
    m = re.search(r'ID CODE: #(\d+)', x); return int(m.group(1)) if m else 0
TOP = []   # Mirtha: these go right after Featured
act = [x for x in others if not gone(x)]
rent = lambda x: 1 if re.search(r'for_rent|for-rent|Vista Mare', x, re.I) else 0   # rentals go after the sale listings
act = sorted(act, key=lambda x: (TOP.index(cid(x)) if cid(x) in TOP else len(TOP), rent(x), 1 if 0 < cid(x) < 2000 else 0))
keep = feat[:2] + act + sold
first = len(c)
for pat in (r'<section class="featured_listing_of', r'<!--#+INI#+-->', r'<article class="listing"'):
    m = re.search(pat, c)
    if m: first = min(first, m.start())
last = c.rfind('</article>')
before = balance(c[:first])
if '#BeginEditable' in s: before = ''  # old page: drop the old menu table
after = re.sub(r'<!--[^>]*-->', '', c[last + 10:] if last >= 0 else '')
after = balance(after) if re.sub(r'<[^>]+>|\s|&nbsp;', '', after) else ''
w = lambda x: '<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->'
grid = ('<section class="featured_listing_of titulo_categoria" id="gotoProperties">\n<h2>Featured Golf &amp; Marina Properties of the Month</h2>\n'
        + '\n'.join(w(x) for x in keep[:2]) + '\n</section>\n' + '\n'.join(w(x) for x in keep[2:]) + '\n')
content = '\n' + before + '\n' + grid + ('<div class="car-more">' + after + '</div>\n' if after else '')
mt = re.search(r'<title>(.*?)</title>', s, re.S | re.I)
title = mt.group(1).strip() if mt else 'Golf and Marina Properties for Sale in Costa Rica | PCR'
h1 = re.sub(r'<[^>]+>', '', region(s, 'title') or '').strip() or title
md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s, re.I)
mk = re.search(r'<meta\s+name="keywords"\s+content="([^"]*)"', s, re.I)
out = rd(W + 'beach.html')
out = out.replace('href="', 'href="') 
out = put(out, 'doctitle', '\n<TITLE>' + title + '</TITLE>\n')
out = put(out, 'head', region(s, 'head') or '')
out = put(out, 'title', h1)
out = put(out, 'content', content)
out = re.sub(r'<link rel="canonical"[^>]*>\s*', '', out)
out = re.sub(r'<meta\s+name="(description|keywords|robots)"[^>]*>\s*', '', out, flags=re.I)
meta = '<meta name="robots" content="noindex, nofollow">\n<link rel="canonical" href="https://www.propertiesincostarica.com/' + REL + '">\n'
if md: meta += '<meta name="description" content="' + md.group(1) + '">\n'
if mk: meta += '<meta name="keywords" content="' + mk.group(1) + '">\n'
out = out.replace('</TITLE>', '</TITLE>\n' + meta, 1)
out = re.sub(r'(<h1 id="sp-h1">.*?</h1>.*?)<p>.*?</p>', lambda m: m.group(1) + '<p>' + INTRO + '</p>', out, count=1, flags=re.S)
out = re.sub(r'(find the right) beach home', r'\1 property', out, flags=re.I)
pic = '<picture><img src="' + 'https://cdn.propertiesincostarica.com/properties/Images/golf-villa-conchal/opt/1.jpg' + '" alt="Golf view villa in Costa Rica" width="1200" height="900" fetchpriority="high" decoding="async" style="object-fit:cover;object-position:center 50%"></picture>'
out = re.sub(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, out, count=1, flags=re.S)
out = out.replace('</head>', CSS + '</head>', 1)
np = W + 'golf_marina-nuevo.html'
open(np, 'w', encoding='utf-8', errors='surrogateescape').write(out)
print('%d tarjetas, %d vendidas al final' % (len(keep), len(sold)))
print('Vista previa: https://www.propertiesincostarica.com/' + np[len(W):])
print('LISTO (la pagina real no se cambio)')
