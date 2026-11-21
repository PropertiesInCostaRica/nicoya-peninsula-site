#!/usr/bin/env python3
# New Google titles and descriptions for 8 pages. Makes a backup of each page first.
import os, re, shutil, subprocess, time

WEB = '/var/www/propertiesincostarica.com/web'
P = [
    ('homes.html', 'Costa Rica Homes for Sale: 95+ Houses and Condos | PCR',
     'Browse 95+ homes for sale in Costa Rica, from beach houses to Central Valley family homes, with photos, prices and ID codes. Local bilingual agents since 1999.'),
    ('listings.html', 'Costa Rica Real Estate for Sale: All Listings | PCR',
     'See every Costa Rica property for sale and for rent: homes, condos, land, beach and luxury estates. Search by area or price and talk to a local agent.'),
    ('region_and_price/index.html', 'Costa Rica Property for Sale by Region and Price | PCR',
     'Find Costa Rica real estate by region and budget, from under US$100K to luxury estates. Beach, mountain and Central Valley homes and land.'),
    ('beach/homes_condos.html', 'Costa Rica Beach Houses and Condos for Sale | PCR',
     'Beach houses and condos for sale in Guanacaste, the Nicoya Peninsula and the Pacific coast. Ocean views, photos and prices, with local agents since 1999.'),
    ('3dtours.html', 'Costa Rica Homes for Sale with 3D Virtual Tours | PCR',
     'Walk through Costa Rica homes for sale from anywhere with interactive 3D tours. Beach, mountain and city properties with prices and full details.'),
    ('beach_front_properties_only.htm', 'Beachfront Property for Sale in Costa Rica | PCR',
     'Beachfront homes, lots and condos for sale in Costa Rica, steps from the sand. Photos, prices and local agent support.'),
    ('homes/ocean_view_homes.html', 'Ocean View Homes for Sale in Costa Rica | PCR',
     'Ocean view homes for sale in Costa Rica with Pacific sunset views. Houses in Tambor, Guanacaste and the Central Pacific with photos and prices.'),
    ('tamarindo-real-estate.html', 'Tamarindo Real Estate: Homes and Condos for Sale | PCR',
     'Homes, condos and villas for sale in Tamarindo, Guanacaste. Ocean views, close to the beach, shops and Liberia airport. Photos, prices and local agents.'),
]
stamp = time.strftime('%Y%m%d-%H%M%S')
bkdir = '/root/respaldos/titles-' + stamp
os.makedirs(bkdir, exist_ok=True)
D1 = re.compile(r'(<meta\s+name=["\']description["\']\s+content=)(["\'])(.*?)\2', re.I | re.S)
D2 = re.compile(r'(<meta\s+content=)(["\'])(.*?)\2(\s+name=["\']description["\'])', re.I | re.S)
T = re.compile(r'(<title>)(.*?)(</title>)', re.I | re.S)
ok = 0
for rel, title, desc in P:
    f = os.path.join(WEB, rel)
    if not os.path.isfile(f):
        print('NO EXISTE: ' + rel)
        continue
    shutil.copy2(f, os.path.join(bkdir, rel.replace('/', '__')))
    s = open(f, encoding='utf-8', errors='surrogateescape').read()
    s2, nt = T.subn(lambda m: m.group(1) + title + m.group(3), s, count=1)
    s3, nd = D1.subn(lambda m: m.group(1) + '"' + desc + '"', s2, count=1)
    if nd == 0:
        s3, nd = D2.subn(lambda m: m.group(1) + '"' + desc + '"' + m.group(4), s2, count=1)
    if nd == 0:
        s3 = s2.replace('</title>', '</title>\n<meta name="description" content="' + desc + '">', 1)
        nd = 1
    open(f, 'w', encoding='utf-8', errors='surrogateescape').write(s3)
    if nt == 1 and nd == 1:
        ok += 1
    print('%s  titulo:%d descripcion:%d' % (rel, nt, nd))
print('Paginas cambiadas: %d de %d' % (ok, len(P)))
print('Respaldo: ' + bkdir)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
