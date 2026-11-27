# -*- coding: utf-8 -*-
# Agrega una lista "Highlights" a paginas de propiedades (diseno nuevo o viejo).
# Uso: python3 hl.py            (aplica todas las de la lista)
#      python3 hl.py --test     (solo muestra que haria)
import re, sys, os, time, shutil

W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/hl-' + time.strftime('%Y%m%d%H%M') + '/'
TEST = '--test' in sys.argv

HL = {
'properties/nicoya_peninsula/for_sale/thriving-tree-farm.html': [
 '10 hectares (24 acres) of fruit tree farm near Bejuco',
 'Ocean views from hilltops, with several home sites',
 'Year round water well, 70 meters deep, and a river at the base',
 'Private and secluded, with good road access',
 'About 2 miles to Bejuco village and its beaches'],
'properties/uvita/for_sale/refreshing_ocean_breezes_in_luxury_home.html': [
 'Ocean view luxury home in Uvita, Bahia Ballena',
 '4 bedrooms, 4.5 bathrooms and maid\'s quarters',
 '610 m2 of construction on 1.3 hectares (3.2 acres)',
 'Floor to ceiling windows facing the Pacific',
 'Kitchen with granite counters and professional appliances',
 'Minutes to waterfalls, beaches and restaurants'],
'properties/caribe/for-sale/expandable-ocean-views.html': [
 'Ready to build: 1 hectare lot in Punta Uva',
 '85 meters of public road frontage plus an internal road',
 'Water and electricity already installed',
 'Expandable ocean views and a constant breeze',
 'Macaws, toucans, sloths and three monkey species',
 'Ideal for a home, vacation rental or boutique eco hotel'],
'properties/santa_cruz/for_sale/surf.html': [
 '3,098 m2 lot on the main road in Marbella',
 'Less than 3 minutes from one of the area\'s best surf breaks',
 'Quiet, lightly visited beach town',
 'Suited for a vacation home or a commercial project'],
'properties/jaco/for_sale/amazing_boutique_nature_resort.html': [
 'Boutique nature resort on 8 hectares (19 acres) between Orotina and Jaco',
 '7 completed villas plus 3 more between 40 and 80% finished',
 'Each villa on at least half an acre among fruit trees',
 'Kohler fixtures, stainless appliances and air conditioning',
 'Price reduced from US$7,000,000 to US$2,750,000'],
'properties/commercial_and_residential_property.html': [
 '1.7 hectares (4.3 acres) on the main boulevard of Playas del Coco',
 'In the busiest commercial area, next to shops and restaurants',
 'Residential project with a commercial component in permitting',
 'Completely flat land with all services available'],
}
TITLES = {
'properties/nicoya_peninsula/for_sale/thriving-tree-farm.html': 'The Farm at a Glance',
'properties/uvita/for_sale/refreshing_ocean_breezes_in_luxury_home.html': 'What Makes This Home Special',
'properties/caribe/for-sale/expandable-ocean-views.html': 'Why Build Here',
'properties/santa_cruz/for_sale/surf.html': 'Key Features',
'properties/jaco/for_sale/amazing_boutique_nature_resort.html': 'The Resort at a Glance',
'properties/commercial_and_residential_property.html': 'Development Potential',
}
OLD = {}

RX = re.compile(r'(<!-- InstanceBeginEditable name="content" -->)(.*?)(<!-- InstanceEndEditable -->)', re.S)

def block(items, title='Highlights'):
    return ('\n<div class="highlights"><h2>' + title + '</h2>\n<ul>\n' +
            '\n'.join('<li>%s</li>' % x for x in items) + '\n</ul></div>\n')

def insert(c, items, title):
    # despues del primer parrafo con texto de verdad
    for m in re.finditer(r'</p>', c, re.I):
        txt = re.sub(r'<[^>]+>', ' ', c[:m.end()])
        txt = re.sub(r'Click on the pictures to enlarge', '', txt)
        if len(re.sub(r'\s+', ' ', txt).strip()) > 150:
            return c[:m.end()] + block(items, title) + c[m.end():]
    return c + block(items, title)

hechas = 0
for p, items in HL.items():
    f = W + p
    if not os.path.exists(f):
        print('NO EXISTE:', p); continue
    t = open(f, encoding='utf-8', errors='surrogateescape').read()
    m = RX.search(t)
    if not m:
        print('SIN REGION content:', p); continue
    if 'class="highlights"' in m.group(2) or re.search(r'highlights', re.sub(r'<[^>]+>',' ',m.group(2)), re.I):
        print('Ya tenia lista:', p); continue
    nc = insert(m.group(2), items, TITLES.get(p, 'Highlights'))
    nt = t[:m.start(2)] + nc + t[m.end(2):]
    if TEST:
        print('Haria:', p); continue
    os.makedirs(B, exist_ok=True)
    shutil.copy2(f, B + p.replace('/', '_'))
    open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt)
    hechas += 1
    print('Lista nueva: https://www.propertiesincostarica.com/' + p)

# titulos nuevos para las listas del primer grupo
for p, title in OLD.items():
    f = W + p
    if not os.path.exists(f): continue
    t = open(f, encoding='utf-8', errors='surrogateescape').read()
    nt = t.replace('<div class="highlights"><h2>Highlights</h2>', '<div class="highlights"><h2>' + title + '</h2>')
    if nt != t and not TEST:
        os.makedirs(B, exist_ok=True); shutil.copy2(f, B + p.replace('/', '_') + '.t')
        open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt)
        print('Titulo nuevo:', title, '|', p)
print('Listas agregadas:', hechas, '| respaldo en', B)
print('LISTO')
