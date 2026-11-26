#!/usr/bin/env python3
# New listing #4248: Classic Coastal Villa Steps from the Sand near Playa Avellanas
import os, re, shutil, subprocess, time
from PIL import Image
try:
    from PIL import ImageOps
except ImportError:
    ImageOps = None
W = '/var/www/propertiesincostarica.com/web/'
SRC = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
REL = 'properties/guanacaste/for_sale/beach-villa-avellanas.html'
PAGE = W + REL
IMGD = W + 'properties/Images/beach-villa-avellanas/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/beach-villa-avellanas/opt/'
URL = 'https://www.propertiesincostarica.com/' + REL
TMP = '/root/list4248/'
B = '/root/respaldos/list4248-' + time.strftime('%Y%m%d%H%M') + '/'
for d in (IMGD + 'thumbs', TMP, B): os.makedirs(d, exist_ok=True)
if os.path.exists(PAGE): raise SystemExit('Ya existe ' + PAGE)
CODE = '4248'
TITLE = 'Classic Coastal Villa Steps from the Sand near Playa Avellanas'
PRICE = 'US$4,950,000'
ALT = 'Luxury beach villa, pool, 4 bedrooms, gated resort community, Playa Avellanas, Tamarindo, Guanacaste, house for sale, Costa Rica'
DESC = 'Elegant 4 bedroom villa with pool, jacuzzi and putting green, moments from a private beach entrance in a gated beach and golf resort community near Tamarindo, Guanacaste. ' + PRICE + '.'
PH = {'0': 'https://uploadcare.engelvoelkers.com/8133eebf-deba-4933-96bb-c47a740d4f5b/-/format/jpeg/-/quality/best/', '1': 'https://uploadcare.engelvoelkers.com/00ebb2d6-6c0e-45d4-9f51-8142fa61c7e4/-/format/jpeg/-/quality/best/', '2': 'https://uploadcare.engelvoelkers.com/1a95177d-0cfd-47c8-829d-17e297c8c89c/-/format/jpeg/-/quality/best/', '3': 'https://uploadcare.engelvoelkers.com/47932f0a-d94d-415c-9bf5-171077288733/-/format/jpeg/-/quality/best/', '4': 'https://uploadcare.engelvoelkers.com/1ac5589b-fc59-41a4-ae71-9a6183d6dc96/-/format/jpeg/-/quality/best/', '5': 'https://uploadcare.engelvoelkers.com/73af747c-5b54-471b-b2c6-23e00b5a0dfd/-/format/jpeg/-/quality/best/', '6': 'https://uploadcare.engelvoelkers.com/a118de8a-585f-4660-974d-c5032e99e04a/-/format/jpeg/-/quality/best/', '7': 'https://uploadcare.engelvoelkers.com/7b85f0e2-dd1e-4046-82d9-c9704d37b5d1/-/format/jpeg/-/quality/best/', '8': 'https://uploadcare.engelvoelkers.com/b55da18d-cc4f-4ea2-b2fc-8409c0e2fdee/-/format/jpeg/-/quality/best/', '9': 'https://uploadcare.engelvoelkers.com/0e12a196-77a2-41e0-a960-b360b2c70441/-/format/jpeg/-/quality/best/', '10': 'https://uploadcare.engelvoelkers.com/feed29c6-94ab-4c6b-8a00-01af8ed5f2ce/-/format/jpeg/-/quality/best/', '11': 'https://uploadcare.engelvoelkers.com/2248cc09-bc99-461a-8a91-843da69feadd/-/format/jpeg/-/quality/best/', '12': 'https://uploadcare.engelvoelkers.com/43189393-5fad-4270-bd5d-e214d1a19eeb/-/format/jpeg/-/quality/best/', '13': 'https://uploadcare.engelvoelkers.com/5244196a-0b49-4180-8176-2426b5602b7c/-/format/jpeg/-/quality/best/', '14': 'https://uploadcare.engelvoelkers.com/48903534-1e94-469a-8b0b-1b0efa115cfb/-/format/jpeg/-/quality/best/', '15': 'https://uploadcare.engelvoelkers.com/dfdd4778-9dd9-44be-a8cc-be290d8173a8/-/format/jpeg/-/quality/best/', '16': 'https://uploadcare.engelvoelkers.com/87253d6f-6b9e-474e-b023-0cca0e0fd29a/-/format/jpeg/-/quality/best/', '17': 'https://uploadcare.engelvoelkers.com/5e4575c0-d0d8-4edc-b958-e44b7450d730/-/format/jpeg/-/quality/best/', '18': 'https://uploadcare.engelvoelkers.com/78560455-78e7-4f85-bc6f-afa8d6b8a396/-/format/jpeg/-/quality/best/', '19': 'https://uploadcare.engelvoelkers.com/399aec58-8653-40ba-af47-65e0db600b70/-/format/jpeg/-/quality/best/', '20': 'https://uploadcare.engelvoelkers.com/52ce40ec-210d-488c-ac8c-1eaa6bd8f0c7/-/format/jpeg/-/quality/best/', '21': 'https://uploadcare.engelvoelkers.com/9033368d-b113-43d5-bd59-3d155da8a563/-/format/jpeg/-/quality/best/', '22': 'https://uploadcare.engelvoelkers.com/76bdaa22-63e6-439d-947f-bf4b23512e9d/-/format/jpeg/-/quality/best/', '23': 'https://uploadcare.engelvoelkers.com/ae966ae9-061d-4784-9c0d-53ed9e282d0b/-/format/jpeg/-/quality/best/', '24': 'https://uploadcare.engelvoelkers.com/c7bf017c-c892-4ea9-aa5f-ef536cb06f83/-/format/jpeg/-/quality/best/', '25': 'https://uploadcare.engelvoelkers.com/a81f5688-a83a-47fa-b97c-ec0e3cd47e44/-/format/jpeg/-/quality/best/', '26': 'https://uploadcare.engelvoelkers.com/631fdf90-e3da-477b-8ee8-378cac611c99/-/format/jpeg/-/quality/best/', '27': 'https://uploadcare.engelvoelkers.com/b67e1d48-ca15-4e07-94b9-8901de5afb48/-/format/jpeg/-/quality/best/'}
BLOCKS = [
 ('p', 'Inside one of the most established gated beach and golf resort communities on the Pacific coast near Tamarindo, this elegant villa sits just moments from a private beach entrance. Arched windows, hand painted tiles and warm wood ceilings give it a timeless, Mediterranean inspired character, while every comfort of a modern tropical home is in place.'),
 ('ph', [['9', '0', '8'], ['1', '2', '10']]),
 ('h2', 'Character in Every Detail'),
 ('p', 'The vaulted entry welcomes you with a striking blue and white tiled staircase, and custom windows frame the gardens throughout. Open ceilings finished in wood and teak, classic arches and carefully crafted details make the home feel collected and personal rather than simply decorated.'),
 ('ph', [['13', '15', '16'], ['17', '14', '11']]),
 ('h2', 'Open Living and a Gourmet Kitchen'),
 ('p', 'The gourmet kitchen with granite counters opens to the living and dining areas and to the covered terraces outside, so the house flows easily between indoors and out. A covered outdoor kitchen with grill makes entertaining effortless.'),
 ('ph', [['18', '19', '20'], ['21', '26', '25']]),
 ('h2', '4 Bedrooms | 4.5 Bathrooms'),
 ('p', 'Four bedroom suites offer comfort and privacy for family and guests, each with its own bathroom, plus a powder room for visitors.'),
 ('ph', [['22', '24', '23']]),
 ('h2', 'Pool, Jacuzzi and Putting Green'),
 ('p', 'The long pool with lounging areas, a jacuzzi with waterfall, a fire pit and a private putting green turn the garden into your own resort. Solar panels add efficiency, and there is a two car garage plus a separate single garage for vehicles, storage or a workshop.'),
 ('ph', [['12', '6', '7']]),
 ('h2', 'Resort Living by the Ocean'),
 ('p', 'Residents enjoy private entrances to Playa Avellanas and Playa Mansita, a beach club, a championship golf course, tennis and pickleball, equestrian facilities, more than 45 km of trails and access to a luxury resort and spa. Tamarindo is a short drive away and Liberia International Airport is about an hour and a half by car.'),
 ('ph', [['3', '4', '5'], ['27']]),
 ('ul', ['Elegant villa built in 2022, moments from a private beach entrance',
         '4 bedroom suites and 4.5 bathrooms, sold furnished',
         'Long pool, jacuzzi with waterfall, fire pit and private putting green',
         'Covered outdoor kitchen with grill and covered terraces',
         'Gourmet kitchen with granite counters, wood and teak ceilings',
         'Solar panels, two car garage plus a single garage',
         'Construction of 268 m2 (2,890 sq.ft.)',
         'Gated beach and golf resort community with beach club, tennis, pickleball, equestrian center and trails',
         'Near Playa Avellanas and Tamarindo, about 1.5 hours from Liberia airport']),
 ('p', 'A rare villa that pairs classic charm with beach and resort living on the Gold Coast of Guanacaste, offered at ' + PRICE + '. Contact us today for more information or to arrange a private showing.'),
]
def get(key):
    p = TMP + key + '.jpg'
    if not os.path.exists(p) or os.path.getsize(p) < 10000:
        u = PH[key] if PH[key].startswith('http') else 'https://drive.usercontent.google.com/download?id=%s&export=download&confirm=t' % PH[key]
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
 'features': '\n<ul id="data_table">\n<li><strong>Construction: 268 m2 (2,890 sq.ft.)</strong></li>\n<li><strong>Bedrooms: 4 | Bathrooms: 4.5</strong></li>\n<li><strong>Steps to the Beach | Pool | Jacuzzi | Putting Green | Gated Resort Community</strong></li>\n</ul>\n',
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
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n<div class="listing_img"> <a href="/%s"> <img src="/images/spacer.gif" data-src="%s" alt="%s" border="0" /> </a> <span class="idcodes">ID CODE: #%s</span></div>\n<div class="listing_data">\n<h3><a href="/%s">%s</a></h3>\n<ul>\n<li>4 Bedrooms | 4.5 Bathrooms | Pool | Steps to the Beach | Gated Resort Community</li>\n<li>Sales Price: %s</li>\n</ul>\n<div class="listing_content">Elegant villa with classic architectural details, pool, jacuzzi and putting green, moments from a private beach entrance near Playa Avellanas in a gated beach and golf resort community. <a href="/%s"> More Information... </a> </div>\n</div>\n</article>\n<!--###################FIN#####################-->\n'
        % (REL, 'https://cdn.propertiesincostarica.com/properties/Images/beach-villa-avellanas/p.jpg', TITLE, CODE, REL, TITLE, PRICE, REL))
for f in ('pinilla_real_estate.html', 'tamarindo-real-estate.html', 'beach.html', 'gated_communities.html', 'homes.html', 'golf_residences.htm'):
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
