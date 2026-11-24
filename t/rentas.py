#!/usr/bin/env python3
# PREVIEWS (-nuevo, noindex) of the other rental pages, same format as the new Long Term Rentals page.
# Live pages are NOT changed. Rented/sold cards are left out of the preview.
import re, os
W = '/var/www/propertiesincostarica.com/web/'
PAGES = [
 ('vacation_rentals.html', 'Vacation homes, villas and condos for short stays in the Central Valley and at the beach, with nightly, weekly and monthly rates.'),
 ('long-term-rentals-furnished.html', 'Furnished homes, condos and apartments for rent in Escazu, Santa Ana, Heredia, San Jose and the beaches, ready to move in.'),
 ('long-term-rentals-unfurnished.html', 'Unfurnished homes, condos and apartments for long term rent in Escazu, Santa Ana, Heredia and San Jose.'),
 ('long_term_rentals_2.html', 'More homes, condos, apartments and offices for long term rent across Costa Rica.'),
 ('luxury_rentals.htm', 'Luxury homes, estates, penthouses and beachfront villas for rent in Costa Rica.'),
]
FALLBACK = 'https://cdn.propertiesincostarica.com/properties/Images/investment-villa/opt/photo-1.jpg'
CSS = ('<style id="car-css">.sp-hero picture img{filter:brightness(.75)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 1px 3px rgba(0,0,0,.9),0 2px 12px rgba(0,0,0,.7)}'
       '.car-more{clear:both;margin-top:30px}</style>\n')
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def region(s, n):
    a = s.find('<!-- InstanceBeginEditable name="%s" -->' % n)
    if a < 0: return None
    a = s.index('-->', a) + 3
    e = s.find('<!-- InstanceEndEditable -->', a)
    return s[a:e] if e > 0 else None
def put(s, n, val):
    a = s.index('<!-- InstanceBeginEditable name="%s" -->' % n)
    a = s.index('-->', a) + 3
    e = s.index('<!-- InstanceEndEditable -->', a)
    return s[:a] + val + s[e:]
def page_of(card):
    m = re.search(r'href="(?:https?://www\.propertiesincostarica\.com)?/?(properties/[^"?#]+\.html?)', card)
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
for REL, INTRO in PAGES:
    p = W + REL
    if not os.path.exists(p):
        print(REL + ': no existe'); continue
    s = rd(p)
    c = region(s, 'content') or ''
    cards = re.findall(r'<article class="listing".*?</article>', c, flags=re.S)
    cards = [x for x in cards if 'href=' in x]
    keep = [x for x in cards if not gone(x)]
    first = len(c)
    for pat in (r'<section class="featured_listing_of', r'<!--#+INI#+-->', r'<article class="listing"'):
        m = re.search(pat, c)
        if m: first = min(first, m.start())
    last = c.rfind('</article>')
    before = balance(c[:first])
    after = re.sub(r'<!--[^>]*-->', '', c[last + 10:] if last >= 0 else '')
    after = balance(after) if re.sub(r'<[^>]+>|\s|&nbsp;', '', after) else ''
    w = lambda x: '<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->'
    grid = ('<section class="featured_listing_of titulo_categoria" id="gotoProperties">\n<h2>Featured Rentals of the Month</h2>\n'
            + '\n'.join(w(x) for x in keep[:2]) + '\n</section>\n' + '\n'.join(w(x) for x in keep[2:]) + '\n')
    content = '\n' + before + '\n' + grid + ('<div class="car-more">' + after + '</div>\n' if after else '')
    mt = re.search(r'<title>(.*?)</title>', s, re.S | re.I)
    title = mt.group(1).strip() if mt else 'Costa Rica Rentals | PCR'
    h1 = re.sub(r'<[^>]+>', '', region(s, 'title') or '').strip() or title
    md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s, re.I)
    mk = re.search(r'<meta\s+name="keywords"\s+content="([^"]*)"', s, re.I)
    out = rd(W + 'beach.html')
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
    out = re.sub(r'(find the right) beach home', r'\1 rental', out, flags=re.I)
    pic = '<picture><img src="' + hero_of(keep) + '" alt="" width="1200" height="900" fetchpriority="high" decoding="async" style="object-fit:cover;object-position:center 55%"></picture>'
    out = re.sub(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, out, count=1, flags=re.S)
    out = out.replace('</head>', CSS + '</head>', 1)
    np = W + re.sub(r'\.(html?)$', r'-nuevo.\1', REL)
    open(np, 'w', encoding='utf-8', errors='surrogateescape').write(out)
    print(REL + ': %d tarjetas, %d alquiladas o vendidas quitadas, quedan %d' % (len(cards), len(cards) - len(keep), len(keep)))
    print('   -> https://www.propertiesincostarica.com/' + np[len(W):])
print('LISTO (las paginas reales no se cambiaron)')
