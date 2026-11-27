# Quita la redireccion 301 de la propiedad 4128 para que su pagina vuelva a verse
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
P = 'properties/Montezuma/for_sale/magical-sanctuary.html'
h = W + '.htaccess'
shutil.copy2(h, '/root/respaldos/htaccess.' + time.strftime('%Y%m%d%H%M'))
lines = open(h, encoding='utf-8', errors='surrogateescape').read().split('\n')
n = 0
for i, l in enumerate(lines):
    if '/' + P in l and l.strip().startswith('Redirect'):
        lines[i] = '# relisted ' + time.strftime('%Y-%m-%d') + ': ' + l; n += 1
open(h, 'w', encoding='utf-8', errors='surrogateescape').write('\n'.join(lines))
print('Redirecciones quitadas:', n)
t = open(W + P, encoding='utf-8', errors='surrogateescape').read()
R = {m.group(1): m.group(2) for m in re.finditer(r'<!-- InstanceBeginEditable name="([^"]+)" -->(.*?)<!-- InstanceEndEditable -->', t, re.S)}
v = lambda x: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x or '')).strip()
for k in ('title', 'code', 'price', 'features'): print(k.upper() + ':', v(R.get(k))[:300])
print('Pagina: https://www.propertiesincostarica.com/' + P)
print('LISTO')
