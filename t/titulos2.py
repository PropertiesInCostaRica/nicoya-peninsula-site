#!/usr/bin/env python3
# New Google titles and descriptions (with starting price) for 6 pages. Backup first.
import os, re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
bk = '/root/respaldos/titulos2-' + time.strftime('%Y%m%d-%H%M%S') + '/'
os.makedirs(bk)
NEW = {
 'homes.html': ('Homes for Sale in Costa Rica from US$79K, 74 Listings | PCR',
   '74 houses and condos for sale across Costa Rica from US$79,000. Beach, mountain and Central Valley homes with photos, prices and bilingual agents since 1999.'),
 'region_and_price/index.html': ('Costa Rica Homes by Price: Under US$100K to Luxury | PCR',
   'Find Costa Rica homes and land by budget, from under US$100,000 to luxury estates. Beach, mountain and Central Valley listings with photos and prices.'),
 'beach/homes_condos.html': ('Costa Rica Beach Houses and Condos from US$135K | PCR',
   'Beach houses and condos for sale in Costa Rica from US$135,000 in Guanacaste, the Nicoya Peninsula and the Pacific coast. Ocean views, photos and prices.'),
 'mountain.html': ('Costa Rica Farms and Mountain Homes from US$65K | PCR',
   'Farms, fincas and mountain homes for sale in Costa Rica from US$65,000. Cool climate and valley views, with size, location and price on every listing.'),
 'beach.html': ('Costa Rica Beach Property for Sale from US$72K | PCR',
   'Beachfront and ocean view homes, condos and lots in Costa Rica from US$72,000, in Guanacaste, the Nicoya Peninsula, the Central Pacific and the Caribbean.'),
 'homes/ocean_view_homes.html': ('Ocean View Homes in Costa Rica from US$120K | PCR',
   'Ocean view homes for sale in Costa Rica from US$120,000, with Pacific sunset views in Tambor, Guanacaste and the Central Pacific. Photos and prices.'),
}
for rel, (t, d) in NEW.items():
    p = W + rel
    if not os.path.exists(p):
        print(rel + ': no existe'); continue
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    s2, n1 = re.subn(r'(<title>)[\s\S]*?(</title>)', lambda m: m.group(1) + t + m.group(2), s, count=1, flags=re.I)
    s2, n2 = re.subn(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1) + d + m.group(2), s2, count=1, flags=re.I)
    if not n2:
        s2 = re.sub(r'(</title>)', lambda m: m.group(1) + '\n<meta name="description" content="' + d + '">', s2, count=1, flags=re.I); n2 = 1
    if n1 != 1 or '</title>' not in s2.lower():
        print(rel + ': no encontre el titulo, sin cambio'); continue
    shutil.copy(p, bk + rel.replace('/', '__'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
    print(rel + ': ' + t)
print('LISTO. Respaldo en ' + bk)
