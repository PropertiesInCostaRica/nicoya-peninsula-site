#!/usr/bin/env python3
# homes.html: banner photo changed to Sol y Mar Sunrise Retreat (infinity pool at sunset). Backup first.
import re, shutil, time
p = '/var/www/propertiesincostarica.com/web/homes.html'
s = open(p, encoding='utf-8', errors='surrogateescape').read()
pic = ('<picture><img src="https://cdn.propertiesincostarica.com/properties/Images/self-sufficient/opt/photo-23.jpg" alt="Sol y Mar Sunrise Retreat infinity pool at sunset" '
       'width="1200" height="900" fetchpriority="high" decoding="async" style="object-fit:cover;object-position:center 30%"></picture>')
s2, n = re.subn(r'(<section class="sp-hero"[^>]*>\s*)<picture>.*?</picture>', lambda m: m.group(1) + pic, s, count=1, flags=re.S)
s2 = s2.replace('.sp-hero picture img{filter:brightness(.75)}', '.sp-hero picture img{filter:brightness(1.15) saturate(1.2)}')
if n != 1:
    print('No encontre la foto del banner, sin cambio'); raise SystemExit
shutil.copy(p, '/root/respaldos/homes.html-' + time.strftime('%Y%m%d-%H%M%S'))
open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
print('LISTO: https://www.propertiesincostarica.com/homes.html')
