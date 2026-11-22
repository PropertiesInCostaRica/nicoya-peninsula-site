#!/usr/bin/env python3
# Previews only: Whale Bay photo in the Seller Financing banner, and more spacing in the Articles list.
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
print('LISTO (solo vistas previas)')
