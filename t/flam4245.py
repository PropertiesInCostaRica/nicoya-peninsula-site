#!/usr/bin/env python3
# Adds #4245 card at the top of the Flamingo listings
import shutil, time, os
W = '/var/www/propertiesincostarica.com/web/'
REL = 'properties/guanacaste/for_sale/ocean-view-estate-flamingo.html'
INI = '<!--###################INI#####################-->'
FIN = '<!--###################FIN#####################-->'
h = open(W + 'homes.html', encoding='utf-8', errors='surrogateescape').read()
i = h.find('href="/' + REL + '"')
if i < 0: raise SystemExit('ERROR: no encontre la tarjeta en homes.html')
card = h[h.rfind(INI, 0, i):h.find(FIN, i) + len(FIN)] + '\n\n'
p = W + 'flamingo_real_estate.html'
t = open(p, encoding='utf-8', errors='surrogateescape').read()
if REL in t: raise SystemExit('ya estaba en Flamingo')
j = t.find(INI)
B = '/root/respaldos/flam4245-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True); shutil.copy2(p, B)
open(p, 'w', encoding='utf-8', errors='surrogateescape').write(t[:j] + card + t[j:])
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('Tarjeta agregada de primera en Flamingo. LISTO')
