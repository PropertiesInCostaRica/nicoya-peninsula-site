# Quita el parrafo <p> que contiene un texto. Uso: python3 quitar.py <pagina> "<texto>"
import re, sys, os, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
p, txt = sys.argv[1].replace('https://www.propertiesincostarica.com/', ''), sys.argv[2]
f = W + p
t = open(f, encoding='utf-8', errors='surrogateescape').read()
rx = re.compile(r'[ \t]*<p\b[^>]*>(?:(?!</p>).)*?' + re.escape(txt) + r'.*?</p>[ \t]*\n?', re.S | re.I)
n = len(rx.findall(t))
if not n:
    print('No encontre:', txt); sys.exit()
B = '/root/respaldos/quitar-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True); shutil.copy2(f, B + p.replace('/', '_'))
open(f, 'w', encoding='utf-8', errors='surrogateescape').write(rx.sub('', t))
print('Quitado (%d): %s' % (n, 'https://www.propertiesincostarica.com/' + p))
print('LISTO')
