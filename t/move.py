# Mueve una tarjeta antes de otra en una seccion.
# Uso: python3 move.py <pagina> <ID a mover> <ID de referencia>
import re, os, sys, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
P = sys.argv[1].replace('https://www.propertiesincostarica.com/', '').lstrip('/'); A = sys.argv[2].lstrip('#'); Bf = sys.argv[3].lstrip('#')
INI = '<!--###################INI#####################-->'; FIN = '<!--###################FIN#####################-->'
s = open(W + P, encoding='utf-8', errors='surrogateescape').read()
def card(i):
    return re.search(r'(?:' + re.escape(INI) + r'\s*)?<article class="listing"(?:(?!</article>).)*?ID CODE:?\s*#' + i + r'\b.*?</article>(?:\s*' + re.escape(FIN) + r')?\s*', s, re.S)
m = card(A)
if not m: raise SystemExit('No encontre #' + A)
block = m.group(0)
s = s[:m.start()] + s[m.end():]
r = card(Bf)
if not r: raise SystemExit('No encontre #' + Bf)
s = s[:r.start()] + block + s[r.start():]
os.makedirs('/root/respaldos', exist_ok=True)
shutil.copy2(W + P, '/root/respaldos/' + P.replace('/', '_') + '.move.' + time.strftime('%Y%m%d%H%M'))
open(W + P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('#' + A + ' ahora va antes de #' + Bf + ': https://www.propertiesincostarica.com/' + P)
print('LISTO')
