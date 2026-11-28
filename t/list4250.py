#!/usr/bin/env python3
# New listing #4250: Building Lot in Paquera (Lee Stevens)
# Preview: python3 list4250.py        Apply: python3 list4250.py --aplicar
import os, re, shutil, subprocess, sys, time
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
SLUG = 'paquera-lot'
REL = 'properties/paquera/for-sale/%s.html' % SLUG
PAGE = W + REL
IMGD = W + 'properties/Images/%s/' % SLUG
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/%s/opt/' % SLUG
URL = 'https://www.propertiesincostarica.com/' + REL
GET = 'https://www.properties-in-costa-rica.com/t/i4250/'
APPLY = '--aplicar' in sys.argv
B = '/root/respaldos/list4250-' + time.strftime('%Y%m%d%H%M') + '/'
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4250'
TITLE = 'Building Lot of 8,444 m2 in Paquera, Nicoya Peninsula'
PRICE = 'US$89,000'
ALT = 'Lot for sale, Paquera, Puntarenas, Nicoya Peninsula, land for sale near Tambor and Curu, Costa Rica'
DESC = 'Lot of 8,444 m2 (over 2 acres) for sale in Paquera on the southern Nicoya Peninsula, near Tambor and Curu Wildlife Refuge. ' + PRICE + '.'
PH = [1, 2, 4]   # stock photos of the region; photo 3 (a volcano) is left out
BLOCKS = [
 ('p', 'In Paquera, on the southern Nicoya Peninsula, this lot of 8,444 m2 (over 2 acres) gives you room for a home, a vacation retreat or a long term investment in a quiet coastal area. It is offered at US$89,000, about US$10.50 per m2.'),
 ('p', '<em>Reference photos of the area. Photos of the lot will be added soon.</em>'),
 ('ph', [[1, 2, 4]]),
 ('h2', 'Room to Build'),
 ('p', 'With 8,444 m2 (90,890 sq.ft.) there is space for a private residence, a family compound, gardens or a small eco project, subject to local permits.'),
 ('h2', 'Life in Paquera'),
 ('p', 'Paquera is a friendly, unhurried town on the Gulf of Nicoya. Curu Wildlife Refuge, the beaches of Tambor and Isla Tortuga are close by, and Montezuma and Santa Teresa are within driving distance. The Paquera ferry links the peninsula with Puntarenas and the rest of the country.'),
 ('ul', ['Lot of 8,444 m2 (90,890 sq.ft.), over 2 acres',
         'Paquera, Puntarenas, southern Nicoya Peninsula',
         'Near Tambor beaches, Curu Wildlife Refuge and Isla Tortuga',
         'Paquera ferry to Puntarenas',
         'About US$10.50 per m2']),
 ('p', 'Offered at ' + PRICE + '. Contact Properties in Costa Rica for more details or to plan a visit.'),
]
print('Pagina: ' + URL)
print('Titulo: ' + TITLE + ' | ID ' + CODE + ' | ' + PRICE)
if not APPLY:
    print('Vista previa. Para publicar: python3 list4250.py --aplicar'); raise SystemExit
for d in (IMGD + 'opt/thumbs', B): os.makedirs(d, exist_ok=True)
def dl(src, dst):
    if subprocess.call(['wget', '-q', '-O', dst, GET + src]) != 0 or os.path.getsize(dst) < 2000:
        raise SystemExit('No pude bajar ' + src)
for n in PH:
    dl('opt/photo-%d.jpg' % n, IMGD + 'opt/%d.jpg' % n)
    dl('thumbs/photo-%d.jpg' % n, IMGD + 'opt/thumbs/%d.jpg' % n)
shutil.copy(IMGD + 'opt/thumbs/1.jpg', IMGD + 'p.jpg')
print('%d fotos bajadas' % len(PH))
html = []; first = True
for kind, val in BLOCKS:
    if kind == 'p': html.append('<p>%s</p>' % val)
    elif kind == 'h2': html.append('<h2>%s</h2>' % val)
    elif kind == 'ul': html.append('<p><strong>Property Highlights</strong></p>\n<ul>\n' + '\n'.join('<li>%s</li>' % x for x in val) + '\n</ul>')
    else:
        for row in val:
            a = ''.join('<a href="%s%d.jpg"><img src="%sthumbs/%d.jpg" alt="%s" width="250" height="187"></a>' % (CDN, k, CDN, k, ALT) for k in row)
            if first:
                a += '\n<span class="to_enlarge">Click on the pictures to enlarge</span>'; first = False
            html.append('<p class="photo">\n' + a + '\n</p>')
R = {
 'doctitle': '\n<meta property="og:title" content="%s, ID CODE: #%s">\n<meta property="og:description" content="%s">\n<meta property="og:image" content="%s1.jpg">\n<meta property="og:url" content="%s">\n<link rel="canonical" href="%s">\n<title>%s, ID CODE: #%s</title>\n<meta name="description" content="%s">\n<meta name="keywords" content="%s">\n' % (TITLE, CODE, DESC, CDN, URL, URL, TITLE, CODE, DESC, ALT),
 'title': TITLE,
 'code': 'ID CODE: #' + CODE,
 'price': 'Sales Price: ' + PRICE,
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 8,444 m2 (90,890 sq.ft.)</strong></li>\n<li><strong>Paquera | Southern Nicoya Peninsula | Near Tambor</strong></li>\n</ul>\n',
 'content': '\n' + '\n'.join(html) + '\n',
 'hidden': '\n<input type="hidden" name="CODE" value="%s">\n<input name="interested_in" type="hidden" id="interested_in" value="%s">\n' % (CODE, TITLE),
}
s = open(SRC, encoding='utf-8', errors='surrogateescape').read()
for name, val in R.items():
    s, n = re.subn(r'(<!-- InstanceBeginEditable name="%s" -->).*?(<!-- InstanceEndEditable -->)' % name, lambda m: m.group(1) + val + m.group(2), s, count=1, flags=re.S)
    if n != 1: raise SystemExit('ERROR region ' + name)
for bad in ('whale-bay-villa', 'Whale Bay', '4241'):
    if bad in s: print('AVISO: quedo texto de la plantilla: ' + bad)
os.makedirs(os.path.dirname(PAGE), exist_ok=True)
open(PAGE, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Pagina nueva: ' + URL)
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="https://cdn.propertiesincostarica.com/properties/Images/%s/p.jpg" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li><strong>Land size: 8,444 m2 (90,890 sq.ft.)</strong></li>\n<li><strong>Paquera | Near Tambor</strong></li>\n<li><strong>Sales Price: %s</strong></li>\n</ul>\n<div class="listing_content">Over 2 acres in Paquera on the southern Nicoya Peninsula, close to Tambor beaches and Curu Wildlife Refuge. Room for a home, retreat or eco project. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, SLUG, TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('tambor_real_estate.html', 'nicoya_peninsula_real_estate.html', 'residential_lots.html'):
    p = W + f
    t = open(p, encoding='utf-8', errors='surrogateescape').read()
    if REL in t: print('ya estaba en ' + f); continue
    i = t.find('featured_listing_of')
    if i >= 0: j = t.find('</section>', i) + len('</section>')
    else: j = t.find('<!--###################INI')
    if j < len('</section>'): print('OJO: no encontre la lista en ' + f); continue
    shutil.copy2(p, B + f.replace('/', '_'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t[:j] + '\n' + CARD + t[j:])
    print('Tarjeta agregada en ' + f)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO. Respaldos en ' + B)
