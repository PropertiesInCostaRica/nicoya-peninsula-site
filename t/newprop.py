#!/usr/bin/env python3
# Puts a property page into the NEW DESIGN (header, menu, footer, lead form) keeping all its own content.
# Usage: python3 newprop.py <page> [more pages...]
#        python3 newprop.py --count          (only counts, changes nothing)
#        python3 newprop.py --test 10        (converts 10 varied pages to review)
#        python3 newprop.py --all            (converts every active listing)
# Sold and rented listings are never touched.
import re, sys, os, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
SHELL = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
RX = re.compile(r'(<!-- InstanceBeginEditable name="([^"]+)" -->)(.*?)(<!-- InstanceEndEditable -->)', re.S)
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
shell = rd(SHELL)
B = '/root/respaldos/newprop-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
import glob, random
def gone(t):
    r = {m.group(2): m.group(3) for m in RX.finditer(t)}
    x = ' '.join(r.get(k, '') for k in ('title', 'code', 'price', 'features'))
    return bool(re.search(r'\bSOLD\b|Sold!|\bRENTED\b|Rented!|\bVendid|\bAlquilad', x, re.I))
args = sys.argv[1:]
if args and args[0] in ('--count', '--test', '--all', '--next'):
    allp = sorted(glob.glob(W + 'properties/**/*.htm*', recursive=True))
    act, sold, other, done = [], [], [], []
    for p in allp:
        t = rd(p)
        if 'hd--v2' in t: done.append(p); continue
        if 'template_properties' not in t or 'InstanceBeginEditable name="content"' not in t: other.append(p); continue
        (sold if gone(t) else act).append(p)
    print('Paginas: %d | ya nuevas: %d | activas por cambiar: %d | vendidas/alquiladas (no se tocan): %d | otra plantilla: %d' % (len(allp), len(done), len(act), len(sold), len(other)))
    if args[0] == '--count':
        for p in other[:15]: print('  otra plantilla: ' + p[len(W):])
        raise SystemExit
    def pid(p):
        m = re.search(r'ID CODE: #(\d+)', rd(p)) or re.search(r'name="CODE"[^>]*value="(\d+)"', rd(p))
        return int(m.group(1)) if m else 0
    if args[0] == '--next':
        # next 10 active listings with ID 3500 or higher, newest first
        n = int(args[1]) if len(args) > 1 else 10
        cand = sorted([(pid(p), p) for p in act if pid(p) >= 3500], reverse=True)
        print('Quedan %d activas con ID 3500 o mayor' % len(cand))
        act = [p for _, p in cand[:n]]
    if args[0] == '--test':
        n = int(args[1]) if len(args) > 1 else 10
        act.sort(key=os.path.getmtime)
        k = max(1, len(act) // n)
        act = act[::k][:n]
    args = [p[len(W):] for p in act]
for rel in args:
    rel = rel.replace('https://www.propertiesincostarica.com/', '').lstrip('/')
    p = W + rel
    if not os.path.exists(p): print('ERROR: no existe ' + rel); continue
    old = rd(p)
    if 'hd--v2' in old: print('Ya tiene el diseno nuevo: ' + rel); continue
    if gone(old): print('Vendida o alquilada, no se toca: ' + rel); continue
    regs = {m.group(2): m.group(3) for m in RX.finditer(old)}
    if 'content' not in regs or 'title' not in regs:
        print('OJO: esta pagina no usa la plantilla de propiedades, no la toque: ' + rel); continue
    miss = []
    def rep(m):
        n = m.group(2)
        if n in regs: return m.group(1) + regs[n] + m.group(4)
        miss.append(n); return m.group(1) + m.group(4)
    new = RX.sub(rep, shell)
    if re.search(r'whale-bay|Whale Bay|4241', RX.sub('', new)): print('OJO: quedo algo de Whale Bay fuera de las regiones en ' + rel)
    shutil.copy2(p, B + rel.replace('/', '_'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(new)
    print('Diseno nuevo: https://www.propertiesincostarica.com/' + rel + (' (regiones vacias: ' + ','.join(miss) + ')' if miss else ''))
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
