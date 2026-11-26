#!/usr/bin/env python3
# New listing #4245: Signature Ocean View Estate Above Flamingo
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/ocean-view-estate-flamingo.html'
PAGE = W + REL
IMGD = W + 'properties/Images/ocean-view-estate-flamingo/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/ocean-view-estate-flamingo/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4245/'
B = '/root/respaldos/list4245-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4245'
TITLE = 'Signature Ocean View Estate Above Flamingo'
PRICE = 'US$3,250,000'
ALT = 'Luxury ocean view estate, infinity pool, 5 bedrooms, Flamingo, Guanacaste, house for sale, Costa Rica'
DESC = 'Architectural 5 bedroom ocean view estate with infinity pool on 1.26 acres in a gated community above Flamingo Marina, Guanacaste, with an established luxury rental operation. ' + PRICE + '.'
PH = {
 '1':'1O5RFb5cxW0PvwhKcmFKNHNA1i3u5YxbQ',
 '2':'1Z2F9cbVCdWWMkPsrpo25YtpZkBjfzUbB',
 '3':'1xiu_aZQdMji5AGmPLw2-T8iRak1CCr-q',
 '4':'14NsB5O5uh88IkzWSJxyzS-LhYG_mlHcR',
 '5':'1DqZ4zuO1yX4L1dfLvTfVtLO590heY7vl',
 '6':'15pimXt-J3sAFfKvy3QtZPqGPA-tnsCjH',
 '7':'1FRt6BN-efpnlO0328Ct40DWBsgFbZFis',
 '8':'1d8W4Z57F2qNiYCC08DG3fNLoLqT5-m40',
 '9':'1b74WIQp5CAzlpO39ee5q9eEhFp7SmStR',
 '10':'1NN_3HAuEsSyYiCD22RDXTP50s14GA0Fy',
 '11':'1RQssMVe0h3SMzcAfHleB1qDZEVOx6PqD',
 '12':'1fzmbQ5lJGdknkX-kcZBLM4C5IteJiUeM',
 '13':'1LtIxDlEr1XO7y7QLv24tZr6X_KY3mwMR',
 '14':'1iOsee9T8XRDZsXVSNZoi6Ttbf5AvLG3F',
 '15':'1NA6z0YkyyxiU55FY5V-Ft08R4H6VdwId',
 '16':'156nnfYJ-1SKjEy351yOPwiqiePQC2P5Z',
 '17':'1PqzJyWZK1TmM98Uuhg4LoBIpiPg6zctd',
 '18':'1TqJyGirI-khkJmAfLrGeOqdG7OfUnRjd',
 '19':'1M5hAKxAi56nJIjQrNBtFW4lGFmIMhpg-',
 '20':'1m4u89mOw_YLBtH_5z-avqcqtTvIV7-wX',
 '20.2':'1fcroQEjyTWJiqFrhSlqp3Be9pUtwLJpd',
 '21':'1DT0slsTUVSlWVPfmeHMPibYvLqrrskCa',
 '22':'1XkCB1YMusZJAi3XcBUOpSpijEWQafUys',
 '23':'1bO9OJ-6jfUns5U10p7eH4stAqORLiyfD',
 '24':'1d7Y0dbxfb1ixFohL8eD-7dVHccYm8yvk',
 '25':'1YFd7DFsodJC7bAfAr6WsFwMMuQ1yMsTe',
 '26':'1AtwTt5idLydoAc3QFPmMjkIRguGg-Z9U',
 '27':'1NIvksVszTAwwbYveW4D24bg5p1KcO9FK',
 '28':'1uf6qU4AxvvNoK5p7Ep0PVFKqA1V9sFxd',
 '29':'1i_-VWGWhuyFTvWrRigYc9-_N2QH7zd0p',
 '30':'1NcYQUYH9HoRgzJCq1eZ7p7H1s0UfOsb5',
 '31':'1WlyV_bdHZXyiaMroeb00tVymuVZ09cn0',
 '32':'1i6YLTph8pFcUOpJh7OhKnIgsuHbA3hmz',
}
BLOCKS = [
 ('p', 'High on the hills above Flamingo Marina, this architectural estate looks out over the Pacific from almost every room. Set on 1.26 acres of mature tropical gardens inside a gated community, it pairs striking design with complete privacy, unforgettable sunsets and the rare advantage of a luxury vacation rental that is already running smoothly.'),
 ('ph', [['1', '3', '20.2']]),
 ('h2', 'Light, Horizon and Natural Materials'),
 ('p', 'You arrive along a landscaped stone walkway to a grand entrance that opens straight onto the view. Inside, soaring wood ceilings, walls of glass, textured stone and custom lighting create a home with real personality, warm and welcoming rather than decorated all at once. The great room, dining area and gourmet kitchen flow together and face the ocean, so every meal comes with a Pacific backdrop.'),
 ('ph', [['2', '4', '5'], ['6', '7', '10'], ['8', '9', '12']]),
 ('h2', 'Outdoor Living with an Infinity Pool'),
 ('p', 'Wide covered terraces lead to outdoor lounges, an outdoor kitchen with grill and a long infinity edge pool that seems to pour into the sea. Established trees and lush gardens give shade and seclusion, making the outdoor spaces as comfortable at noon as they are magical at sunset and under the stars.'),
 ('ph', [['13', '14', '15'], ['18', '19', '20']]),
 ('h2', '5 Bedrooms | 4.5 Bathrooms'),
 ('p', 'Five generous bedroom suites, including a primary suite with ocean views from the bed, give family and guests space and privacy. The bathrooms are finished with natural stone, wood vanities and walk in showers, many of them open to garden or ocean views.'),
 ('ph', [['16', '17', '23'], ['24', '30', '31'], ['32', '22', '21'], ['25', '26']]),
 ('h2', 'Easy Ownership, Proven Rental Income'),
 ('p', 'The estate comes with full time house care, professional rental management and a strong rental history, so it is immaculately maintained and earns income whenever the owners are away. The community offers tennis courts, a fitness center, hiking and biking trails and a restaurant overlooking the Pacific, and Playa Flamingo, Playa Conchal, Brasilito, international schools and the marina are only minutes away. Liberia International Airport is about 45 minutes by car.'),
 ('ph', [['11', '28', '29'], ['27']]),
 ('ul', ['Architectural ocean view estate in a gated community above Flamingo Marina',
         '5 bedrooms and 4.5 bathrooms, ocean views from almost every room',
         'Infinity edge pool, covered terraces, outdoor kitchen and lounges',
         'Wood ceilings, natural stone, floor to ceiling glass and custom lighting',
         'Mature tropical gardens with great privacy',
         'Full time house care and an established luxury rental program in place',
         'Lot of 5,097 m2 (54,863 sq.ft., 1.26 acres), construction of 310 m2 (3,337 sq.ft.)',
         'Community with tennis, fitness center, trails and restaurant',
         'Minutes to Playa Flamingo and Playa Conchal, about 45 minutes to Liberia airport']),
 ('p', 'A truly special home on the Gold Coast of Guanacaste that combines design, views and income, offered at ' + PRICE + '. Contact us today for more information or to arrange a private showing.'),
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
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 5,097 m2 (54,863 sq.ft.)</strong></li>\n<li><strong>Construction: 310 m2 (3,337 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 5 | Bathrooms: 4.5</strong></li>\n<li><strong>Ocean View | Infinity Pool | Gated Community | Rental Income | Outdoor Kitchen</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>Land: 5,097 m2 | 5 Bedrooms | 4.5 Bathrooms | Ocean View | Infinity Pool</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">Architectural estate with Pacific views from almost every room, infinity pool and 1.26 acres of tropical gardens above Flamingo Marina, with full time house care and a proven rental program. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/ocean-view-estate-flamingo/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('flamingo_real_estate.html', 'beach.html', 'gated_communities.html', 'homes.html', 'homes/ocean_view_homes.html', 'ocean_view_properties.htm'):
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
