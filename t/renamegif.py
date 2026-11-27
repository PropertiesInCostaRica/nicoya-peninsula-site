# Para que se vea YA la foto animada nueva (el CDN guarda la vieja):
# copia p.gif con otro nombre y cambia todas las tarjetas del sitio a ese nombre nuevo.
# Uso: python3 renamegif.py turn-key-ocean-view-estate
import os, re, sys, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
folder = sys.argv[1]
D = W + 'properties/Images/' + folder + '/'
new = 'p-' + time.strftime('%Y%m%d%H%M') + '.gif'
shutil.copy2(D + 'p.gif', D + new)
old_re = re.compile(r'(properties/Images/' + re.escape(folder) + r'/)p(?:-\d{12})?\.gif')
B = '/root/respaldos/renamegif-' + time.strftime('%Y%m%d%H%M') + '/'
n = 0
for root, dirs, files in os.walk(W):
    if '/.git' in root or root.startswith(W + 'properties/Images'): continue
    for fn in files:
        if not re.search(r'\.(html?|php)$', fn): continue
        f = os.path.join(root, fn)
        try: t = open(f, encoding='utf-8', errors='surrogateescape').read()
        except Exception: continue
        if folder + '/p' not in t: continue
        nt = old_re.sub(lambda m: m.group(1) + new, t)
        if nt != t:
            os.makedirs(B, exist_ok=True); rel = f[len(W):]
            shutil.copy2(f, B + rel.replace('/', '_'))
            open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt); n += 1
            print('Actualizada: https://www.propertiesincostarica.com/' + rel)
print('Paginas con la foto animada nueva: %d (%s)' % (n, new))
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
