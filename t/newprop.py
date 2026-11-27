#!/usr/bin/env python3
# Puts a property page into the NEW DESIGN (header, menu, footer, lead form) keeping all its own content.
# Usage: python3 newprop.py <page path from web root> [more pages...]
import re, sys, os, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
SHELL = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
RX = re.compile(r'(<!-- InstanceBeginEditable name="([^"]+)" -->)(.*?)(<!-- InstanceEndEditable -->)', re.S)
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
shell = rd(SHELL)
B = '/root/respaldos/newprop-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
for rel in sys.argv[1:]:
    rel = rel.replace('https://www.propertiesincostarica.com/', '').lstrip('/')
    p = W + rel
    if not os.path.exists(p): print('ERROR: no existe ' + rel); continue
    old = rd(p)
    if 'hd--v2' in old: print('Ya tiene el diseno nuevo: ' + rel); continue
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
