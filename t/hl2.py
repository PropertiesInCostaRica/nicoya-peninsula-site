# -*- coding: utf-8 -*-
# Agrega una lista "Highlights" a paginas de propiedades (diseno nuevo o viejo).
# Uso: python3 hl.py            (aplica todas las de la lista)
#      python3 hl.py --test     (solo muestra que haria)
import re, sys, os, time, shutil

W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/hl-' + time.strftime('%Y%m%d%H%M') + '/'
TEST = '--test' in sys.argv

HL = {
'properties/hacienda_pinilla/for_sale/charming-colonial-home.html': [
 'Spanish colonial home inside Hacienda Pinilla Beach & Golf Resort',
 '3 bedrooms, each with its own bathroom and walk in closet',
 'Teak floors, vaulted ceilings, wood beams and stone walls',
 'Kitchen with granite counters, breakfast bar and large pantry',
 '2,230 m2 lot with 410 m2 of construction'],
'properties/caribe/for-sale/colorful-vibes.html': [
 '6 tropical bungalows plus a reception building',
 'About 300 meters from the natural pools of Playa Chiquita',
 'Established rental business with a decade of history',
 'Close to restaurants, yoga studios and a supermarket',
 '1,500 m2 lot in the South Caribbean'],
'properties/caribe/for-sale/tranquil-terrain.html': [
 '1,328 m2 flat lot with lush trees in Playa Negra',
 'Gentle creek running behind the property',
 'Quiet residential area, short distance to the beach',
 'Easy access to Puerto Viejo and Hone Creek'],
'properties/caribe/for-sale/paradise-compound.html': [
 '3,400 m2 (3/4 acre) about 1 km from Cocles beach',
 'Main house with 2 bedrooms and 2 bathrooms plus two guest villas',
 'High quality construction with fine woods and luxury finishes',
 'Year round creek and jungle surroundings',
 'Live in the house and earn from the villas'],
'properties/caribe/for-sale/extraordinary-compound.html': [
 'Turnkey compound on 3,000 m2 in Cocles, Puerto Viejo',
 'One level main house with 3 bedrooms and 2 bathrooms',
 '5 bungalows, 2 pools, 2 ranchos and a yoga platform',
 'Gourmet kitchen with top of the line appliances',
 'Income producing property'],
'properties/caribe/for-sale/dream-tropical-jungle.html': [
 '5,000 m2 (1.25 acres) of jungle about 1 mile from Punta Uva Beach',
 'Open loft house with the heavy structure already done',
 'Guest cabin and terrace',
 'Little river along the bottom of the property',
 'Main road access with full privacy inside'],
'properties/tamarindo/for_sale/opportunity.html': [
 '11 hectares (27 acres), 5 minutes from Tamarindo Beach',
 'Over 300 meters of road frontage on fairly flat land',
 'All services on site',
 '2 minutes to supermarkets and commercial centers',
 'About one hour from Liberia International Airport'],
'properties/dominical/for_sale/ocean-view-eco-development-land.html': [
 '33 hectares (81 acres) above Playa Dominicalito in Escaleras',
 'Panoramic ocean and bay views from finished building sites',
 'Interior road built and power to the border',
 'Mature teak, cedar, pochote and guadua bamboo',
 '10 minutes from Dominical'],
'properties/dominical/for_sale/ocean_view_home_and_extra_land.html': [
 'Coastline views of the Whale\'s Tail, Ballena Island and the Osa Peninsula',
 'Duplex wood home of 2,100 sq.ft. with 3 bedrooms',
 'Private studio apartment on the ground floor with its own parking',
 'Large covered balconies',
 'Includes an extra lot, 3,326 m2 in total'],
'properties/caribe/for-sale/caribbean-gem.html': [
 '2 acre jungle compound in Playa Chiquita, steps from the Caribbean',
 'Main house with 3 bedrooms',
 '7 bungalows around a pool',
 'Top rated Italian restaurant on site',
 'Macaws, monkeys and toucans all around'],
'properties/tambor/for_rent/oceanfront-estate.html': [
 'Beachfront estate next to Tango Mar Resort',
 '7 master bedrooms plus a 1 bedroom apartment with kitchen',
 'Over 10,500 sq.ft. of air conditioned space',
 'Beachfront pool and outdoor bar',
 'Dining room for 14, ideal for weddings and retreats'],
'properties/bahia-ballena/for-sale/oceanview-development-lands.html': [
 'Over 9 acres with ocean views, minutes from Uvita',
 'Paved access straight from the Costanera highway',
 'Gated entrance with guard house',
 'Main house with separate master villa, large pool and patio',
 'Seven parcels, including a second house'],
'properties/herradura/for_sale/house_with_pool_and_equine_quarters.html': [
 '2.7 acre property in Herradura',
 '3 bedrooms, 3.5 bathrooms and maid\'s quarters',
 'Swimming pool and vaulted ceilings',
 'Five horse stables with living quarters',
 'Parking for 20 cars'],
}

RX = re.compile(r'(<!-- InstanceBeginEditable name="content" -->)(.*?)(<!-- InstanceEndEditable -->)', re.S)

def block(items):
    return ('\n<div class="highlights"><h2>Highlights</h2>\n<ul>\n' +
            '\n'.join('<li>%s</li>' % x for x in items) + '\n</ul></div>\n')

def insert(c, items):
    # despues del primer parrafo con texto de verdad
    for m in re.finditer(r'</p>', c, re.I):
        txt = re.sub(r'<[^>]+>', ' ', c[:m.end()])
        txt = re.sub(r'Click on the pictures to enlarge', '', txt)
        if len(re.sub(r'\s+', ' ', txt).strip()) > 150:
            return c[:m.end()] + block(items) + c[m.end():]
    return c + block(items)

hechas = 0
for p, items in HL.items():
    f = W + p
    if not os.path.exists(f):
        print('NO EXISTE:', p); continue
    t = open(f, encoding='utf-8', errors='surrogateescape').read()
    m = RX.search(t)
    if not m:
        print('SIN REGION content:', p); continue
    if re.search(r'highlights', m.group(2), re.I):
        print('Ya tiene Highlights:', p); continue
    nc = insert(m.group(2), items)
    nt = t[:m.start(2)] + nc + t[m.end(2):]
    if TEST:
        print('Haria:', p); continue
    os.makedirs(B, exist_ok=True)
    shutil.copy2(f, B + p.replace('/', '_'))
    open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt)
    hechas += 1
    print('Highlights: https://www.propertiesincostarica.com/' + p)

print('Listas agregadas:', hechas, '| respaldo en', B)
print('LISTO')
