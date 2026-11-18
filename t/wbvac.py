#!/usr/bin/env python3
# Whale Bay Villa: add A/C and good internet to the features and highlights.
import shutil, subprocess, time

P = '/var/www/propertiesincostarica.com/web/properties/puntarenas/for_sale/whale-bay-villa.html'
bk = '/root/respaldos/whale-bay-villa-' + time.strftime('%Y%m%d-%H%M%S') + '.html'
shutil.copy2(P, bk)
s = open(P, encoding='utf-8', errors='surrogateescape').read()
n = 0
a = '<li><strong>Ocean View | Pool | Garage | Furnished</strong></li>'
if a in s:
    s = s.replace(a, '<li><strong>Ocean View | Pool | Garage | Furnished | Split A/C | Good Internet</strong></li>')
    n += 1
b = '<li>Living room with vaulted beamed ceiling and sliding doors</li>'
c = '<li>Split unit air conditioning in the rooms, and good internet</li>'
if b in s and c not in s:
    s = s.replace(b, b + '\n' + c, 1)
    n += 1
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Cambios: %d (deben ser 2)' % n)
print('Respaldo: ' + bk)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
