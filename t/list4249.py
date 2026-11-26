#!/usr/bin/env python3
# New listing #4249: Contemporary Golf View Villa with Infinity Pool near Playa Conchal
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/golf-villa-conchal.html'
PAGE = W + REL
IMGD = W + 'properties/Images/golf-villa-conchal/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/golf-villa-conchal/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4249/'
B = '/root/respaldos/list4249-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4249'
TITLE = 'Contemporary Golf View Villa with Infinity Pool near Playa Conchal'
PRICE = 'US$3,695,000'
ALT = 'Contemporary luxury villa, golf view, infinity pool, 5 bedrooms, gated community, Playa Conchal, Guanacaste, house for sale, Costa Rica'
DESC = 'New contemporary 5 bedroom villa with golf views and infinity pool in a gated beach and golf community near Playa Conchal, Guanacaste. Owner financing available. ' + PRICE + '.'
PH = {'01': '1cObxg5kO2iIigBpzSGe-h4DS28JhbjxD', '01n': '1OOgn6LOSDgShvyELcwwSwekWTVLAJQX3', '02': '1wmbXwGqg8Z4lO0IbYlvplJqDTNe-vEp_', '03': '1Gzp-1J4N5N6XR7gCMEIF_7QYd6-KQ-LW', '04': '1Eu98omMNNHNCjrC_60pKVFuyGKtiBxqe', '05': '1KwtetXbExMp20dBksP5HKo4z8kax6xDV', '055': '1NE5ZOzki8tJ_4B8KP5VxYr78Sd8f5H-D', '06': '1W2N6DWFAXne9AYejVzKK4LR1EkDyg1y6', '07': '1NRp_tK_U_iY65BqW23Jj8-kDL0CRSxor', '08': '1PwY9v9F44Rss5xN987ZseY4VUFwjnK6U', '09': '1WEsh56OeDfMZktav7PB8z342PXtmM05x', '095': '1_-CwZRe2-0gaEOuqqwjSW6Jv11ATi1zY', '10': '1bKeot5Gb3zKJDf-oikRUK2FDJzLYKpk9', '11': '1V_N5fun9q69HwV-FkINmp5znYaV4RNkS', '12': '1GhfoTu2uAWHrRuiEwZOXNZtMmQJ1YguV', '13': '1EdBd-ey_bRIHxmA91BrlFbRn4iiDfrT2', '14': '1jkTo_9hE6zfj5VVh2HcdXd_i0HyDRHbL', '15': '1szeRt4gn2A4pLKOjMmK70UGhWi-31_hn', '16': '1ptSQZTOysld4EyYcBkrEumRU4GVZP_xb', '17': '1oHDwPuoCFDz5eGCgao3cxiNYzqtLl5wP', '18': '1AxKlC-U_Mrk7sv0BW4bktWf2hNC4n9pM', '19': '1XKYWNVkCeqHkCodl2IAS3-Q-dPbRb4wa', '191': '1q6g48bFrgKwKzTKF05PWQsIpBjNaBJOy', '192': '1r3_0zXLRhAZLaQqEwBurNS3RULlF9dBW', '20': '1VzLCjD1sq9u7L8UveTESsr_BlgwETeF0', '22': '1Qft7PHaYAyoSBAJSp6-rnKN5hT9NFdJD', '23': '1FbvDlAFliL6ShSMC2S9cS1jF5ea1Dndw', '231': '1DGBHWkte6V3s-xcrian3YUomNAxmxH-K', '24': '1_YnWskGEcgvhS1r5dnXoEdKRhvcbbxri', '25': '1Cn9A0n-Km-alAf1K-jpmfk45WH-MMec1'}
BLOCKS = [
 ('p', 'Looking out over emerald fairways and tropical gardens in a gated beach and golf community near Playa Conchal, this contemporary villa is a study in glass, stone and light, designed to follow the sun throughout the day. It is a new construction project, and the images shown are architectural renderings of the finished home.'),
 ('ph', [['01', '01n', '02']]),
 ('h2', 'Double Height Living Open to the Greens'),
 ('p', 'A grand double height entrance leads into expansive living spaces with panoramic golf views. The living room, dining area and kitchen open naturally onto shaded terraces and a resort style infinity pool framed by lush landscaping, creating one seamless indoor and outdoor space.'),
 ('ph', [['03', '04', '05'], ['055', '06', '07'], ['08', '09', '095'], ['10', '11', '12']]),
 ('h2', 'Terraces, Pool and Outdoor Kitchen'),
 ('p', 'Covered decks, sun loungers around the infinity pool, a comfortable outdoor sitting area and a built in grill make the villa ideal for entertaining and for high end vacation rentals.'),
 ('ph', [['13', '14', '15'], ['16', '17', '18']]),
 ('h2', '5 Bedrooms | 5.5 Bathrooms'),
 ('p', 'Four bedroom suites are spread across both levels for privacy and natural light, each with its own spa inspired bathroom, and the primary suite includes a walk in closet. A flexible room on the lower level can become a gym and sauna, a creative studio or a fifth guest suite.'),
 ('ph', [['20', '192', '231'], ['22', '23', '24'], ['25', '191', '19']]),
 ('h2', 'Resort Living near Playa Conchal'),
 ('p', 'Owners enjoy a championship golf course, beach club, wellness and fitness facilities and walking trails, with the white sand of Playa Conchal, fine dining and surfing nearby. Owner financing is available.'),
 ('ul', ['New contemporary villa, construction underway',
         '5 bedrooms (4 suites plus a flexible lower level suite) and 5.5 bathrooms',
         'Double height living with panoramic golf views',
         'Resort style infinity pool, covered terraces and outdoor grill',
         'Lower level flex room for gym, sauna, studio or guest suite',
         'Lot of 1,177 m2 (12,669 sq.ft.), construction of 736 m2 (7,922 sq.ft.)',
         'Gated community with golf, beach club and wellness facilities',
         'Minutes to the white sand beach of Playa Conchal',
         'Owner financing available']),
 ('p', 'Refined yet relaxed, a villa designed for wellness, quiet luxury and strong rental performance, offered at ' + PRICE + '. Contact us today for more information, floor plans or a private presentation.'),
]
def get(key):
    p = TMP + key + '.jpg'
    if not os.path.exists(p) or os.path.getsize(p) < 10000:
        u = 'https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t' % PH[key]
        if subprocess.call(['wget', '-q', '-O', p, u]) != 0 or os.path.getsize(p) < 10000:
            print('AVISO: no pude bajar la foto ' + key + ', la salto'); return None
    return p
def conv(key, k):
    p = get(key)
    if not p: return False
    im = Image.open(p)
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
    return True
k = 0; html = []; first = True
for kind, val in BLOCKS:
    if kind == 'p': html.append('<p>%s</p>' % val)
    elif kind == 'h2': html.append('<h2>%s</h2>' % val)
    elif kind == 'ul': html.append('<p><strong>Property Highlights</strong></p>\n<ul>\n' + '\n'.join('<li>%s</li>' % x for x in val) + '\n</ul>')
    else:
        for row in val:
            a = ''
            for key in row:
                if not conv(key, k + 1): continue
                k += 1
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
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 1,177 m2 (12,669 sq.ft.)</strong></li>\n<li><strong>Construction: 736 m2 (7,922 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 5 | Bathrooms: 5.5</strong></li>\n<li><strong>Golf View | Infinity Pool | New Construction | Gated Community | Owner Financing</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>Land: 1,177 m2 | 5 Bedrooms | 5.5 Bathrooms | Golf View | Infinity Pool</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">New contemporary villa with double height living, golf views and infinity pool in a gated beach and golf community near Playa Conchal. Owner financing available. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/golf-villa-conchal/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('conchal.html', 'beach.html', 'gated_communities.html', 'homes.html', 'golf_residences.htm', 'pre-construction_real_estate.html'):
    p = W + f
    t = open(p, encoding='utf-8', errors='surrogateescape').read()
    if REL in t: print('ya estaba en ' + f); continue
    i = t.find('featured_listing_of')
    if i >= 0: j = t.find('</section>', i) + len('</section>')
    else: j = t.find('<!--###################INI')
    if j < 0: print('OJO: no encontre la lista en ' + f); continue
    shutil.copy2(p, B + f.replace('/', '_'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t[:j] + '\n' + CARD + t[j:])
    print('Tarjeta agregada en ' + f)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
