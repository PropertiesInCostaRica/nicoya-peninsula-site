#!/usr/bin/env python3
# Makes the banner photo brighter on the 8 Caribbean pages (text keeps a stronger shadow so it stays readable).
import shutil, time
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
OLD = '.sp-hero picture img{filter:brightness(.55)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 2px 8px rgba(0,0,0,.8)}'
NEW = '.sp-hero picture img{filter:brightness(.75)}.sp-hero-in h1,.sp-hero-in p{text-shadow:0 1px 3px rgba(0,0,0,.9),0 2px 12px rgba(0,0,0,.7)}'
for rel in ['caribbean.html', 'puerto-viejo-real-estate.html', 'cocles-chiquita-real-estate.html', 'manzanillo-real-estate.html',
            'cahuita-real-estate.html', 'hone-creek-carbon.html', 'tortuguero-real-estate.html', 'guapiles-real-estate.html']:
    p = W + rel
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    if OLD not in s:
        print(rel + ': no encontrado, sin cambio'); continue
    shutil.copy(p, '/root/respaldos/' + rel + '-' + TS)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s.replace(OLD, NEW))
    print(rel + ': mas claro')
print('LISTO')
