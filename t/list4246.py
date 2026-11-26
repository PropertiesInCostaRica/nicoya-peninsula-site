#!/usr/bin/env python3
# New listing #4246: Modern Courtyard Home Steps from the Surf, Playa Grande
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/courtyard-home-playa-grande.html'
PAGE = W + REL
IMGD = W + 'properties/Images/courtyard-home-playa-grande/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/courtyard-home-playa-grande/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4246/'
B = '/root/respaldos/list4246-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4246'
TITLE = 'Modern Courtyard Home Steps from the Surf, Playa Grande'
PRICE = 'US$1,795,000'
ALT = 'Modern courtyard home, pool, 4 bedrooms, beach access, Playa Grande, Guanacaste, house for sale, Costa Rica'
DESC = 'Modern 4 bedroom courtyard home with pool and a private path to one of the best surf breaks in Playa Grande, Guanacaste. Fully furnished with strong rental potential. ' + PRICE + '.'
PH = {'001': '1e5RVlyQ7l6ZU_7lMGnVZ0G2ekygn3dHX', '002': '1iVgSA9JjdxPR7P4AGQf0_VbLtN2Y8uam', '003': '1vCuRBE9R4L2ehjNWIOFHyu-gJcwRzLXS', '004a': '11exVZitOK1C4vZIg5NHlwEr9mYRt-CMy', '004b': '1RWBbnqayNqAuXEqA-xLvBJ3YW3ztfel0', '005': '13zUezdQw9Od7b8bfaKbccEP705bCtflJ', '006': '1NzT-bvRlOCt2MrdEs3KcWobvfWi1C9_5', '007': '10-Q8euCNm5Mrr4vEebbtkvjPbBShIMW9', '008': '1uJPKDlV4XG81Gv0zbPfOH3zg70JHuv3D', '009': '1sJhP9joo1u7BkWpBwqgM7J8GpSm9uYOJ', '010': '1HYEyiA1uCa_GCY7PH_fHXcHBfCICjZ71', '011': '1leQ32TC_P0Zw3EIcCpAXG_cRIg15Rarj', '012': '1NDrpxK_3pBw1VhqDlSAPPNlWLqrGSRJ7', '013': '1b5RL6x7HgWRJTrIywfo1k0XhHTCB6n-8', '014': '1tVYkAMTO1FoaVKWryMFHT9f8CruBa9fS', '015': '1yon0enj25LpcU9Y0sNe3opz7zdsP3AtX', '016': '1c3ayfYj3ArC2gSULHICMq5YyyLCH0d5i', '017': '19RpKYTuJBTcNyRMQc1_lz-c8AdS0PZxV', '018': '1yPhixSWfSR7KEUrrVgiFtybUPtjiyQPI', '019a': '1RjIK5gdYCCoMPiDb2ufEsrb0zb4bjqNa', '019b': '1bZ9ICJH_hlFCn73R7QQKeL-1P2sy9XVX', '020': '1Oo0Gy-mFtvd-jgODdLksuXPBFNCXGjfK', '021': '1dDbkLyF_gHWQt92B8FG8gzAL38wclm_X', '022': '13aPEhXTSV7Sp1jOo8AmJFuFnSapQl1gK', '023': '1BbY3fASx3mnwwQPyXNY_rTkM1X66rxAJ', '024': '1_r6J-8uGHf6A0qjGLWOhQcpQD8eOEwT5', '025': '1UUcr1CpObXh0KcAJibb6YyUri4f6ayuD', '026': '1Nzlh2dAaTYKOk4EfX_t0LsaTuVZCEnTg', 'Na': '10ICf46Ef8KOQu3S2K5QDPkRXHPqYoa4L', 'Nb': '12xBBjgQ-WdeTYhtx-1hFVFNDH7swkaz7', 'Nc': '15Sn5J_e63fkfwpo_rU0_TGzLwZXPt_Oy', 'Nd': '1ACjd4gl8uZLYJ1e4h3hSg3amRmB3hOH-', 'Ne': '1B4l0D1hkTiQg43rxhomDlQTlQDp4qw9o'}
BLOCKS = [
 ('p', 'Close enough to hear the waves from the backyard, this modern home in Playa Grande, Guanacaste, has a discreet path that takes you straight to one of the most consistent surf breaks on the coast. Clean white architecture, warm wood and a lush dry tropical garden create a calm, private retreat that works beautifully as a family home and has very strong rental potential.'),
 ('ph', [['002', '025', '001']]),
 ('h2', 'Designed Around a Central Courtyard'),
 ('p', 'The home wraps around an open courtyard and pool, so every room enjoys light, breeze and garden views while keeping its own privacy. The living, dining and kitchen areas share one bright open space with large windows, classic lines and carefully chosen finishes. It is sold fully furnished with pieces made by local artisans.'),
 ('ph', [['004b', '004a', '005'], ['006', '007', '013']]),
 ('h2', 'Gardens, Patios and Outdoor Showers'),
 ('p', 'Shaded sitting areas, sculptural cacti and native plants frame the courtyard and the outdoor living spaces. Rain showers indoors and out make it easy to rinse off after a surf session, and there is practical storage for surfboards, motorcycles and beach gear.'),
 ('ph', [['009', '010', '011'], ['012', '014', '003']]),
 ('h2', '4 Bedroom Suites | 4.5 Bathrooms'),
 ('p', 'All four bedrooms are en suite, including two spacious primary suites, giving family and guests comfort and privacy. Bathrooms feature walk in rain showers, stone details and natural light.'),
 ('ph', [['015', '016', '017'], ['018', '019a', '019b'], ['021', '022', '024'], ['Nc', 'Ne', 'Nd'], ['023', '020', 'Na']]),
 ('h2', 'Beach Life in Playa Grande'),
 ('p', 'Playa Grande is known for its wide golden beach, great surf and protected natural surroundings, with Tamarindo just across the estuary for restaurants and shopping. The home includes a security system and whole house water filtration, so owners and guests can simply enjoy the beach.'),
 ('ph', [['Nb', '008', '026']]),
 ('ul', ['Modern single family home steps from the beach in Playa Grande',
         'Private path to one of the area\'s most consistent surf breaks',
         '4 en suite bedrooms including two primary suites, 4.5 bathrooms',
         'Pool and open courtyard at the heart of the home',
         'Indoor and outdoor rain showers, storage for surfboards and motorcycles',
         'Sold fully furnished with locally made pieces',
         'Security system and whole house water filtration',
         'Lot of 800 m2 (8,611 sq.ft.), construction of 395 m2 (4,251 sq.ft.)',
         'Excellent family home with very strong rental income potential']),
 ('p', 'A rare chance to own a modern home just steps from the surf in Playa Grande, offered at ' + PRICE + '. Contact us today for more information or to arrange a private showing.'),
]
def get(key):
    p = TMP + key + '.jpg'
    if not os.path.exists(p) or os.path.getsize(p) < 10000:
        u = 'https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t' % PH[key]
        if subprocess.call(['wget', '-q', '-O', p, u]) != 0 or os.path.getsize(p) < 10000:
            raise SystemExit('ERROR: no pude bajar la foto ' + key)
    return p
def conv(key, k):
    im = Image.open(get(key))
    try: im.draft('RGB', (2000, 2000))
    except Exception: pass
    if ImageOps and hasattr(ImageOps, 'exif_transpose'):
        try: im = ImageOps.exif_transpose(im)
        except Exception: pass
    im = im.convert('RGB')  # re-save drops EXIF and GPS
    if im.width > 1600: im = im.resize((1600, int(im.height * 1600.0 / im.width)), Image.LANCZOS)
    im.save(IMGD + '%d.jpg' % k, quality=84, optimize=True, progressive=True)
    tw, th = 500, 374
    r = max(float(tw) / im.width, float(th) / im.height)
    t = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
    x = (t.width - tw) // 2; y = (t.height - th) // 2
    t.crop((x, y, x + tw, y + th)).save(IMGD + 'thumbs/%d.jpg' % k, quality=82, optimize=True)
k = 0; html = []; first = True
for kind, val in BLOCKS:
    if kind == 'p': html.append('<p>%s</p>' % val)
    elif kind == 'h2': html.append('<h2>%s</h2>' % val)
    elif kind == 'ul': html.append('<p><strong>Property Highlights</strong></p>\n<ul>\n' + '\n'.join('<li>%s</li>' % x for x in val) + '\n</ul>')
    else:
        for row in val:
            a = ''
            for key in row:
                k += 1; conv(key, k)
                a += '<a href="%s%d.jpg"><img src="%sthumbs/%d.jpg" alt="%s" width="250" height="187"></a>' % (CDN, k, CDN, k, ALT)
            if first:
                a += '\n<span class="to_enlarge">Click on the pictures to enlarge</span>'; first = False
            html.append('<p class="photo">\n' + a + '\n</p>')
print('%d fotos listas (sin datos GPS)' % k)
shutil.copy(IMGD + 'thumbs/1.jpg', IMGD + '../p.jpg')
R = {
 'doctitle': '\n<meta property="og:title" content="%s, ID CODE: #%s">\n<meta property="og:description" content="%s">\n<meta property="og:image" content="%s1.jpg">\n<meta property="og:url" content="%s">\n<link rel="canonical" href="%s">\n<title>%s, ID CODE: #%s</title>\n<meta name="description" content="%s">\n<meta name="keywords" content="%s">\n' % (TITLE, CODE, DESC, CDN, URL, URL, TITLE, CODE, DESC, ALT),
 'title': TITLE,
 'code': 'ID CODE: #' + CODE,
 'price': 'Sales Price: ' + PRICE,
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 800 m2 (8,611 sq.ft.)</strong></li>\n<li><strong>Construction: 395 m2 (4,251 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 4 | Bathrooms: 4.5</strong></li>\n<li><strong>Pool | Steps to the Beach | Furnished | Rental Income | Surf Storage</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>Land: 800 m2 | 4 Bedrooms | 4.5 Bathrooms | Pool | Steps to the Beach</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">Modern courtyard home with pool and a private path to the surf in Playa Grande, four en suite bedrooms, sold furnished with strong rental potential. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/courtyard-home-playa-grande/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('tamarindo-real-estate.html', 'beach.html', 'homes.html', 'invest/income_producing.html'):
    p = W + f
    t = open(p, encoding='utf-8', errors='surrogateescape').read()
    if REL in t: print('ya estaba en ' + f); continue
    i = t.find('featured_listing_of')
    j = t.find('</section>', i) if i >= 0 else -1
    if j < 0: print('OJO: no encontre la lista en ' + f); continue
    j += len('</section>')
    shutil.copy2(p, B + f.replace('/', '_'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t[:j] + '\n' + CARD + t[j:])
    print('Tarjeta agregada en ' + f)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
