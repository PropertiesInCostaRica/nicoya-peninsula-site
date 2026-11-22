#!/usr/bin/env python3
# Preview only: show listings 2 per row with the ID on the photo (financing-nuevo.html)
import re
P = '/var/www/propertiesincostarica.com/web/financing-nuevo.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
if 'class="pg-grid"' in s:
    raise SystemExit('Ya tenia la cuadricula')
a = s.find('<article class="listing"')
b = s.rfind('</article>') + len('</article>')
if a < 0:
    raise SystemExit('No encontre propiedades')
s = s[:a] + '<div class="pg-grid">\n' + s[a:b] + '\n</div>' + s[b:]
CSS = '''<style>
.pg-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin:24px 0}
.pg-grid>*:not(article){grid-column:1/-1}
.pg-grid article.listing{background:#fff;border-radius:6px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.12);display:flex;flex-direction:column}
.pg-grid .listing_img{position:relative}
.pg-grid .listing_img img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
.pg-grid .idcodes{position:absolute;left:12px;bottom:12px;background:rgba(0,0,0,.65);color:#fff;font-family:Oswald,sans-serif;font-size:14px;letter-spacing:1px;padding:5px 12px;border-radius:3px}
.pg-grid .listing_data{padding:16px 20px 22px}
.pg-grid .listing_data h3{margin:0 0 10px;font-size:20px;line-height:1.3}
.pg-grid .listing_data h3 a{color:#216B3D;text-decoration:none}
.pg-grid .listing_data ul{list-style:none;padding:0;margin:0 0 12px;font-size:14px}
.pg-grid .listing_data li{margin:3px 0}
.pg-grid .listing_content{font-size:14px;color:#555}
@media (max-width:700px){.pg-grid{grid-template-columns:1fr}}
</style>
</head>'''
s = s.replace('</head>', CSS, 1)
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Propiedades en la cuadricula: %d' % len(re.findall(r'<article class="listing"', s)))
print('LISTO (solo la vista previa)')
