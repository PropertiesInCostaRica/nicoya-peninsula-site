#!/usr/bin/env python3
# Previews only: Whale Bay photo in the Seller Financing banner, spacing in the Articles list,
# and 'Can't find the right home?' (not 'beach home') on all 6 previews.
import re
W = '/var/www/propertiesincostarica.com/web/'
P = W + 'financing-nuevo.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
IMG = 'https://cdn.propertiesincostarica.com/properties/Images/whale-bay-villa-2/opt/photo-1.jpg'
new = ('<picture><img src="' + IMG + '" alt="" width="1672" height="941" fetchpriority="high" decoding="async" '
       'style="object-fit:cover;object-position:center 60%"></picture>')
s2, n = re.subn(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + new, s, count=1, flags=re.S)
if n:
    open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
print('Foto Whale Bay en Seller Financing: ' + ('SI' if n else 'NO'))
P = W + 'articles/index-nuevo.htm'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
CSS = ('<style>#contentpage ul li{margin:10px 0;line-height:1.5;font-size:16px}'
       '#contentpage ul li a{text-decoration:none}#contentpage ul li a:hover{text-decoration:underline}</style>\n</head>')
if 'margin:10px 0;line-height:1.5' not in s:
    s = s.replace('</head>', CSS, 1)
    open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Articulos con mas espacio: SI')
n = 0
for rel in ['financing-nuevo.html', 'articles/index-nuevo.htm', 'videos/index-nuevo.html', 'links-nuevo.html', 'info/sanjose-nuevo.html', 'map-nuevo.html']:
    P = W + rel
    try:
        s = open(P, encoding='utf-8', errors='surrogateescape').read()
    except IOError:
        continue
    s2 = re.sub(r'(find the right) beach (home)', r'\1 \2', s, flags=re.I)
    if s2 != s:
        open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2); n += 1
print('Paginas con "Can\'t find the right home?": %d' % n)
print('LISTO (solo vistas previas)')
