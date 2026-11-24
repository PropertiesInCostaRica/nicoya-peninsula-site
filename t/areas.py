#!/usr/bin/env python3
# PREVIEWS (-nuevo.html, noindex) of the 7 Caribbean area pages, same format as the new Caribbean page.
# Live pages are NOT changed. Sold cards are left out of the previews.
import re, os
W = '/var/www/propertiesincostarica.com/web/'
PAGES = [
 ('puerto-viejo-real-estate.html', 'Puerto Viejo / Playa Negra', 'Homes, lots and income properties in Puerto Viejo de Talamanca and Playa Negra, the lively heart of the Southern Caribbean.'),
 ('cocles-chiquita-real-estate.html', 'Cocles / Playa Chiquita', 'Homes, lots and rental villas between Cocles and Playa Chiquita, minutes from Puerto Viejo and the beach.'),
 ('manzanillo-real-estate.html', 'Punta Uva / Manzanillo', 'Prime properties near Punta Uva and Manzanillo, beside the Gandoca Manzanillo Wildlife Refuge.'),
 ('cahuita-real-estate.html', 'Cahuita', 'Homes, lots and farms in Cahuita and Playa Grande, next to Cahuita National Park.'),
 ('hone-creek-carbon.html', 'Hone Creek / Carbon', 'Lots, farms and homes in Hone Creek and Carbon, close to services and 15 minutes from Puerto Viejo.'),
 ('tortuguero-real-estate.html', 'Limón / Tortuguero', 'Properties in Limón and Tortuguero on Costa Rica\'s Northern Caribbean coast.'),
 ('guapiles-real-estate.html', 'Guápiles / Siquirres', 'Farms, land and homes in Guápiles and Siquirres, on the route between San José and the Caribbean.'),
]
FALLBACK = 'https://cdn.propertiesincostarica.com/properties/Images/investment-villa/opt/photo-1.jpg'
CSS = ('<style id="car-css">.sp-hero picture img{filter:brightness(.55)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 2px 8px rgba(0,0,0,.8)}'
       '.car-areas{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:18px 0 26px;clear:both}'
       '.car-areas span{font-weight:bold;color:#048dc7;text-transform:uppercase;font-size:13px;margin-right:4px}'
       '.car-areas a{border:1px solid #4cb9d4;border-radius:3px;padding:8px 14px;text-decoration:none;color:#036;background:#f4fdff;font-size:14px}'
       '.car-areas a:hover,.car-areas a.on{background:#4cb9d4;color:#fff}.car-more{clear:both;margin-top:30px}</style>\n')
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
    m = re.search(r'href="(?:https?://www\.propertiesincostarica\.com)?(/[^"?#]+\.html?)', card)
    if not m: return None
    f = W + m.group(1).lstrip('/')
    return rd(f) if os.path.exists(f) else None
def sold(card):
    if re.search(r'>\s*SOLD\b', card): return True
    t = page_of(card)
    if not t: return False
    pr = region(t, 'price') or ''
    return bool(re.search(r'<title>\s*SOLD', t, re.I) or '<p class="sold">' in t or re.search(r'\bSOLD\b|Sold!', pr))
def hero_of(cards):
    for c in cards:
        t = page_of(c)
        if t:
            m = re.search(r'https://cdn\.propertiesincostarica\.com/properties/Images/[^"\']+/opt\d?/photo-1\.jpg', t)
            if m: return m.group(0)
    return FALLBACK
def balance(h):
    # drop closing div/section tags that have no opening tag
    for tag in ('div', 'section', 'article'):
        while len(re.findall(r'</%s>' % tag, h)) > len(re.findall(r'<%s[\s>]' % tag, h)):
            i = h.rfind('</%s>' % tag)
            h = h[:i] + h[i + len(tag) + 3:]
    return h
shell = rd(W + 'beach.html')
for rel, name, intro in PAGES:
    p = W + rel
    if not os.path.exists(p):
        print(rel + ': no existe'); continue
    s = rd(p)
    c = region(s, 'content') or ''
    cards = re.findall(r'<article class="listing".*?</article>', c, flags=re.S)
    keep = [x for x in cards if not sold(x)]
    first = len(c)
    for pat in (r'<section class="featured_listing_of', r'<!--#+INI#+-->', r'<article class="listing"'):
        m = re.search(pat, c)
        if m: first = min(first, m.start())
    last = c.rfind('</article>')
    before = balance(c[:first])
    after = c[last + 10:] if last >= 0 else ''
    after = re.sub(r'<!--[^>]*-->', '', after)
    after = balance(after) if re.sub(r'<[^>]+>|\s|&nbsp;', '', after) else ''
    links = ''.join('<a href="/' + r + '"' + (' class="on"' if r == rel else '') + '>' + n + '</a>' for r, n, i in PAGES)
    pills = '<div class="car-areas"><span>Explore by area:</span><a href="/caribbean.html">All Caribbean</a>' + links + '</div>\n'
    w = lambda x: '<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->'
    if len(keep) > 2:
        grid = ('<section class="featured_listing_of titulo_categoria" id="gotoProperties">\n<h2>Featured Properties of the Month</h2>\n'
                + '\n'.join(w(x) for x in keep[:2]) + '\n</section>\n' + '\n'.join(w(x) for x in keep[2:]) + '\n')
    else:
        grid = ('<section class="featured_listing_of titulo_categoria" id="gotoProperties">\n<h2>Properties in ' + name + '</h2>\n'
                + '\n'.join(w(x) for x in keep) + '\n</section>\n')
    content = '\n' + before + '\n' + pills + grid + ('<div class="car-more">' + after + '</div>\n' if after else '')
    title = re.search(r'<title>(.*?)</title>', s, re.S | re.I).group(1).strip().replace('Honne', 'Hone')
    h1 = re.sub(r'<[^>]+>', '', region(s, 'title') or '').strip().replace('Honne', 'Hone') or title
    md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s, re.I)
    out = shell
    out = put(out, 'doctitle', '\n<TITLE>' + title + '</TITLE>\n')
    out = put(out, 'head', region(s, 'head') or '')
    out = put(out, 'title', h1)
    out = put(out, 'content', content)
    out = re.sub(r'<link rel="canonical"[^>]*>\s*', '', out)
    out = re.sub(r'<meta\s+name="(description|keywords|robots)"[^>]*>\s*', '', out, flags=re.I)
    meta = '<meta name="robots" content="noindex, nofollow">\n<link rel="canonical" href="https://www.propertiesincostarica.com/' + rel + '">\n'
    if md: meta += '<meta name="description" content="' + md.group(1).replace('Honne', 'Hone') + '">\n'
    out = out.replace('</TITLE>', '</TITLE>\n' + meta, 1)
    out = re.sub(r'(<h1 id="sp-h1">.*?</h1>.*?)<p>.*?</p>', lambda m: m.group(1) + '<p>' + intro + '</p>', out, count=1, flags=re.S)
    out = re.sub(r'(find the right) beach home', r'\1 property', out, flags=re.I)
    pic = '<picture><img src="' + hero_of(keep) + '" alt="" width="1200" height="900" fetchpriority="high" decoding="async" style="object-fit:cover;object-position:center 55%"></picture>'
    out = re.sub(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, out, count=1, flags=re.S)
    out = re.sub(r'<style id="(hero-dark|car-css)">.*?</style>\n?', '', out, flags=re.S)
    out = out.replace('</head>', CSS + '</head>', 1)
    np = W + rel.replace('.html', '-nuevo.html')
    open(np, 'w', encoding='utf-8', errors='surrogateescape').write(out)
    print('%s: %d tarjetas, %d vendidas quitadas -> https://www.propertiesincostarica.com/%s' % (rel, len(cards), len(cards) - len(keep), np[len(W):]))
print('LISTO (las paginas reales no se cambiaron)')
