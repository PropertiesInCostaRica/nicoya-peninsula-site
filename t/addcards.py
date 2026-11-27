# Agrega tarjetas de propiedades a una seccion (copiandolas de otras secciones del sitio).
# Uso: python3 addcards.py <pagina> <ID> <ID> ...
#  - Las de PCR/Klaudia quedan justo despues de Featured.
#  - Las de Cynthia (E&V) quedan despues de las activas de PCR (antes de las viejas o vendidas).
import os, re, sys, glob, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
P = sys.argv[1].replace('https://www.propertiesincostarica.com/', '').lstrip('/')
IDS = [x.lstrip('#') for x in sys.argv[2:]]
EV = ['modern-tropical-pool-home','tamarindo-pool-home','modern-home-casita-tamarindo','ocean-view-estate-flamingo','courtyard-home-playa-grande','golf-view-residence-conchal','beach-villa-avellanas','golf-villa-conchal']
INI = '<!--###################INI#####################-->'; FIN = '<!--###################FIN#####################-->'
def rd(f): return open(f, encoding='utf-8', errors='surrogateescape').read()
s = rd(W + P)
pool = {}
for f in glob.glob(W + '*.htm*') + glob.glob(W + 'homes/*.htm*') + glob.glob(W + 'invest/*.htm*') + glob.glob(W + 'beach/*.htm*') + glob.glob(W + 'region_and_price/*/*/*.php'):
    if 'nuevo' in f: continue
    try: t = rd(f)
    except Exception: continue
    for a in re.findall(r'<article class="listing".*?</article>', t, re.S):
        m = re.search(r'ID CODE:?\s*#(\d+)', a)
        if m and m.group(1) not in pool and 'Sold!' not in a: pool[m.group(1)] = a
w = lambda x: INI + '\n' + x + '\n' + FIN + '\n'
pcr, ev = [], []
for i in IDS:
    if re.search(r'ID CODE:?\s*#' + i + r'\b', s): print('#' + i + ' ya estaba en la pagina'); continue
    if i not in pool: print('#' + i + ': no encontre su tarjeta en ninguna seccion'); continue
    (ev if any('/' + e + '.html' in pool[i] for e in EV) else pcr).append(pool[i]); print('Agregada #' + i)
if not pcr and not ev: raise SystemExit('Nada que agregar')
fs = re.search(r'<section class="featured_listing_of.*?</section>\s*', s, re.S)
if not fs: raise SystemExit('No encontre Featured')
s = s[:fs.end()] + ''.join(w(x) for x in pcr) + s[fs.end():]
if ev:
    arts = list(re.finditer(r'(?:' + re.escape(INI) + r'\s*)?<article class="listing".*?</article>', s, re.S))
    pos = None
    for m in arts:
        if m.start() < fs.end(): continue
        idm = re.search(r'#(\d+)', m.group(0))
        if 'Sold!' in m.group(0) or (idm and int(idm.group(1)) < 2000) or re.search(r'Off the Market|Under Contract', m.group(0), re.I): pos = m.start(); break
    if pos is None: pos = arts[-1].end() + 1 if arts else fs.end()
    s = s[:pos] + ''.join(w(x) for x in ev) + s[pos:]
os.makedirs('/root/respaldos', exist_ok=True)
shutil.copy2(W + P, '/root/respaldos/' + P.replace('/', '_') + '.add.' + time.strftime('%Y%m%d%H%M'))
open(W + P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Ver: https://www.propertiesincostarica.com/' + P)
print('LISTO')
