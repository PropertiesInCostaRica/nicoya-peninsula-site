#!/usr/bin/env python3
# New listing #4247: New Golf View Residence with Pool and Elevator near Playa Conchal
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/golf-view-residence-conchal.html'
PAGE = W + REL
IMGD = W + 'properties/Images/golf-view-residence-conchal/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/golf-view-residence-conchal/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4247/'
B = '/root/respaldos/list4247-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4247'
TITLE = 'New Golf View Residence with Pool and Elevator near Playa Conchal'
PRICE = 'US$3,250,000'
ALT = 'New luxury residence, golf view, pool, elevator, 5 bedrooms, gated community, Playa Conchal, Guanacaste, house for sale, Costa Rica'
DESC = 'Newly built 5 bedroom luxury residence with golf course views, pool, fire pit and private elevator in a gated beach and golf community at Playa Conchal, Guanacaste. ' + PRICE + '.'
PH = {'001': '1Kv_t0295C5q0dFByHmT2eFfYoQzeFGAE', '0021': '14Xmzs0BTfTDVjJGPB-LL__rMk55wPR_g', '003': '1avD64tthtkMe3COpIWN8yP1cKhZ15DY2', '004': '1VkCguUaDmokHt4TUOWJIZFSFTP5Ds0xo', '005': '1ykb8MQoXqVEjxOEJ91k65rRkS3Ytc8Ig', '006': '1Y5u92lyxG5AHG1XEuIrpJY-JTaK2F_X4', '007': '1z4Z-04zF2QgmruX_DbUXRiDqGCqgv116', '008': '140RsdgEMypf0ttw11ovoVL0DZRNTcggq', '009': '1PmGuIrpOAxSqzXvLLyvk99GpYXH5i9mz', '010': '1lr4lJ2AvPwkgEyqsd4aBRmHpySkOvAxZ', '011': '1QXbZ5U5Nn1LEhgf0Uah8HhBAbFwyK8LP', '012': '14Tvv50ZLxmWqVz8KYipSPr8D4nG7buzl', '013': '1ydM6tOJj68Cqbc5hk8JzgTYu2894Zp3j', '014': '16DSKDWt_Z1j4u5SisMkBsa0F6oejmjdV', '015': '1pXNuSn0fyvgMFYeMJNWH0a70FwXwdF5C', '016': '1c64mVsXhzUpbIQJT2-azsIOI_ASQydss', '017': '1sJIFUq5_j3qLX7X1Nk00mFQkT0IbRH9P', '0171': '1bxDF_hiBxD9WB9PCYHMi-Imw_timGCaK', '0172': '1PjKbp_mVrnIOf7FMGb6VV5XxduJufHUA', '018': '1v0Z4QFFtTGN3okcYhg-1Z43RKszqkhoE', '0182': '1UeFaUf3hotYuhVtVzzj3sGHnUj1vLcmF', '019': '15HVxLy6s5e_zq2arGiZ4qj9Ff63jN9fh', '021': '1C5UCxpsUxm0O0WSr-fnLkRkEEIxHF8kQ', '023a': '1eRjzT0hp4WQgZfGVCGft9NGS4tcWXxuU', '023b': '1X9qbllinw9dkJShwB85IKZi9uaI8apDn', '025': '1GjB8aqqss61s-y0XVSnJjyVBDq8ql7eN', '030': '14yFfZsPnPmNqA6qDSMvGORUoZVVQEFBy'}
BLOCKS = [
 ('p', 'Bright, open and full of perspective, this brand new two level residence looks out over the green fairways of a championship golf course inside a gated beach and golf community at Playa Conchal, one of the most beautiful white sand beaches in Costa Rica. Expansive windows bring the sky, the greens and the surrounding trees right into the home.'),
 ('ph', [['001', '0021', '011']]),
 ('h2', 'Generous Volume and Natural Light'),
 ('p', 'High ceilings, clean lines and large format windows give every space a calm, balanced feel, and natural light moves through the living areas all day. The open living room, dining area and designer kitchen with its long island connect directly to the outdoor terrace, and a private elevator links both levels quietly and comfortably.'),
 ('ph', [['004', '005', '006'], ['007', '008', '009'], ['010', '003', '012']]),
 ('ph', [['013', '014', '019']]),
 ('h2', '5 Bedrooms | 6.5 Bathrooms'),
 ('p', 'Five bedroom suites offer space and privacy for family and guests. The primary suite opens to the garden and has a spa style bathroom with double vanity, a large walk in shower and a walk in closet.'),
 ('ph', [['015', '016', '021'], ['0171', '0172', '018'], ['0182', '023b', '025']]),
 ('h2', 'Pool, Fire Pit and Resort Living'),
 ('p', 'Outside, a generous swimming pool and a fire pit create the perfect setting for entertaining, quiet afternoons and evenings under the stars. Owners enjoy the community\'s championship golf, beach club and resort amenities, with the turquoise water of Playa Conchal just minutes away. Rental projections are available, and a professional management team is ready to handle short term rentals or full time living.'),
 ('ph', [['017', '023a', '030']]),
 ('ul', ['Newly built luxury residence on two levels with private elevator',
         '5 bedroom suites and 6.5 bathrooms',
         'Views over the fairways of a championship golf course',
         'Swimming pool, fire pit and outdoor terrace',
         'High ceilings, large format windows and designer kitchen',
         'Lot of 1,146 m2 (12,335 sq.ft.), construction of 630 m2 (6,781 sq.ft.)',
         'Gated community with golf, beach club and resort amenities',
         'Minutes to the white sand beach of Playa Conchal',
         'Rental projections and professional management available']),
 ('p', 'A timeless home for family living or high end rentals in one of the most prestigious destinations on the Gold Coast of Guanacaste, offered at ' + PRICE + '. Contact us today for more information or to arrange a private showing.'),
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
 'features': '\n<ul id="data_table">\n<li><strong>Land size: 1,146 m2 (12,335 sq.ft.)</strong></li>\n<li><strong>Construction: 630 m2 (6,781 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 5 | Bathrooms: 6.5</strong></li>\n<li><strong>Golf View | Pool | Elevator | Gated Community | Beach Club</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>Land: 1,146 m2 | 5 Bedrooms | 6.5 Bathrooms | Golf View | Pool</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">Brand new luxury residence with golf course views, pool, fire pit and private elevator in a gated beach and golf community minutes from Playa Conchal. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/golf-view-residence-conchal/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('conchal.html', 'beach.html', 'gated_communities.html', 'homes.html', 'golf_residences.htm'):
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
