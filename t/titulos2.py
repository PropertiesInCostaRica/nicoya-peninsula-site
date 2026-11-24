#!/usr/bin/env python3
# TEST: new Google titles and descriptions (with starting price) for 3 pages. Backup first.
import os, re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
bk = '/root/respaldos/titulos2-' + time.strftime('%Y%m%d-%H%M%S') + '/'
os.makedirs(bk)
NEW = {
 'homes.html': ('Homes for Sale in Costa Rica from US$79K, 74 Listings | PCR',
   '74 houses and condos for sale across Costa Rica from US$79,000. Beach, mountain and Central Valley homes with photos, prices and bilingual agents since 1999.'),
 'beach/homes_condos.html': ('Costa Rica Beach Houses and Condos from US$135K | PCR',
   'Beach houses and condos for sale in Costa Rica from US$135,000 in Guanacaste, the Nicoya Peninsula and the Pacific coast. Ocean views, photos and prices.'),
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
