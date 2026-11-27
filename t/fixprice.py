# Cambia el precio en TODAS las tarjetas del sitio que apuntan a una propiedad.
# Uso: python3 fixprice.py <pagina-de-la-propiedad> "US$1,200,000"
import os, re, sys, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
P = sys.argv[1].replace('https://www.propertiesincostarica.com/', '').lstrip('/'); PR = sys.argv[2]
slug = P.split('/')[-1]
B = '/root/respaldos/fixprice-' + time.strftime('%Y%m%d%H%M') + '/'
LI = '<li><strong>Sales Price: ' + PR + '</strong></li>'
def fix(a):
    if P not in a: return a
    a2, n = re.subn(r'<li>(?:(?!</li>).)*?Price(?:(?!</li>).)*?</li>', LI, a, count=1, flags=re.S | re.I)
    return a2
n = 0
for root, dirs, files in os.walk(W):
    if '/.git' in root or root.startswith(W + 'properties/Images'): continue
    for fn in files:
        if not re.search(r'\.(html?|php)$', fn): continue
        f = os.path.join(root, fn)
        try: t = open(f, encoding='utf-8', errors='surrogateescape').read()
        except Exception: continue
        if P not in t or '<article class="listing"' not in t: continue
        nt = re.sub(r'<article class="listing"(?:(?!</article>).)*?' + re.escape(P) + r'.*?</article>', lambda m: fix(m.group(0)), t, flags=re.S)
        if nt != t:
            os.makedirs(B, exist_ok=True); rel = f[len(W):]
            shutil.copy2(f, B + rel.replace('/', '_'))
            open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt); n += 1
            print('Precio actualizado: https://www.propertiesincostarica.com/' + rel)
print('Paginas actualizadas:', n)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
