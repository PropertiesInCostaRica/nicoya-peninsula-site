# Da espacio abajo a la caja de Featured. Uso: python3 pad.py <pagina>
import os, sys, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
p = sys.argv[1].replace('https://www.propertiesincostarica.com/', ''); f = W + p
t = open(f, encoding='utf-8', errors='surrogateescape').read()
a = '<section class="featured_listing_of titulo_categoria">'
if a not in t: print('No encontre la caja Featured'); sys.exit()
B = '/root/respaldos/pad-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True); shutil.copy2(f, B + p.replace('/', '_'))
t = t.replace(a, '<section class="featured_listing_of titulo_categoria" style="padding-bottom:40px;margin-bottom:30px">', 1)
open(f, 'w', encoding='utf-8', errors='surrogateescape').write(t)
print('Espacio agregado: https://www.propertiesincostarica.com/' + p); print('LISTO')
