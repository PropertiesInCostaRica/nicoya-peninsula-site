#!/usr/bin/env python3
# 1) Better titles, descriptions and H1 on the new design pages (live and previews).
# 2) Publish the new Map page (map-nuevo.html -> map.html), with backup.
import re, shutil, subprocess, time, os
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
FIX = {
 'map-nuevo.html': ('Costa Rica Map: Properties for Sale by Region | PCR',
   'Map of Costa Rica showing the areas where we have homes, land and beach properties for sale, plus directions to our office in Santa Ana.',
   'Costa Rica Map'),
 'financing.html': ('Seller Financing Properties in Costa Rica | PCR',
   'Homes, land and investment properties in Costa Rica with owner financing. See photos, prices and terms, and ask an agent about your options.', None),
 'articles/index.htm': ('Costa Rica Real Estate Articles and Guides | PCR',
   'Guides on buying property in Costa Rica: residency, closing costs, taxes, financing, probate and everyday life, by Properties in Costa Rica.', None),
 'videos/index.html': ('Costa Rica Property Video Tours | PCR',
   'Watch video tours of homes, estates and land for sale in Costa Rica, and contact us to schedule a visit.', None),
 'links-nuevo.html': ('Useful Costa Rica Links for Buyers and Visitors | PCR',
   'Helpful Costa Rica resources for property buyers, visitors and new residents: travel, tours, services and more.', 'Useful Costa Rica Links'),
 'info/sanjose-nuevo.html': ('Downtown San Jose Costa Rica Attractions | PCR',
   'Museums, theatres, parks and markets to visit in downtown San Jose, Costa Rica, from the National Theatre to the Central Market.', 'Downtown San Jose Attractions'),
}
os.makedirs('/root/respaldos/titulos-' + ts, exist_ok=True)
for rel, (t, d, h1) in FIX.items():
    p = W + rel
    if not os.path.exists(p):
        print(rel + ': no existe'); continue
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    shutil.copy2(p, '/root/respaldos/titulos-' + ts + '/' + rel.replace('/', '__'))
    s = re.sub(r'<title>.*?</title>', '<TITLE>' + t + '</TITLE>', s, count=1, flags=re.S | re.I)
    s = re.sub(r'<meta\s+name="description"[^>]*>', '<meta name="description" content="' + d + '">', s, count=1, flags=re.I)
    s = re.sub(r'(<meta\s+property="og:title"\s+content=")[^"]*', r'\g<1>' + t, s, flags=re.I)
    s = re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*', r'\g<1>' + d, s, flags=re.I)
    s = re.sub(r'(<meta\s+name="twitter:title"\s+content=")[^"]*', r'\g<1>' + t, s, flags=re.I)
    s = re.sub(r'(<meta\s+name="twitter:description"\s+content=")[^"]*', r'\g<1>' + d, s, flags=re.I)
    if h1:
        s = re.sub(r'(<h1 id="sp-h1"><!-- InstanceBeginEditable name="title" -->).*?(<!-- InstanceEndEditable -->)', lambda m: m.group(1) + h1 + m.group(2), s, count=1, flags=re.S)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    print('Titulo: ' + rel + ' -> ' + t)
# publish map
new = open(W + 'map-nuevo.html', encoding='utf-8', errors='surrogateescape').read()
new = re.sub(r'<meta name="robots" content="noindex, nofollow">\s*', '', new, count=1)
if 'cr-map' in new and 'sp-hero' in new and 'noindex' not in new:
    shutil.copy2(W + 'map.html', '/root/respaldos/map-viejo-' + ts + '.html')
    open(W + 'map.html', 'w', encoding='utf-8', errors='surrogateescape').write(new)
    shutil.move(W + 'map-nuevo.html', '/root/respaldos/map-nuevo-' + ts + '.html')
    print('Mapa publicado: https://www.propertiesincostarica.com/map.html')
else:
    print('Mapa NO publicado, revisar')
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
