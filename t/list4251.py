#!/usr/bin/env python3
# New listing #4251: Flat Building Lots near Cahuita National Park (Leo)
# Preview: python3 list4251.py        Apply: python3 list4251.py --aplicar
import os, re, shutil, subprocess, sys, time
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
SLUG = 'cahuita-lots'
REL = 'properties/caribe/for-sale/%s.html' % SLUG
PAGE = W + REL
IMGD = W + 'properties/Images/%s/' % SLUG
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/%s/opt/' % SLUG
URL = 'https://www.propertiesincostarica.com/' + REL
GET = 'https://www.properties-in-costa-rica.com/t/i4251/'
APPLY = '--aplicar' in sys.argv
B = '/root/respaldos/list4251-' + time.strftime('%Y%m%d%H%M') + '/'
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4251'
TITLE = 'Flat Building Lots near Cahuita National Park, Caribbean Coast'
PRICE = 'From US$95,000'
ALT = 'Building lots for sale, Cahuita, Limon, Caribbean coast, near Cahuita National Park, residential and commercial lots, sea view lots, Costa Rica'
DESC = 'Flat residential, commercial and sea view building lots on Route 36, 500 m from Cahuita National Park on the Caribbean coast of Costa Rica. ' + PRICE + '.'
PH = [1, 2, 3, 4, 5, 6, 7, 8, 9]   # photo 10 is the survey plan: left out (it shows 20 lots, the text says 15)
BLOCKS = [
 ('p', 'Just 500 meters from the Puerto Vargas entrance to Cahuita National Park, this subdivision on Costa Rica\'s South Caribbean coast offers flat building lots for a home, a small lodge or a roadside business. The lots sit along Route 36, the main road between Cahuita and Puerto Viejo, so access is easy all year.'),
 ('ph', [[1, 2, 3]]),
 ('h2', 'Lots for Every Plan'),
 ('p', 'The subdivision has 15 lots: twelve of about 1,000 m2 (10,764 sq.ft.) and three larger lots of 1,159 m2, 1,163 m2 and 1,275 m2. Some lots are already sold, so ask us which ones are still available. The 1,159 m2 and 1,275 m2 lots are at the back of the property and enjoy sea views.'),
 ('p', 'Lots are priced at US$95 per m2, so a 1,000 m2 lot is US$95,000. The two sea view lots are priced at US$150 per m2.'),
 ('ph', [[4, 5, 6]]),
 ('h2', 'Ready to Build'),
 ('p', 'Every lot is flat, so the whole surface can be used for the house, parking and gardens. Electricity is available at the front of the property, and the land is outside any restricted area, so you can start permits and construction paperwork right away.'),
 ('h2', 'Corner Lots on Route 36'),
 ('p', 'Two corner lots of about 1,000 m2 are still available with direct frontage on Route 36 and room for parking in front. They work well for a shop, a cafe or lodging, and the location near the national park entrance suits hospitality projects.'),
 ('ph', [[7, 8, 9]]),
 ('h2', 'Life in Cahuita'),
 ('p', 'Cahuita town is 3 km away and Puerto Viejo is 10 km away, so beaches, restaurants and daily services are close by.'),
 ('ul', ['15 flat building lots in Cahuita, Limon, 500 m from Cahuita National Park',
         'Lots from about 1,000 m2 to 1,275 m2 (10,764 to 13,724 sq.ft.)',
         'US$95 per m2, sea view lots US$150 per m2',
         'Two sea view lots at the back of the property',
         'Two corner lots with frontage on Route 36, good for commercial or residential use',
         'Electricity at the property front',
         'Outside restricted areas, ready for permits',
         '3 km to Cahuita and 10 km to Puerto Viejo']),
 ('p', 'Lots from US$95,000. Contact Properties in Costa Rica for the list of available lots, title details or to plan a visit.'),
]
print('Pagina: ' + URL)
print('Titulo: ' + TITLE + ' | ID ' + CODE + ' | ' + PRICE)
if not APPLY:
    print('Vista previa. Para publicar: python3 list4251.py --aplicar'); raise SystemExit
for d in (IMGD + 'opt/thumbs', B): os.makedirs(d, exist_ok=True)
def dl(src, dst):
    if subprocess.call(['wget', '-q', '-O', dst, GET + src]) != 0 or os.path.getsize(dst) < 2000:
        raise SystemExit('No pude bajar ' + src)
for n in PH:
    dl('opt/photo-%d.jpg' % n, IMGD + 'opt/%d.jpg' % n)
    dl('thumbs/photo-%d.jpg' % n, IMGD + 'opt/thumbs/%d.jpg' % n)
dl('p.gif', IMGD + 'p.gif')
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
 'features': '\n<ul id="data_table">\n<li><strong>Lot sizes: 1,000 m2 to 1,275 m2 (10,764 to 13,724 sq.ft.)</strong></li>\n<li><strong>US$95 per m2 | Sea view lots US$150 per m2</strong></li>\n<li><strong>Flat Lots | Electricity | Route 36 Frontage | 500 m to Cahuita National Park</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="https://cdn.propertiesincostarica.com/properties/Images/%s/p.gif" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li><strong>Lots from 1,000 m2 (10,764 sq.ft.)</strong></li>\n<li><strong>Flat | Electricity | Sea View Lots</strong></li>\n<li><strong>Sales Price: %s</strong></li>\n</ul>\n<div class="listing_content">Flat building lots on Route 36, 500 m from the Puerto Vargas entrance to Cahuita National Park, for a home, lodge or business. Two sea view lots and two corner lots available. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, SLUG, TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('cahuita-real-estate.html', 'caribbean.html', 'residential_lots.html'):
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
