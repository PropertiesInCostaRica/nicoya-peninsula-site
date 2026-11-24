#!/usr/bin/env python3
# Darkens the banner photo on caribbean-nuevo.html so the white text is easy to read.
import shutil, time
p = '/var/www/propertiesincostarica.com/web/caribbean-nuevo.html'
s = open(p, encoding='utf-8', errors='surrogateescape').read()
css = '<style id="hero-dark">.sp-hero picture img{filter:brightness(.55)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 2px 8px rgba(0,0,0,.8)}</style>\n'
if 'id="hero-dark"' in s:
    print('Ya estaba arreglado')
else:
    shutil.copy(p, '/root/respaldos/caribbean-nuevo.html-' + time.strftime('%Y%m%d-%H%M%S'))
    s = s.replace('</head>', css + '</head>', 1)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    print('LISTO: https://www.propertiesincostarica.com/caribbean-nuevo.html')
