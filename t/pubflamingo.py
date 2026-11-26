#!/usr/bin/env python3
# Publish flamingo_real_estate-nuevo.html as flamingo_real_estate.html
import re, os, glob, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/'
os.makedirs(B, exist_ok=True)
st = time.strftime('%Y%m%d%H%M')
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s): open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
LI = ('<li>Land: 3,175 m2 (3/4 acre) / Total Construction: 600 m2 (6,500 sq.ft.) </li>\n'
      '      <li><b>MAIN HOUSE:</b> 436 m2 (4,693 sq. ft.) / Bedrooms: 3 | Baths: 3 </li>\n'
      '      <li><b>GUESTHOUSE:</b> 75 m2 (800 sq. ft.) / Bedrooms: 2 | Baths: 1 </li>\n'
      '      <li>Swimming Pool: 75 m2 (800 sq. ft.) | Garage: 4 | Ample Parking </li>\n'
      '      <li>Sales Price: US$1,200,000 </li>')
TXT = ('A masterfully crafted ocean view estate in Tango Mar on the southern Nicoya Peninsula. '
       'The main house offers 3 bedrooms and 3 bathrooms, a detached <b>GUESTHOUSE</b> adds 2 bedrooms and full privacy for family or guests, '
       'and the pool looks out to the ocean, all on 3,175 m2 of beautifully kept grounds. '
       '<a href="/properties/nicoya_peninsula/for_sale/abundance.html">3D Tours</a>')
def fixcard(m):
    c = m.group(0)
    if 'for_sale/abundance.html' not in c: return c
    c = re.sub(r'<ul>.*?</ul>', '<ul>\n      ' + LI + '\n    </ul>', c, count=1, flags=re.S)
    c = re.sub(r'(<div class="listing_content">).*?(</div>)', lambda x: x.group(1) + TXT + ' ' + x.group(2), c, count=1, flags=re.S)
    return c

REL = 'flamingo_real_estate.html'
new = W + 'flamingo_real_estate-nuevo.html'
if not os.path.exists(new): raise SystemExit('No existe la vista previa ' + new)
shutil.copy2(W + REL, B + REL + '.' + st)
s = rd(new)
s = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', s)
wr(W + REL, s)
print('Publicado: https://www.propertiesincostarica.com/' + REL)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
