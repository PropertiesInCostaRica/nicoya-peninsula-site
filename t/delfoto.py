# Quita una foto de la galeria de una pagina. Uso: python3 delfoto.py <pagina> <archivo-foto>
import re, sys, os, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
p = sys.argv[1].replace('https://www.propertiesincostarica.com/', ''); img = sys.argv[2]
f = W + p; t = open(f, encoding='utf-8', errors='surrogateescape').read()
rx = re.compile(r'<a href="[^"]*/' + re.escape(img) + r'"[^>]*>\s*<img[^>]*></a>\s*')
n = len(rx.findall(t))
if not n: print('No encontre la foto', img); sys.exit()
B = '/root/respaldos/delfoto-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True); shutil.copy2(f, B + p.replace('/', '_'))
open(f, 'w', encoding='utf-8', errors='surrogateescape').write(rx.sub('', t))
print('Foto quitada (%d): %s' % (n, 'https://www.propertiesincostarica.com/' + p)); print('LISTO')
