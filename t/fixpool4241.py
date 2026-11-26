#!/usr/bin/env python3
# Whale Bay Villa #4241: the owners say it is NOT an infinity pool. Fix the page and its cards.
import re, os, glob, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
PAGE = W + 'properties/puntarenas/for_sale/whale-bay-villa.html'
B = '/root/respaldos/fixpool4241-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s): open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
def fix(t):
    t = re.sub(r'\b[Aa]n infinity edge pool', lambda m: 'A pool' if m.group(0)[0] == 'A' else 'a pool', t)
    t = re.sub(r'\binfinity edge pool', 'pool', t)
    t = re.sub(r'\bInfinity edge pool', 'Pool', t)
    t = re.sub(r'\bInfinity [Ee]dge\b', 'Ocean view pool', t)
    t = re.sub(r'\binfinity pool', 'pool', t)
    t = re.sub(r'\bInfinity [Pp]ool', 'Pool', t)
    return t
s = rd(PAGE); n = len(re.findall(r'infinity', s, re.I))
shutil.copy2(PAGE, B + 'whale-bay-villa.html'); s = fix(s); wr(PAGE, s)
print('Pagina: %d cambios, quedan %d' % (n, len(re.findall(r'infinity', s, re.I))))
c = 0
for p in glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*'):
    if '/properties/' in p: continue
    t = rd(p)
    if 'whale-bay-villa.html' not in t or not re.search('infinity', t, re.I): continue
    new = re.sub(r'<article class="listing".*?</article>', lambda m: fix(m.group(0)) if 'whale-bay-villa.html' in m.group(0) else m.group(0), t, flags=re.S)
    if new != t:
        shutil.copy2(p, B + p[len(W):].replace('/', '_')); wr(p, new); c += 1
        print('Tarjeta corregida: ' + p[len(W):])
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO (%d paginas con tarjeta)' % c)
