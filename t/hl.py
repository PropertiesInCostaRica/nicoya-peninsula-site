# -*- coding: utf-8 -*-
# Agrega una lista "Highlights" a paginas de propiedades (diseno nuevo o viejo).
# Uso: python3 hl.py            (aplica todas las de la lista)
#      python3 hl.py --test     (solo muestra que haria)
import re, sys, os, time, shutil

W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/hl-' + time.strftime('%Y%m%d%H%M') + '/'
TEST = '--test' in sys.argv

HL = {
'properties/caribe/for-sale/rental-haven.html': [
 '10 fully furnished units: studios, 1, 2 and 3 bedroom floor plans',
 'Capacity for 35 guests with a proven rental history and great reviews',
 'Office with private bathroom and a spacious laundry room',
 'Short stroll to the beach in Playa Chiquita, surrounded by jungle',
 'Turnkey: keep a unit for yourself and rent the rest'],
'properties/playa-negra/for-sale/garden-apts.html': [
 'Duplex with two apartments, each with 2 bedrooms and 1 bathroom',
 'Short walk to the volcanic black sand beach of Playa Negra',
 'Large terraces with hammocks for sunrise and sunset',
 'Walking distance to supermarkets, restaurants and the bus stop',
 'Option to buy 500+ m2 of adjacent land with a barbecue area'],
'properties/bahia-ballena/for-sale/secluded-paradise.html': [
 '34 hectares (84 acres) in Tierras Morenas, Savegre',
 'Ocean views, close to Dominical and Marino Ballena National Park',
 'Rolling hills, flat areas and fertile farmland with mature fruit trees',
 'Fresh spring water and river access',
 'Classic Costa Rican style house on the property',
 'Ideal for a private estate or a boutique eco resort'],
'properties/osa/for_sale/amazing-views-lot-in-the-pacific.html': [
 '266 acres (108 hectares) in the Escaleras community',
 'Ocean and coastline views from Dominicalito up to Manuel Antonio',
 'Private road already cut with several finished building sites',
 'Two year round streams',
 'About 1 km from Playa Dominicalito, 5 minutes to Dominical, 10 to Uvita',
 'Suited for luxury homes, villas, condominiums or a resort hotel'],
'properties/samara/for-sale/beautiful-sunsets-view-home.html': [
 'A few steps from Playa Samara',
 '1,181 m2 lot with tropical gardens and plenty of privacy',
 'Pool with a rancho area and covered corridors around the house',
 '2 bedrooms with an open living and dining area',
 'Short walk to groceries, restaurants, pharmacy and town'],
'properties/nicoya_peninsula/for_sale/serene-views.html': [
 'Modern 4 bedroom, 2 bathroom home with sea views',
 'Fully furnished, air conditioned and in new condition',
 'Within 5 minutes of the beach',
 'Open plan kitchen with top appliances and a breakfast area',
 'Large terrace and a private subtropical garden',
 'Located in the Nicoya Peninsula Blue Zone'],
'properties/puntarenas/for_sale/peaceful-quintas.html': [
 'Quintas of about 5,000 m2 (1.24 acres) each in Miramar',
 'Water and electricity available, ready to build',
 'Quiet countryside setting with ocean breezes',
 'About 15 to 20 minutes to Playa Doña Ana',
 'About 25 minutes to Playa Caldera'],
'properties/nicoya_peninsula/for_sale/mountains-beyond.html': [
 'About 7,000 m2 of land surrounded by natural jungle',
 'Valley and mountain views with no direct neighbors',
 '30 m2 infinity pool with natural Coralina stone',
 '40 m2 Mediterranean style teak terrace with arches',
 'Water from the property\'s own sources',
 '10 minutes to Playa Carrillo, 20 minutes to Samara'],
'properties/hacienda_pinilla/for_sale/premier-villa.html': [
 'Over 5,000 sq.ft. on two floors in Malinches del Mar, Hacienda Pinilla',
 '4 bedrooms and 4.5 bathrooms, professionally furnished',
 'Second floor jacuzzi with dry forest views',
 'Spanish Colonial design with large windows and natural light',
 'Hacienda Club access: fitness room, infinity lap pool, covered garages'],
'properties/caribe/for-sale/bright-light.html': [
 'Modern home in Cocles, Puerto Viejo, close to the beach',
 '2 bedrooms and 1 bathroom with high ceilings',
 'Open American style kitchen with integrated living and dining',
 'Social areas open to a terrace and landscaped garden'],
'properties/nicoya_peninsula/for_sale/cozy-home.html': [
 '6.4 hectares (15.8 acres) in Las Delicias de Cóbano',
 'Mediterranean style home with ocean views from every room',
 '3 bedrooms and 3 bathrooms, about 600 m2 of construction',
 'Rooftop terrace for sunsets',
 'Near Montezuma and Santa Teresa, in the Nicoya Blue Zone'],
'properties/tamarindo/for_sale/develop.html': [
 'Over 6 acres of undisturbed land 5 minutes from Tamarindo',
 'Mostly flat with a small central hill',
 'Short drive to Avellanas, Flamingo and Playa Grande',
 'Less than an hour from Liberia International Airport',
 'Borders the Rancho Villarreal development'],
'properties/caribe/for-sale/dream-land.html': [
 'Mixed use land between Cahuita and Puerto Viejo',
 'Over 200 meters of main road frontage plus a private easement',
 'Water, electricity and internet available',
 'Gentle slope with natural drainage',
 'Organic banana plantation on the property',
 'Options of 25,000 m2 or 50,000 m2'],
'properties/central_pacific/for_sale/breathtaking-ocean-views-house.html': [
 'Main house plus guest house, 760 m2 in total',
 '8 bedrooms, 4 kitchens and 4 living rooms',
 'Infinity pool overlooking the Pacific Ocean',
 'Covered terraces for sunsets',
 'Only 10 minutes from Jaco Beach'],
'properties/tambor/for_rent/ultimate-estate.html': [
 'Newly renovated 12,500 sq.ft. beachfront villa in Tambor',
 '7 bedrooms, 8 bathrooms, sleeps 18',
 'Three level deck system for events and relaxing',
 'Whale watching observatory and sunset bar',
 'Ideal for weddings, corporate retreats and recording sessions'],
'properties/tortuguero/for_sale/priceless.html': [
 '20 steps from the Caribbean Sea',
 '5 room lodge with a rental history',
 '2 minutes from Tortuguero Village, 3 minutes from the National Park',
 'Newly built with wood and concrete',
 'Space to add a cocktail room and 2 to 4 more rooms'],
'properties/guanacaste/for_sale/new-magnificently-design.html': [
 'Brand new hilltop home in a gated community in Playa Grande',
 'Ocean and sunset views through floor to ceiling windows',
 '4 bedrooms plus an office or guest room, each with its own bathroom',
 'Pool by the creek with outdoor dining and a built in barbecue',
 '3 car garage and laundry room'],
'properties/dominical/for_sale/ultimate_parcel_of_land.html': [
 '60.5 acres of rainforest bordering Baru National Park',
 '5 acres of flat commercial land with 342 meters on the coastal highway',
 'Extraordinary ocean views',
 'Two streams born on the property, waterfalls near the road',
 '5 minute walk to Guapil Beach, 2.5 km north of Dominical'],
'properties/guanacaste/for_sale/parcel-ready-to-build.html': [
 '1,455 m2 flat parcel in a gated community',
 'Close to Playa Carrillo and Samara',
 'Power, water and rain drainage in place',
 'Manicured grounds with shade trees',
 'Room for a home, yard and pool'],
'properties/samara/for-sale/ocean-view-oasis.html': [
 'Panoramic ocean views in Camaronal, Samara',
 '4 bedrooms and 3 bathrooms on 2,083 m2',
 'Main house with high ceilings and a cupola for natural airflow',
 'Separate master suite with its own kitchen, great for guests or rental',
 'Large pool and a separate caretaker residence'],
'properties/paquera/for-sale/revenue-home.html': [
 '6 rental units built from three 40 foot shipping containers',
 'Some units already producing income, the rest close to finished',
 '730 m2 lot on the main road in Playa Organos',
 '1 km from the beach, about 10 minutes from the Paquera Ferry',
 'Ample guest parking'],
'properties/tambor/for_sale/corner-house.html': [
 'Corner lot backing onto the 8th hole of Los Delfines Golf & Country Club',
 '3 bedrooms and 3 bathrooms on 1,000 m2',
 '15KW solar system with battery backup',
 'Kitchen with solid wood cabinets and granite counters',
 'New air conditioning in every bedroom'],
'properties/paquera/for-sale/free-standing-bungalow.html': [
 'Fully furnished 3 bedroom bungalow in Paquera',
 'Already operating on Airbnb and VRBO',
 'Freshly painted, move in ready',
 'Private backyard with fire pit and a mature mango tree',
 'Two air conditioning units'],
'properties/paquera/for-sale/vacation-getaway.html': [
 'Affordable 2 bedroom home on 340 m2',
 'Large front yard with room for a pool or casita',
 'Fully fenced with a steel gate on a quiet dead end street',
 '5 minutes to groceries, clinic and schools',
 '15 minutes to the Paquera Ferry'],
'properties/tambor/for_sale/renovated-hotel.html': [
 '12 room hotel on about 949 m2 in Playa Tambor',
 'Municipal hotel authorization and current Health Ministry permit',
 'Sold with furnishings, mattresses and linens',
 'Pool, two kitchens and a large community room',
 'Starlink internet and on site parking'],
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
