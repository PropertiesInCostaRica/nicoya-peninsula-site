#!/usr/bin/env python3
# New listing #4244: Modern Single Level Home with Guest Casita and Pool near Tamarindo
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/modern-home-casita-tamarindo.html'
PAGE = W + REL
IMGD = W + 'properties/Images/modern-home-casita-tamarindo/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/modern-home-casita-tamarindo/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4244/'
B = '/root/respaldos/list4244-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4244'
TITLE = 'Modern Single Level Home with Guest Casita and Pool near Tamarindo'
PRICE = 'US$795,000'
ALT = 'Modern home, guest casita, pool, 4 bedrooms, gated community, near Tamarindo, Guanacaste, house for sale, Costa Rica'
DESC = 'New modern single level home with a 1 bedroom guest casita, pool and almost half an acre in a gated community a short drive from the beaches of Tamarindo, Guanacaste. ' + PRICE + '.'
PH = {
 '198':'1PA0oTFdxW6sf4Vqgp6JQIJgnuL5fh4zU',
 '205':'1pidxrl2NPy-h9B8MINxbRKNCYsKUeBJn',
 '213':'1Ki8vCY3QCcTZbeBLkpIYEFq1122o9fGU',
 '312':'1qMcCIPnYzBqAIgvsdc_-VrLqZ6DQXzQF',
 '318':'1SsE7g-SUF7JZdsrMuOxPVIxvkMMs0v19',
 '321':'1D-22wr1baEaE2_4uMl6Q3X13QsIPrw0F',
 '335':'1Gl_ItyjpKXaeBTZSeh-dDGb9QeroduOc',
 '339':'1k0HC_V4KlacAsb1dpKGkLgNPhdD5aYbx',
 '302':'1WyjTAIG7e53yxZoRpshARkzkybxSfy_O',
 '184':'1Z7fOQPSr-Pa-EfyzG2oToTTiJ-2TNxXp',
 '271':'1sgIA49xE2njlqBYU2tucdnp-zcwUTLzz',
 '279':'1beYdJbuItwdyqCmJEt1mpEGBRXiExJru',
 '284':'18QnL-nYJn-kGNgpCB6dZqJfXSFusMpzB',
 '289':'1-Weu9iJuNQB0jFMk7QHbs94a5wJDWeP9',
 '245':'1DGq5gFBa62UIxrS6GZBIeQJ9WTsTboUD',
 '294':'1ZJC0VI6QV12Q_D3brfCxsOSTDZMmQ6XQ',
 '298':'18QNFYo7biU6mFUi07wynY7H1ScafJlvl',
 '307':'1FDV8SfaZYlpvhUa28U3_981aYSyrh9hQ',
 '195':'13E1lgiT1-K1pqAMnDpNYRQDefkmp_3bo',
 '221':'1EvZGGu2BdaHNdybFSHJRHIglvniuCLLr',
 '228':'112iuuLWestZrRG2donwcWYJvjQeBPmz6',
 '237':'1XB86v23qLtlJ_QGa5TjRkxFfJyz-njbf',
 '243':'1VelSHe3xz4mUjj0juIa5O_Yj76NYmkYJ',
 '190':'1AW6nfuPc0tO8lUidespAti02tvIvU8-k',
}
BLOCKS = [
 ('p', 'Newly built and sold fully furnished, this modern single level home and its separate guest casita sit on almost half an acre of landscaped gardens inside a peaceful gated community, just a short drive from Tamarindo and the beaches of the Gold Coast of Guanacaste. Polished concrete, warm wood ceilings and walls of glass create a calm, contemporary home where every room opens to the green surroundings.'),
 ('ph', [['198', '205', '213']]),
 ('h2', 'Open Living, Indoors and Out'),
 ('p', 'The heart of the home is a bright open living, dining and kitchen area under a high wood ceiling. Sliding glass doors connect it to the covered terrace, the pool and the lawn, so the house feels twice its size. The well equipped kitchen with its long island is ready for family meals and entertaining, and the BBQ area by the pool makes outdoor dinners easy.'),
 ('ph', [['312', '318', '321'], ['335', '339', '302']]),
 ('h2', '4 Bedrooms | 4 Bathrooms'),
 ('p', 'The main house offers three bedrooms, each with its own bathroom, and the private casita adds a fourth bedroom suite that is perfect for guests, family, a caretaker or extra rental income. The bathrooms feature custom wood vanities, walk in showers and large windows that bring in natural light and garden views.'),
 ('ph', [['184', '271', '279'], ['284', '289', '245'], ['294', '298', '307']]),
 ('h2', 'Room to Grow'),
 ('p', 'With a lot of 1,974 m2 (0.49 acre), there is still plenty of space on the property to build another guest casita for rental income or to extend the main house to five or six bedrooms. The yard is fully landscaped and has an irrigation system to keep it green all year.'),
 ('ph', [['195', '221', '228'], ['237', '243', '190']]),
 ('h2', 'A Secure Community near the Beach'),
 ('p', 'The gated community has a clubhouse and nature trails, with monthly HOA fees of about US$181. Tamarindo, the surrounding beaches, schools, restaurants and shopping are all a short drive away.'),
 ('ul', ['New modern single level home, sold fully furnished',
         'Main house with 3 bedroom suites plus a separate 1 bedroom guest casita',
         '4 bedrooms and 4 bathrooms in total',
         'Private pool, BBQ area and covered terrace',
         'Open living, dining and kitchen with glass doors to the garden',
         'Landscaped yard with irrigation system',
         'Lot of 1,974 m2 (21,257 sq.ft., 0.49 acre), construction of 241 m2 (2,600 sq.ft.)',
         'Space to add another casita or expand to 5 or 6 bedrooms',
         'Gated community with clubhouse and nature trails, short drive to Tamarindo and the beaches']),
 ('p', 'A beautiful, peaceful home with income potential and room to grow, offered at ' + PRICE + '. Contact us today for more information or to arrange a private showing.'),
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
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 1,974 m2 (21,257 sq.ft.)</strong></li>\n<li><strong>Construction: 241 m2 (2,600 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 4 | Bathrooms: 4</strong></li>\n<li><strong>Pool | Guest Casita | Gated Community | Furnished | BBQ Area</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>Land: 1,974 m2 | 4 Bedrooms | 4 Bathrooms | Pool | Guest Casita</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">New modern single level home with a separate guest casita, pool and almost half an acre of gardens, in a gated community with clubhouse a short drive from Tamarindo and the beaches. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/modern-home-casita-tamarindo/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
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
