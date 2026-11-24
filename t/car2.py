#!/usr/bin/env python3
# Rebuilds the content of caribbean-nuevo.html (PREVIEW only):
# cards in the 2 per row grid like Financing, area links as buttons, darker banner photo.
import re, shutil, time
p = '/var/www/propertiesincostarica.com/web/caribbean-nuevo.html'
s = open(p, encoding='utf-8', errors='surrogateescape').read()
shutil.copy(p, '/root/respaldos/caribbean-nuevo.html-' + time.strftime('%Y%m%d-%H%M%S'))
A = '<!-- InstanceBeginEditable name="content" -->'
a = s.index(A) + len(A)
e = s.index('<!-- InstanceEndEditable -->', a)
c = s[a:e]
cards = re.findall(r'<article class="listing".*?</article>', c, flags=re.S)
print('Tarjetas:', len(cards))
txt = c[:c.index('<section class="featured_listing_of')]
txt = re.sub(r'\s*</div>\s*$', '', txt.rstrip())
areas = re.findall(r'<a href="([^"]+-real-estate\.html|hone-creek-carbon\.html)">([^<]+)</a>', txt)
txt = re.sub(r'<center>.*?</center>', '', txt, flags=re.S)
paras = re.split(r'(?<=</p>)', txt, maxsplit=1)
intro, rest = paras[0], (paras[1] if len(paras) > 1 else '')
pills = '<div class="car-areas"><span>Explore by area:</span>' + ''.join('<a href="/' + h + '">' + t.strip() + '</a>' for h, t in areas) + '</div>\n'
grid = ('<section class="featured_listing_of titulo_categoria" id="gotoProperties">\n<h2>Caribbean Properties for Sale and Rent</h2>\n'
        + '\n'.join('<!--###################INI#####################-->\n' + x + '\n<!--###################FIN#####################-->' for x in cards)
        + '\n</section>\n')
new = '\n' + intro + '\n' + pills + grid + '<div class="car-more">' + rest + '</div>\n'
s = s[:a] + new + s[e:]
css = ('<style id="car-css">.sp-hero picture img{filter:brightness(.55)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 2px 8px rgba(0,0,0,.8)}'
       '.car-areas{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:18px 0 26px;clear:both}'
       '.car-areas span{font-weight:bold;color:#048dc7;text-transform:uppercase;font-size:13px;margin-right:4px}'
       '.car-areas a{border:1px solid #4cb9d4;border-radius:20px;padding:6px 14px;text-decoration:none;color:#036;background:#f4fdff;font-size:14px}'
       '.car-areas a:hover{background:#4cb9d4;color:#fff}.car-more{clear:both;margin-top:30px}</style>\n')
s = re.sub(r'<style id="(hero-dark|car-css)">.*?</style>\n?', '', s, flags=re.S)
s = s.replace('</head>', css + '</head>', 1)
open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Areas:', len(areas))
print('LISTO: https://www.propertiesincostarica.com/caribbean-nuevo.html')
