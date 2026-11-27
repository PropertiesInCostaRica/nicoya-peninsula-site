# Agrega el boton "Schedule a Showing" (WhatsApp) a todas las propiedades activas con diseno nuevo
# Uso: python3 showing.py <pagina> (solo una, para probar)
#      python3 showing.py          (todas)
#      python3 showing.py --quitar (lo quita de todas)
import os, re, sys, glob, shutil, time, urllib.request
W = '/var/www/propertiesincostarica.com/web/'
TAG = '<script src="/pcr-showing.js" defer></script>'
B = '/root/respaldos/showing-' + time.strftime('%Y%m%d%H%M') + '/'
QUITAR = '--quitar' in sys.argv
ONE = [a.replace('https://www.propertiesincostarica.com/', '').lstrip('/') for a in sys.argv[1:] if not a.startswith('--')]
if not QUITAR:
    open(W + 'pcr-showing.js', 'wb').write(urllib.request.urlopen('https://www.properties-in-costa-rica.com/t/pcr-showing.js').read())
RX = re.compile(r'<!-- InstanceBeginEditable name="([^"]+)" -->(.*?)<!-- InstanceEndEditable -->', re.S)
def gone(t):
    r = {m.group(1): m.group(2) for m in RX.finditer(t)}
    x = re.sub(r'<[^>]+>', ' ', ' '.join(r.get(k, '') for k in ('title', 'code', 'price', 'features')))
    return bool(re.search(r'\bSOLD\b|\bRENTED\b|Off the Market|Under Contract|\bVendid|\bAlquilad', x, re.I))
n = s = 0
for f in ([W + p for p in ONE] if ONE else glob.glob(W + 'properties/**/*.htm*', recursive=True)):
    if 'nuevo' in f or f.endswith('-wa.html'): continue
    try: t = open(f, encoding='utf-8', errors='surrogateescape').read()
    except Exception: continue
    if QUITAR:
        if TAG not in t: continue
        nt = t.replace(TAG + '\n', '').replace(TAG, '')
    else:
        if 'hd--v2' not in t or 'InstanceBeginEditable name="content"' not in t or TAG in t: continue
        if gone(t): s += 1; continue
        i = t.rfind('</body>')
        if i < 0: continue
        nt = t[:i] + TAG + '\n' + t[i:]
    os.makedirs(B, exist_ok=True)
    shutil.copy2(f, B + f[len(W):].replace('/', '_'))
    open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt); n += 1
print(('Quitado de' if QUITAR else 'Boton agregado a') + ' %d paginas' % n + ('' if QUITAR else ' (saltadas vendidas/alquiladas/fuera del mercado: %d)' % s))
print('Ver: https://www.propertiesincostarica.com/' + (ONE[0] if ONE else 'properties/puntarenas/for_sale/whale-bay-villa.html'))
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
