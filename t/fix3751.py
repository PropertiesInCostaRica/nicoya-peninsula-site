# Actualiza en TODO el sitio las tarjetas de #3751 (abundance.html): nombre y precio nuevos
import os, re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/fix3751-' + time.strftime('%Y%m%d%H%M') + '/'
TITLE = 'Masterfully Crafted Ocean View Estate in Tango Mar'
LI = ('<li>Land: 3,175 m2 (3/4 acre) / Total Construction: 600 m2 (6,500 sq.ft.)</li>\n'
      '<li><b>MAIN HOUSE:</b> 436 m2 (4,693 sq. ft.) / Bedrooms: 3 | Baths: 3</li>\n'
      '<li><b>GUESTHOUSE:</b> 75 m2 (800 sq. ft.) / Bedrooms: 2 | Baths: 1</li>\n'
      '<li>Swimming Pool: 75 m2 (800 sq. ft.) | Garage: 4 | Ample Parking</li>\n'
      '<li>Sales Price: US$1,200,000</li>')
TXT = ('A masterfully crafted ocean view estate in Tango Mar on the southern Nicoya Peninsula. '
       'The main house offers 3 bedrooms and 3 bathrooms, a detached <b>GUESTHOUSE</b> adds 2 bedrooms and full privacy for family or guests, '
       'and the pool looks out to the ocean, all on 3,175 m2 of beautifully kept grounds. '
       '<a href="/properties/nicoya_peninsula/for_sale/abundance.html"> More Information... </a>')
def fix(a):
    a2 = re.sub(r'(<h3[^>]*>\s*<a[^>]*>).*?(</a>)', lambda m: m.group(1) + TITLE + m.group(2), a, count=1, flags=re.S)
    a2 = re.sub(r'<ul>.*?</ul>', '<ul>\n' + LI + '\n</ul>', a2, count=1, flags=re.S)
    a2 = re.sub(r'(<div class="listing_content">).*?(</div>)', lambda m: m.group(1) + TXT + ' ' + m.group(2), a2, count=1, flags=re.S)
    a2 = re.sub(r'(alt=")[^"]*(")', lambda m: m.group(1) + TITLE + m.group(2), a2, count=1)
    return a2
n = 0
for root, dirs, files in os.walk(W):
    if '/.git' in root or root.startswith(W + 'properties/Images'): continue
    for fn in files:
        if not re.search(r'\.(html?|php)$', fn): continue
        f = os.path.join(root, fn)
        try: t = open(f, encoding='utf-8', errors='surrogateescape').read()
        except Exception: continue
        if 'abundance.html' not in t or '<article class="listing"' not in t: continue
        nt = re.sub(r'<article class="listing"(?:(?!</article>).)*?abundance\.html.*?</article>', lambda m: fix(m.group(0)), t, flags=re.S)
        if nt != t:
            os.makedirs(B, exist_ok=True); rel = f[len(W):]
            shutil.copy2(f, B + rel.replace('/', '_'))
            open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt); n += 1
            print('Actualizada: https://www.propertiesincostarica.com/' + rel)
print('Paginas actualizadas:', n)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
