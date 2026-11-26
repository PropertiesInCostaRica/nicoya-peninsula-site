#!/usr/bin/env python3
# New listing #4243: Turnkey Modern Pool Home, Walk to Tamarindo
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/tamarindo-pool-home.html'
PAGE = W + REL
IMGD = W + 'properties/Images/tamarindo-pool-home/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/tamarindo-pool-home/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4243/'
B = '/root/respaldos/list4243-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4243'
TITLE = 'Turnkey Modern Pool Home in a Gated Community, Walk to Tamarindo'
PRICE = 'US$779,000'
ALT = 'Modern home, pool, 3 bedrooms, gated community, walk to Tamarindo beach, Guanacaste, house for sale, Costa Rica'
DESC = 'Turnkey modern 3 bedroom home with private pool in a small gated community within walking distance of Tamarindo town and beach, Guanacaste. ' + PRICE + '.'
PH = {
 'a':'1CksQ6sxyUdoS5O33xtMUYalalHb7Z456','b':'1fKjwcimhJUxaM-3P-G1nBnz7mMcxIPVK','c':'1wYVefUEk9XMqeMRJRH955VOfgbcw00ub',
 'd':'12pRm8Cp3qpODnKudP11H2xOyIW89SpG8','e':'1zf5exvn28oyfGZuyY4vLKsw-LdZg0SoE','f':'1YoSJm5xk6fINCq4yUs6x3BrLu39hPZWx',
 'g':'1Hea4L2xkk3LsO9gEqq9GHjx-e3GBIvUb','h':'1GNAF93XriLDZDpZe6Bt0EntCA7cVsrun','i':'14Pus905wDA35pmfC5-YzHZq0yEu45bB5',
 'j':'1KEVtDB7DT44ZAzeQ6bmuPLrUrjMSPwYi','k':'122UESInpYeRcQdAwbUx33K0I_tyIvIFK','l':'1aXeQD6tOKC6yihWCfP5LCNOSu1zP-qi5',
 'm':'1cev1aQp1QhqcEzXA7UEMgavj5agpxQzv','n':'1jJ2P4IBuzeao1X55HA_lY0a-uUx8Rvyx','o':'15bgvdwN0iSZwHjCMYDWHitJ2Dwfd5BG_',
 'p':'11nyTYrAXEdVUARn58jA3EFK0i0fEhpLy',
}
BLOCKS = [
 ('p', 'Finished in 2022 and sold fully furnished, this modern two level home sits inside a small, quiet gated community from which you can walk to the restaurants, shops and beach of Tamarindo, Guanacaste. Polished concrete, warm tropical wood and wide glass openings give it a clean, contemporary look, and the private pool and garden make it feel like a retreat the moment you arrive.'),
 ('ph', [['a', 'b', 'c']]),
 ('h2', 'Indoor and Outdoor Living as One'),
 ('p', 'Large tempered glass windows and folding accordion doors open the living and dining areas completely to the pool and garden. The kitchen features black granite counters and custom wood cabinetry, and much of the furniture and the built ins were made to measure for the house. A covered barbecue area beside the pool is the natural spot for sunset dinners with family and friends.'),
 ('ph', [['h', 'g', 'd'], ['e', 'f', 'i']]),
 ('h2', '3 Bedrooms | 2.5 Bathrooms'),
 ('p', 'The primary suite is on the main floor, with its own bathroom and direct views of the garden. Upstairs you will find two more bedrooms that share a full bathroom, a powder room and an open office area that is ideal for working from home. Inverter air conditioning keeps the home comfortable while saving energy.'),
 ('ph', [['j', 'l', 'k'], ['m', 'o', 'n']]),
 ('h2', 'Solid, Low Maintenance Construction'),
 ('p', 'The house is built with a monolithic system of polished precast concrete walls, roofed with durable tiles made from recycled plastic and wired to US electrical standards. A storage shed keeps surfboards and beach gear organized. Monthly HOA fees are around US$110, which keeps the community tidy and secure.'),
 ('ph', [['p']]),
 ('ul', ['Modern home completed in 2022, sold turnkey and furnished',
         '3 bedrooms and 2.5 bathrooms, primary suite on the main floor',
         'Private pool, garden and covered barbecue area',
         'Accordion glass doors opening the living area to the pool',
         'Kitchen with black granite counters and custom cabinetry',
         'Upstairs open office space, inverter air conditioning',
         'Precast concrete construction, recycled plastic roof tiles, US standard electrical',
         'Lot of 490 m2 (5,274 sq.ft.), home of 160 m2 (1,722 sq.ft.)',
         'Small gated community, walking distance to Tamarindo town and beach']),
 ('p', 'An easy, move in ready home in one of the most popular beach towns in Costa Rica, ideal as a residence, a vacation home or a rental, offered at ' + PRICE + '. Contact us today for more information or to arrange a private showing.'),
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
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 490 m2 (5,274 sq.ft.)</strong></li>\n<li><strong>Construction: 160 m2 (1,722 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 3 | Bathrooms: 2.5</strong></li>\n<li><strong>Pool | Gated Community | Furnished | A/C | Walk to Town and Beach</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>Land: 490 m2 | 3 Bedrooms | 2.5 Bathrooms | Pool | Gated Community</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">Turnkey modern home built in 2022 with a private pool, BBQ area and glass doors to the garden, in a small gated community within walking distance of Tamarindo town and beach. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/tamarindo-pool-home/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
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
