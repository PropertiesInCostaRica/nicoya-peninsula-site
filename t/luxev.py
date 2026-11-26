#!/usr/bin/env python3
# Puts the E&V exclusives on Luxury Estates, right after Casa Leon del Mar, in order
import os, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
LUX = W + 'luxury_estates_in_costa_rica.html'
EV = ['properties/guanacaste/for_sale/modern-tropical-pool-home.html',
      'properties/guanacaste/for_sale/tamarindo-pool-home.html',
      'properties/guanacaste/for_sale/modern-home-casita-tamarindo.html']
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
t = open(LUX, encoding='utf-8', errors='surrogateescape').read()
B = '/root/respaldos/luxev-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True); shutil.copy2(LUX, B)
i = t.find('ocean-setting.html', t.find(FIN, t.find('featured_listing_of')))
if i < 0: raise SystemExit('ERROR: no encontre Casa Leon del Mar en Luxury')
pos = t.find(FIN, i) + len(FIN)
n = 0
for rel in EV:
    if not os.path.exists(W + rel): print('aun no existe: ' + rel); continue
    if ('href="/' + rel + '"') in t:
        j = t.find('href="/' + rel + '"'); pos = max(pos, t.find(FIN, j) + len(FIN)); print('ya estaba: ' + rel); continue
    c = card(rel)
    if not c: print('OJO sin tarjeta: ' + rel); continue
    t = t[:pos] + '\n' + c + t[pos:]; pos += 1 + len(c) - 1; n += 1
    print('Agregada en Luxury: ' + rel)
open(LUX, 'w', encoding='utf-8', errors='surrogateescape').write(t)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO luxury (%d nuevas)' % n)
