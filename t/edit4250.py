#!/usr/bin/env python3
# #4250 Paquera lot: new text (Vainilla, Los Delfines, ferry, Blue Zone) plus area photos from #3315 and #1372.
# Preview: python3 edit4250.py      Apply: python3 edit4250.py --aplicar
import os, re, shutil, sys, time
W = '/var/www/propertiesincostarica.com/web/'
REL = 'properties/paquera/for-sale/paquera-lot.html'
PAGES = ['tambor_real_estate.html', 'nicoya_peninsula_real_estate.html', 'residential_lots.html']
APPLY = '--aplicar' in sys.argv
OLD_T = 'Building Lot of 8,444 m2 in Paquera, Nicoya Peninsula'
NEW_T = 'Building Lot of 8,444 m2 in Vainilla, Paquera, Nicoya Peninsula'
OLD_C = 'Over 2 acres in Paquera on the southern Nicoya Peninsula, close to Tambor beaches and Curu Wildlife Refuge. Room for a home, retreat or eco project.'
NEW_C = 'Over 2 acres in the small town of Vainilla, near Los Delfines, Tambor and the Paquera ferry. Room for a home, retreat or eco project in the Blue Zone.'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/paquera-lot/opt/'
ALT = 'Lot for sale, Vainilla, Paquera, Puntarenas, Nicoya Peninsula, near Los Delfines and Tambor, Blue Zone, Costa Rica'
IMG = W + 'properties/Images/paquera-lot/opt/'
EXTRA = [  # (new number, source big photo, source thumb): #3315 photos 1,5,6,7 and two from #1372
 (5, 'properties/Images/personal-paradise/opt/Image2.jpg', 'properties/Images/personal-paradise/opt/thumbs/Image2.jpg'),
 (6, 'properties/Images/personal-paradise/opt/Image19.jpg', 'properties/Images/personal-paradise/opt/thumbs/Image19.jpg'),
 (7, 'properties/Images/personal-paradise/opt/Image17.jpg', 'properties/Images/personal-paradise/opt/thumbs/Image17.jpg'),
 (8, 'properties/Images/personal-paradise/opt/Image14.jpg', 'properties/Images/personal-paradise/opt/thumbs/Image14.jpg'),
 (9, 'properties/Images/beautifullnwidendless/add/02.jpg', 'properties/Images/beautifullnwidendless/add/thumbs/02.jpg'),
 (10, 'properties/Images/beautifullnwidendless/add/03.jpg', 'properties/Images/beautifullnwidendless/add/thumbs/03.jpg'),
]
for n, big, th in EXTRA:
    for p in (big, th):
        if not os.path.exists(W + p): raise SystemExit('No encuentro la foto ' + p)
print('%d fotos de la zona encontradas' % len(EXTRA))
CAP = '<p><em>Photos of the surrounding area.</em></p>'
def ph(nums, first=False):
    a = ''.join('<a href="%s%d.jpg"><img src="%sthumbs/%d.jpg" alt="%s" width="250" height="187"></a>' % (CDN, k, CDN, k, ALT) for k in nums)
    if first: a += '\n<span class="to_enlarge">Click on the pictures to enlarge</span>'
    return '<p class="photo">\n' + a + '\n</p>'
CONTENT = '\n'.join([
 '<p>In the small town of Vainilla, just outside Paquera on the southern Nicoya Peninsula, this lot of 8,444 m2 (over 2 acres) offers room for a home, a vacation retreat or a long term investment. It is offered at US$89,000, about US$10.50 per m2.</p>',
 ph([1, 2, 4], True),
 '<h2>Near Los Delfines and Tambor</h2>',
 '<p>The lot is a short drive from the Los Delfines golf and beach community in Tambor. Nearby you will find the calm waters of Tambor Bay, Playa Pochote, Playa Muertos, Playa Quesera and Curu Wildlife Refuge.</p>',
 '<h2>Things to Do Around Vainilla</h2>',
 '<p>Vainilla is a peaceful base for exploring the peninsula: horseback rides, ATV tours, waterfall hikes, boat trips to Isla Tortuga and night tours to see the glowing bioluminescent water. The town also keeps its traditions alive with community activities and local festivals.</p>',
 ph([5, 6, 7]),
 ph([8, 9, 10]),
 CAP,
 '<h2>Easy Access by Ferry</h2>',
 '<p>The Paquera ferry connects the peninsula with Puntarenas and the rest of the country, so you can arrive from San Jose without driving around the gulf, while Vainilla keeps its quiet, rural character.</p>',
 '<h2>A Real Blue Zone Experience</h2>',
 '<p>Life in Vainilla follows the relaxed rhythm of the Nicoya Peninsula Blue Zone, known around the world for its long lived, healthy communities. Montezuma and Santa Teresa, with their beaches, restaurants and surf, are within driving distance.</p>',
 '<h2>Room to Build</h2>',
 '<p>With 8,444 m2 (90,890 sq.ft.) there is space for a private residence, a family compound, gardens or a small eco project, subject to local permits.</p>',
 '<p><strong>Property Highlights</strong></p>\n<ul>\n<li>Lot of 8,444 m2 (90,890 sq.ft.), over 2 acres</li>\n<li>Vainilla, Paquera, southern Nicoya Peninsula</li>\n<li>Near Los Delfines, Tambor Bay, Playa Pochote, Playa Quesera and Curu Wildlife Refuge</li>\n<li>Horseback riding, waterfalls, Isla Tortuga and bioluminescence tours nearby</li>\n<li>Access through the Paquera ferry from Puntarenas</li>\n<li>Close to Montezuma and Santa Teresa</li>\n<li>In the Nicoya Peninsula Blue Zone</li>\n<li>About US$10.50 per m2</li>\n</ul>',
 '<p>Offered at US$89,000. Contact Properties in Costa Rica for more details or to plan a visit.</p>',
])
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s): open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
B = '/root/respaldos/edit4250-' + time.strftime('%Y%m%d%H%M') + '/'
s = rd(W + REL)
s2, n = re.subn(r'(<!-- InstanceBeginEditable name="content" -->).*?(<!-- InstanceEndEditable -->)', lambda m: m.group(1) + '\n' + CONTENT + '\n' + m.group(2), s, count=1, flags=re.S)
if n != 1: raise SystemExit('No encontre el contenido')
s2 = s2.replace(OLD_T, NEW_T).replace('Paquera, Puntarenas, Nicoya Peninsula, land for sale near Tambor and Curu', 'Vainilla, Paquera, Puntarenas, Nicoya Peninsula, near Los Delfines and Tambor, Blue Zone')
s2 = s2.replace('<li><strong>Paquera | Southern Nicoya Peninsula | Near Tambor</strong></li>', '<li><strong>Vainilla, Paquera | Near Los Delfines | Blue Zone</strong></li>')
s2 = s2.replace('Lot of 8,444 m2 (over 2 acres) for sale in Paquera on the southern Nicoya Peninsula, near Tambor and Curu Wildlife Refuge.', 'Lot of 8,444 m2 (over 2 acres) for sale in Vainilla, Paquera, near Los Delfines, Tambor and the Paquera ferry, in the Nicoya Peninsula Blue Zone.')
print('Pagina: cambios listos' + (' (titulo nuevo: %s)' % NEW_T))
todo = [(REL, s2)]
for f in PAGES:
    t = rd(W + f)
    if OLD_T not in t and OLD_C not in t: print('sin tarjeta: ' + f); continue
    t2 = t.replace(OLD_T, NEW_T).replace(OLD_C, NEW_C).replace('<li><strong>Paquera | Near Tambor</strong></li>', '<li><strong>Vainilla, Paquera | Near Los Delfines</strong></li>')
    todo.append((f, t2)); print('Tarjeta a cambiar: ' + f)
if not APPLY:
    print('Vista previa. Para aplicar: python3 edit4250.py --aplicar'); raise SystemExit
os.makedirs(B, exist_ok=True)
for n, big, th in EXTRA:
    shutil.copy2(W + big, IMG + '%d.jpg' % n)
    shutil.copy2(W + th, IMG + 'thumbs/%d.jpg' % n)
print('Fotos copiadas')
for f, t in todo:
    shutil.copy2(W + f, B + f.replace('/', '_'))
    wr(W + f, t)
OP = 'In the small town of Vainilla, just outside Paquera on the southern Nicoya Peninsula, this lot of 8,444 m2 (over 2 acres) offers room for a home, a vacation retreat or a long term investment. It is offered at US$89,000, about US$10.50 per m2.'
code = ("from django.db import connection\nc = connection.cursor()\n"
        "c.execute('UPDATE listing_listing SET title=%%s, header=%%s, meta_title=%%s, opening_paragraph=%%s, meta_description=%%s WHERE id_code=4250', [%r, %r, %r, %r, %r])\n"
        "try:\n    connection.commit()\nexcept Exception: pass\nprint('@@buscador actualizado')\n") % (NEW_T, NEW_T, NEW_T, OP, OP[:160])
open('/tmp/edit4250_db.py', 'w').write(code)
os.system('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/edit4250_db.py 2>&1 | grep -o -E "@@.*|rror.*" | sed "s/^@@//"')
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO. Respaldos en ' + B)
