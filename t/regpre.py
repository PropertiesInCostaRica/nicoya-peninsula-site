#!/usr/bin/env python3
# PREVIEW region_and_price/index-nuevo.html (noindex) with the new design. Live page NOT changed.
import re, os
W = '/var/www/propertiesincostarica.com/web/'
REL = 'region_and_price/index.html'
HERO = 'https://cdn.propertiesincostarica.com/properties/Images/ocean-setting/opt3/photo-3.jpg'
INTRO = 'Search Costa Rica real estate by region and budget, from the Central Valley to the beaches of the Pacific and the Caribbean.'
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
s = rd(W + REL)
c = region(s, 'content')
paras = re.findall(r'<p align="justify">.*?</p>', c, re.S)
intro = paras[0] + '\n' + (paras[1] if len(paras) > 1 else '')
loc = re.findall(r'<div class="lsting">\s*<h4>.*?</ul>\s*</div>', c, re.S)
# price blocks: one per form
blocks = []
for m in re.finditer(r'<form name="form_([a-z_]+)"[^>]*>(.*?)</form>', c, re.S):
    key, body = m.group(1), m.group(2)
    name = re.search(r'Properties by\s+price range in\s+([^:<]+):', body)
    name = re.sub(r'\s+', ' ', name.group(1)).strip() if name else key.replace('_', ' ').title()
    before = c[:m.start()]
    imgs = re.findall(r'<img src="(maps/[^"]+)"', before)
    img = imgs[-1] if imgs else ''
    links = re.findall(r'<a href="([^"]+)"[^>]*>\s*([^<]+?)\s*</a>', body)
    blocks.append((key, name, img, links))
cid = {'costa_rica': 'costarica'}
cards = ''
for key, name, img, links in blocks:
    cards += ('<div class="rp-card" id="' + cid.get(key, key + '_cr') + '">'
              + ('<img src="' + img + '" alt="' + name + ' map" loading="lazy">' if img else '')
              + '<h3>' + name + '</h3><ul>' + ''.join('<li><a href="' + h + '">' + t + '</a></li>' for h, t in links) + '</ul></div>\n')
css = ('<style id="car-css">.sp-hero picture img{filter:brightness(.9) saturate(1.1)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 1px 3px rgba(0,0,0,.9),0 2px 12px rgba(0,0,0,.7)}'
       '.rp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;margin:20px 0 34px}'
       '.rp-card{border:1px solid #d9eef4;border-radius:4px;background:#f7fcfe;padding:14px;text-align:center}'
       '.rp-card img{max-width:180px;height:auto;margin:0 auto 8px;display:block}'
       '.rp-card h3{font-size:18px;margin:4px 0 10px;color:#036}.rp-card ul{list-style:none;margin:0;padding:0;text-align:left}'
       '.rp-card li{border-top:1px solid #e3f1f6}.rp-card li a{display:block;padding:7px 4px;text-decoration:none}'
       '.rp-card li a:hover{background:#4cb9d4;color:#fff}'
       '.rp-loc{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;margin:16px 0 30px;text-align:left}'
       '.rp-loc .lsting{border:1px solid #d9eef4;border-radius:4px;padding:10px 14px;width:auto;float:none;margin:0}'
       '.rp-loc h4{color:#048dc7;text-transform:uppercase;font-size:14px;margin:4px 0 6px}.rp-loc ul{margin:0;padding-left:18px}</style>\n')
content = ('\n' + intro + '\n<h2 id="gotoProperties">Properties by Region and Price</h2>\n<div class="rp-grid">\n' + cards + '</div>\n'
           + ('<h2>Properties by Location</h2>\n<div class="rp-loc">\n' + '\n'.join(loc) + '\n</div>\n' if loc else ''))
mt = re.search(r'<title>(.*?)</title>', s, re.S | re.I)
title = mt.group(1).strip() if mt else 'Costa Rica Property for Sale by Region and Price | PCR'
h1 = re.sub(r'<[^>]+>', '', region(s, 'title') or '').strip() or title
md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s, re.I)
out = rd(W + 'beach.html')
out = put(out, 'doctitle', '\n<TITLE>' + title + '</TITLE>\n')
out = put(out, 'head', region(s, 'head') or '')
out = put(out, 'title', h1)
out = put(out, 'content', content)
out = re.sub(r'<link rel="canonical"[^>]*>\s*', '', out)
out = re.sub(r'<meta\s+name="(description|keywords|robots)"[^>]*>\s*', '', out, flags=re.I)
meta = '<meta name="robots" content="noindex, nofollow">\n<link rel="canonical" href="https://www.propertiesincostarica.com/' + REL + '">\n'
if md: meta += '<meta name="description" content="' + md.group(1) + '">\n'
out = out.replace('</TITLE>', '</TITLE>\n' + meta, 1)
out = re.sub(r'(<h1 id="sp-h1">.*?</h1>.*?)<p>.*?</p>', lambda m: m.group(1) + '<p>' + INTRO + '</p>', out, count=1, flags=re.S)
out = re.sub(r'(find the right) beach home', r'\1 property', out, flags=re.I)
pic = '<picture><img src="' + HERO + '" alt="Ocean view terrace at sunset" width="1200" height="807" fetchpriority="high" decoding="async" style="object-fit:cover;object-position:center 50%"></picture>'
out = re.sub(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, out, count=1, flags=re.S)
out = out.replace('</head>', css + '</head>', 1)
np = W + 'region_and_price/index-nuevo.html'
open(np, 'w', encoding='utf-8', errors='surrogateescape').write(out)
print('Regiones: %d, ubicaciones: %d' % (len(blocks), len(loc)))
print('Vista previa: https://www.propertiesincostarica.com/region_and_price/index-nuevo.html')
print('LISTO (la pagina real no se cambio)')
