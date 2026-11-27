# -*- coding: utf-8 -*-
# Agrega una lista "Highlights" a paginas de propiedades (diseno nuevo o viejo).
# Uso: python3 hl.py            (aplica todas las de la lista)
#      python3 hl.py --test     (solo muestra que haria)
import re, sys, os, time, shutil

W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/hl-' + time.strftime('%Y%m%d%H%M') + '/'
TEST = '--test' in sys.argv

HL = {
'properties/tamarindo/for_sale/beachfront-condos-in-the-healthiest-place-on-earth.html': [
 '3.2 acre parcel at the edge of the maritime zone, in the Nicoya Blue Zone',
 'Permits for 4 towers of seven stories, originally planned for 44 units',
 'Two towers already built in grey work',
 'Permits and plans approved before height limits changed'],
'properties/flamingo/for_sale/two-fully-titled-lots.html': [
 'Two fully titled ocean view lots on Flamingo\'s northern ridge',
 'Lot 1: 1,177 m2. Lot 2: 832 m2',
 'Close to the new Flamingo Marina',
 'Blue flag beach with white sand and clear water',
 'Convenient to Liberia airport, schools and hospitals'],
'properties/caribe/for-sale/cocles-dwellings.html': [
 'Short walk to Cocles beach',
 'Main house of 80 m2 with high ceilings and quality finishes',
 'Two independent 30 m2 bungalows for guests or rental income',
 'Pool and storage on a 594 m2 lot'],
'properties/osa/for_sale/boutique_villas_nestled_in_the_jungle_with_ocean_views.html': [
 'Fully operational boutique hotel with 14 bungalows',
 'Hilltop pool with ocean views and a sunset rancho',
 'Equipped restaurant on site',
 '3.6 acres of jungle above the Terraba and Tortuga rivers',
 'Easy access from the coastal highway'],
}
TITLES = {
'properties/tamarindo/for_sale/beachfront-condos-in-the-healthiest-place-on-earth.html': 'Development Potential',
'properties/flamingo/for_sale/two-fully-titled-lots.html': 'Why Build Here',
'properties/caribe/for-sale/cocles-dwellings.html': 'Live, Vacation and Earn',
'properties/osa/for_sale/boutique_villas_nestled_in_the_jungle_with_ocean_views.html': 'The Hotel at a Glance',
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
