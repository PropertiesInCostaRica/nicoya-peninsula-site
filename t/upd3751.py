#!/usr/bin/env python3
# #3751: new exclusive listing by Klaudia (Listing System 566). Same page and ID.
# New title, price US$1,200,000, new text, photos split Main House / Casita. Cards updated on listing pages.
import os, re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
P = W + 'properties/nicoya_peninsula/for_sale/abundance.html'
TS = time.strftime('%Y%m%d-%H%M%S')
bk = '/root/respaldos/upd3751-' + TS + '/'
os.makedirs(bk)
OLD_T = 'Turn-Key Ocean View Estate with Guest House and Short Walk to the Beach!'
NEW_T = 'Masterfully Crafted Ocean View Estate in Tango Mar'
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def save(p, s):
    shutil.copy(p, bk + p[len(W):].replace('/', '__'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
def put(s, n, val):
    a = s.index('<!-- InstanceBeginEditable name="%s" -->' % n)
    a = s.index('-->', a) + 3
    e = s.index('<!-- InstanceEndEditable -->', a)
    return s[:a] + val + s[e:]
def get(s, n):
    a = s.index('<!-- InstanceBeginEditable name="%s" -->' % n)
    a = s.index('-->', a) + 3
    return s[a:s.index('<!-- InstanceEndEditable -->', a)]
s = rd(P)
c = get(s, 'content')
B = re.findall(r'<p class="photo">.*?</p>', c, re.S)
B = [re.sub(r'\s*<span class="to_enlarge">.*?</span>', '', b, flags=re.S) for b in B]
vid = re.search(r'<iframe id="video".*?</iframe>', c, re.S)
if len(B) < 9:
    print('Encontre solo %d grupos de fotos, no se cambio nada' % len(B)); raise SystemExit
def ph(*idx): return '\n'.join(B[i] for i in idx)
first = B[0].replace('</p>', '\n  <span class="to_enlarge">Click on the pictures to enlarge</span>\n</p>', 1)
content = '''
''' + first + '''

<p><strong>Exclusive listing.</strong> A beautifully built and lovingly maintained ocean view estate in Tango Mar, with a main house, a detached guest casita and a large swimming pool at the heart of it all, a short walk from the beach.</p>

<h2>Main House | 3 Bedrooms &middot; 3 Bathrooms &middot; 436 m&sup2;</h2>

<p>Open the <strong>solid wood double doors</strong> and look straight through to the pool and the Pacific beyond. You can feel the ocean breeze as you step inside. Built in 2012, the home is arranged in two wings around the <strong>5 &times; 15 m swimming pool</strong>, with a covered ocean view terrace for outdoor dining and lounging.</p>

''' + ph(1, 2) + '''

<p>One wing houses the primary suite, with a walk-in closet and a spacious en suite bathroom. The opposite wing features two additional king size bedrooms with en suite bathrooms, a fully equipped kitchen with two refrigerators and a pantry, and a laundry room with a washer and dryer. Both wings open onto the pool terrace.</p>

''' + ph(3) + '''

<p>The bedrooms can also be reached through a <strong>separate side entrance</strong>, giving renters or older children privacy to come and go independently. Each bedroom has individually controlled air conditioning, a ceiling fan, a TV with satellite service, a telephone and a safe.</p>

''' + ph(4) + '''

<p>The main house also has Starlink internet, solar water heating and a water storage tank with a pump. A changing room, outdoor shower and dedicated equipment room serve the pool area.</p>

''' + ph(5) + '''

<h2>Detached Guest House | 2 Bedrooms &middot; 1 Bathroom &middot; 75 m&sup2;</h2>

<p>Built in 2010, the casita sits higher on the property, with its own tropical garden, a glimpse of the ocean and a <strong>wraparound terrace with hammocks</strong> for reading or taking an afternoon nap. The open plan living and dining area connects to a fully equipped kitchen, so guests can settle in and prepare their own meals.</p>

''' + ph(6) + '''

<p>Both queen bedrooms have air conditioning and ceiling fans. The casita also has a full bathroom, a washer and dryer, an outdoor shower, Starlink internet, solar water heating and its own water storage tank with a pump.</p>

''' + ph(7) + '''

<h2>Tango Mar and the Southern Nicoya Peninsula</h2>

<p>Golf, tennis and oceanfront dining are nearby at Hotel Tango Mar. Take the popular short hike to <strong>Cocolita Falls</strong> or spend the day at nearby <strong>Playa Quizales</strong> or <strong>Playa Tambor</strong>. Cur&uacute;, Cabo Blanco and boat trips to Tortuga Island are also within reach for day trips.</p>

''' + ph(8) + '''

<p>Local grocery shopping is approximately 3 km away, and <strong>C&oacute;bano is about 20 minutes away</strong> for banks, stores, churches and other everyday services. A new medical facility is currently under construction in C&oacute;bano. Both homes receive water from the Tango Mar Water Association.</p>

<p><strong>To arrange a private showing, contact Klaudia Nabialek with Properties in Costa Rica on WhatsApp at +506 8629 3756.</strong></p>

''' + (vid.group(0) if vid else '') + '\n'
s = put(s, 'content', content)
s = put(s, 'title', NEW_T)
s = re.sub(r'<title>.*?</title>', '<title>' + NEW_T + ', ID CODE: #3751</title>', s, count=1, flags=re.S | re.I)
desc = 'Exclusive: masterfully crafted ocean view estate in Tango Mar with a 3 bedroom main house, a 2 bedroom guest casita and a 5 x 15 m pool, a short walk to the beach.'
s = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1) + desc + m.group(2), s, count=1, flags=re.I)
s = put(s, 'price', get(s, 'price').replace('US$1,300,000', 'US$1,200,000'))
s = put(s, 'features', get(s, 'features').replace('Main house: 435 m2 (4,700 sq. ft.)', 'Main house: 436 m2 (4,693 sq. ft.)'))
s = s.replace('value="' + OLD_T + '"', 'value="' + NEW_T + '"')
if 'US$1,200,000' not in s:
    print('No pude cambiar el precio, no se guardo nada'); raise SystemExit
save(P, s)
print('Pagina #3751 actualizada')
# cards on listing pages
n = 0
for root, dirs, files in os.walk(W):
    dirs[:] = [d for d in dirs if d not in ('blog', 'Images', 'images', 'cgi-bin', 'css', 'js', 'properties')]
    for f in files:
        if not f.endswith(('.html', '.htm')): continue
        p = os.path.join(root, f)
        t = rd(p)
        if 'for_sale/abundance.html' not in t: continue
        def fix(m):
            x = m.group(0)
            if 'for_sale/abundance.html' not in x: return x
            return x.replace(OLD_T, NEW_T).replace('US$1,300,000', 'US$1,200,000')
        t2 = re.sub(r'<article class="listing".*?</article>', fix, t, flags=re.S)
        if t2 != t:
            save(p, t2); n += 1
            print('Tarjeta actualizada en ' + p[len(W):])
print('Paginas con tarjeta actualizada: %d' % n)
print('LISTO: https://www.propertiesincostarica.com/properties/nicoya_peninsula/for_sale/abundance.html  (respaldo en ' + bk + ')')
