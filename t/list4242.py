#!/usr/bin/env python3
# New listing #4242: Modern Tropical Home with Pool in a Gated Beach Community, Playa Grande
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/modern-tropical-pool-home.html'
PAGE = W + REL
IMGD = W + 'properties/Images/modern-tropical-pool-home/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/modern-tropical-pool-home/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4242/'
B = '/root/respaldos/list4242-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4242'
TITLE = 'Modern Tropical Home with Pool in a Gated Beach Community, Playa Grande'
PRICE = 'US$1,350,000'
ALT = 'Modern tropical home, pool, 4 bedrooms, gated community, Playa Grande, Guanacaste, house for sale, Costa Rica'
DESC = 'Modern 4 bedroom tropical home with private pool in a secure gated community minutes from the beach in Playa Grande, Guanacaste. ' + PRICE + '.'
PH = {
 '01':'1dqfrD30jJxswyhJsEVhzkdRA0KINtcn5','02':'1E5-M6cSXlCYt9cm01S_T3OLrJB3U6Ctl','03':'1dptxkxYqrZ6VkCFK9f1iHjl3PiKo76A9',
 '04':'1vgDP7J69YrM5pP-SfaHfAP9Kldbk72SK','4.5':'1HaJ6WM-Z8cELNyFxwVlBnbbImuqIzlis','05':'19tnJXb4dIRBU_3YXLRVOoOEWr9rbEG1p',
 '5.5':'1pWe0E3Aoxf9kanglvZi3h2-F1GtKnGyR','06':'1MeyxQ58ZUsUpwdPBq_33Jjw-iJjdd83y','07':'1-QlGbZjypSsMzUTY72iJus2Eyly6Lizx',
 '09':'13FgyCbjapw_W17KA2-sJdwm6WyOiQNbo','10':'1W8h5WIwT2neWAe5GPwDr_3EwEDnHkG9o','11':'15rj2Vp9o4OZwfHZOKD6ykRlqnmOUox7s',
 '12':'1tbvICshwFSZ3IyrPfVOw_wSZSL4amjPI','13':'1MrcBadyiZUTIFuYdYYTYsAWlU778uDdm','14':'1l90Xql5C9o9tl3UJ_QEVPqqEtZFhHT20',
 '14.5':'12BnrRivbPvFKA0GUfjHdoInqiF8HRdW1','15':'1JcF40O0HHd1tj9zhVK_TXHxBIKKRCXq-','16':'149jbY-cwUINZ4G9Wm8uA3EaGG0UGYz_r',
 '17':'1C2g65H7pdbDrponNjTjMmHm-vQMwh4t3','17.5':'1Cgs0QtdATG_8EPLL4vMr1yCIMCmDAW6N','18':'1oyxqc2hj7mD2QxJKOIvYgoSH3jLLjfMG',
 '19':'1fae2CM9cUme-a98MaTNzeacdJnQZxqyZ','21':'11Av4KM-e4XtkzCfErBEGlvyMhhFHuGfN',
}
BLOCKS = [
 ('p', 'Set among mature tropical trees inside a secure gated community, this contemporary home is built around a private pool and a wide wooden deck, just a few minutes from the beach in Playa Grande, Guanacaste. Glass walls, high wood ceilings and clean lines give it a bright, relaxed feel, while the trees around the property keep it private and cool.'),
 ('ph', [['01', '02', '07'], ['19', '06', '09']]),
 ('h2', 'Open Living Around the Pool'),
 ('p', 'The kitchen, dining room and living room share one generous open space. Large sliding glass doors fold the whole room out onto the deck and the pool, so daily life, dinners with friends and lazy beach days all flow easily between inside and out. The kitchen has a long island, dark cabinetry and warm wood shelving.'),
 ('ph', [['05', '5.5', '10'], ['11', '12', '13']]),
 ('h2', '4 Bedrooms | 3.5 Bathrooms'),
 ('p', 'The primary suite looks onto the garden and pool and has its own bathroom. Two more bedrooms, one of them set up with bunk beds for kids or guests, share a bathroom, and a fourth bedroom with a private bath works just as well as a guest room or a home office. Every room has air conditioning and plenty of natural light.'),
 ('ph', [['14', '14.5', '15'], ['16', '17', '17.5']]),
 ('h2', 'Made for Beach Life'),
 ('p', 'Come home from the waves through a practical mud room with an outdoor shower and storage for surfboards and beach gear, so sand stays outside. A large laundry room and a garage complete the home.'),
 ('ph', [['18', '21', '03']]),
 ('h2', 'A Secure Community Close to Everything'),
 ('p', 'The gated community offers 24 hour security, a clubhouse with ocean views and a pool, tennis and pickleball courts and walking trails, with low HOA fees. The beach, restaurants, schools and daily services are all a few minutes away, and Tamarindo is a short drive.'),
 ('ph', [['04', '4.5']]),
 ('ul', ['Contemporary single family home in a gated community near Playa Grande',
         '4 bedrooms and 3.5 bathrooms, air conditioning throughout',
         'Private pool surrounded by a wooden deck and mature trees',
         'Open kitchen, dining and living areas with glass walls to the pool',
         'Mud room with outdoor shower and surfboard storage, large laundry room, garage',
         'Lot of 1,105 m2 (0.27 acre), home of 190 m2 (2,045 sq.ft.)',
         'Community clubhouse with ocean view, tennis, pickleball and trails, 24 hour security',
         'A few minutes to the beach, close to Tamarindo']),
 ('p', 'A well designed, easy to live in beach home in one of the most sought after areas of Guanacaste, offered at ' + PRICE + '. Contact us today for more information or to arrange a private showing.'),
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
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 1,105 m2 (11,894 sq.ft.)</strong></li>\n<li><strong>Construction: 190 m2 (2,045 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 4 | Bathrooms: 3.5</strong></li>\n<li><strong>Pool | Gated Community | Garage | A/C | Mud Room with Outdoor Shower</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>Land: 1,105 m2 | 4 Bedrooms | 3.5 Bathrooms | Pool | Gated Community</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">Contemporary tropical home with a private pool, glass walls to the deck and a mud room for surfers, in a secure gated community a few minutes from the beach in Playa Grande. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/modern-tropical-pool-home/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('tamarindo-real-estate.html', 'beach.html', 'gated_communities.html', 'homes.html'):
    p = W + f
    t = open(p, encoding='utf-8', errors='surrogateescape').read()
    if REL in t: print('ya estaba en ' + f); continue
    i = t.find('featured_listing_of')
    j = t.find('</section>', i) if i >= 0 else -1
    if j < 0: print('OJO: no encontre la lista en ' + f); continue
    j += len('</section>')
    shutil.copy2(p, B + f)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t[:j] + '\n' + CARD + t[j:])
    print('Tarjeta agregada en ' + f)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
