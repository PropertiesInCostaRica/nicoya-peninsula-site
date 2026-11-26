#!/usr/bin/env python3
# Puts the E&V exclusives on Luxury Estates (after Casa Leon del Mar) and Sea Side Homes (top of list), in order
import os, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
LUX = W + 'luxury_estates_in_costa_rica.html'
EV = ['properties/guanacaste/for_sale/modern-tropical-pool-home.html',
      'properties/guanacaste/for_sale/tamarindo-pool-home.html',
      'properties/guanacaste/for_sale/modern-home-casita-tamarindo.html',
      'properties/guanacaste/for_sale/ocean-view-estate-flamingo.html',
      'properties/guanacaste/for_sale/courtyard-home-playa-grande.html']
INI = '<!--###################INI#####################-->'
FIN = '<!--###################FIN#####################-->'
def card(rel):
    for f in ('homes.html', 'tamarindo-real-estate.html', 'beach.html'):
        t = open(W + f, encoding='utf-8', errors='surrogateescape').read()
        i = t.find('href="/' + rel + '"')
        if i < 0: continue
        a = t.rfind(INI, 0, i); b = t.find(FIN, i) + len(FIN)
        return t[a:b] + '\n'
    return None
def place(page, anchor):
    p = W + page
    t = open(p, encoding='utf-8', errors='surrogateescape').read()
    B = '/root/respaldos/luxev-' + time.strftime('%Y%m%d%H%M') + '/'
    os.makedirs(B, exist_ok=True); shutil.copy2(p, B + page.replace('/', '_'))
    f = t.find('featured_listing_of')
    if anchor:
        i = t.find(anchor, t.find(FIN, f) if f >= 0 else 0)
        if i < 0: print('ERROR: no encontre ' + anchor + ' en ' + page); return
        pos = t.find(FIN, i) + len(FIN)
    elif f >= 0:
        pos = t.find('</section>', f) + len('</section>')
    else:
        pos = t.find(INI)
    n = 0
    for rel in EV:
        if not os.path.exists(W + rel): print('aun no existe: ' + rel); continue
        if ('href="/' + rel + '"') in t:
            j = t.find('href="/' + rel + '"'); pos = max(pos, t.find(FIN, j) + len(FIN)); continue
        c = card(rel)
        if not c: print('OJO sin tarjeta: ' + rel); continue
        t = t[:pos] + '\n' + c + t[pos:]; pos += len(c); n += 1
        print('Agregada en ' + page + ': ' + rel)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t)
    print('%s: %d nuevas' % (page, n))
place('luxury_estates_in_costa_rica.html', 'ocean-setting.html')
place('homes/sea_side_homes.html', None)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO luxury y sea side')
