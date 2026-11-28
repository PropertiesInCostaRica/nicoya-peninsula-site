#!/usr/bin/env python3
# #4251 Cahuita lots (Leo): new price on the page, on every listing card and in the search database.
# Also fixes the sea view lots price per m2: US$150 -> US$155 (the agent's text says US$155).
#
#   python3 price4251.py "US$120,000"                    -> preview only, changes nothing
#   python3 price4251.py "US$120,000" --aplicar          -> applies (backups in /root/respaldos)
#   add --sin-m2 to also take out the "US$95 per m2" lines (use it if the price per m2 no longer applies)
#
# The page must already exist (made by list4251.py). Python 3.5 compatible.
import os, re, sys, glob, shutil, subprocess, time, json
W = '/var/www/propertiesincostarica.com/web/'
REL = 'properties/caribe/for-sale/cahuita-lots.html'
PAGE = W + REL
CODE = 4251
AP = '--aplicar' in sys.argv
SINM2 = '--sin-m2' in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith('--')]
if not args or not re.match(r'^US\$[\d,]+$', args[0]):
    raise SystemExit('Uso: python3 price4251.py "US$120,000" [--sin-m2] [--aplicar]')
NEW = args[0]
NUM = int(NEW.replace('US$', '').replace(',', ''))
B = '/root/respaldos/price4251-' + time.strftime('%Y%m%d%H%M') + '/'
if not os.path.exists(PAGE):
    raise SystemExit('La pagina #4251 no existe todavia. Primero publiquela con list4251.py y despues corra este script.')
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s): open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
def save(p, s):
    if not AP: return
    os.makedirs(B, exist_ok=True)
    shutil.copy2(p, B + p[len(W):].replace('/', '_'))
    wr(p, s)

# 1. Property page
s = rd(PAGE); t = s
t = re.sub(r'(<!-- InstanceBeginEditable name="price" -->).*?(<!-- InstanceEndEditable -->)',
           lambda m: m.group(1) + 'Sales Price: ' + NEW + m.group(2), t, count=1, flags=re.S)
t = t.replace('From US$95,000', NEW)
t = t.replace('Lots from US$95,000.', 'Offered at ' + NEW + '.')
t = t.replace('US$150 per m2', 'US$155 per m2')
if SINM2:
    t = t.replace('<p>Lots are priced at US$95 per m2, so a 1,000 m2 lot is US$95,000. The two sea view lots are priced at US$155 per m2.</p>',
                  '<p>Ask us for the current price and availability of each lot.</p>')
    t = t.replace('<li>US$95 per m2, sea view lots US$155 per m2</li>\n', '')
    t = t.replace('<li><strong>US$95 per m2 | Sea view lots US$155 per m2</strong></li>', '<li><strong>Sales Price: ' + NEW + '</strong></li>')
left = sorted(set(re.findall(r'US\$[\d,]+(?: per m2)?', t)))
print('Pagina: https://www.propertiesincostarica.com/' + REL)
print('  precios que quedan en la pagina: ' + ', '.join(left))
if t != s:
    save(PAGE, t); print('  pagina ' + ('ACTUALIZADA' if AP else 'se actualizaria'))
else:
    print('  la pagina ya estaba asi, sin cambios')

# 2. Listing cards in every section page
def fixcard(m):
    c = m.group(0)
    if REL not in c: return c
    return re.sub(r'<li>(\s*<strong>)?\s*Sales Price:.*?</li>',
                  lambda k: '<li>' + ('<strong>' if k.group(1) else '') + 'Sales Price: ' + NEW + ('</strong>' if k.group(1) else '') + '</li>',
                  c, count=1, flags=re.S)
n = 0
for f in sorted(glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*')):
    if f == PAGE: continue
    s = rd(f)
    if REL not in s or '<article' not in s: continue
    t = re.sub(r'<article class="listing".*?</article>', fixcard, s, flags=re.S)
    if t != s:
        save(f, t); n += 1
        print('Tarjeta ' + ('actualizada' if AP else 'se actualizaria') + ': https://www.propertiesincostarica.com/' + f[len(W):])
print('%d paginas con tarjeta' % n)

# 3. Search database (the admin panel cannot edit prices, so it is done directly)
code = r'''from django.db import connection
c = connection.cursor()
c.execute("SELECT id, sales_price FROM listing_listing WHERE id_code=%%s", [%d])
r = c.fetchall()
if not r: print("@@Buscador: #%d no esta en la base todavia (corra dbnew.py)")
for i, p in r:
    print("@@Buscador: registro %%s precio actual %%s -> %d" %% (i, p))
    if %s:
        c.execute("UPDATE listing_listing SET sales_price=%%s WHERE id=%%s", [%d, i])
        try: connection.commit()
        except Exception: pass
        print("@@Buscador: ACTUALIZADO")
''' % (CODE, CODE, NUM, AP, NUM)
open('/tmp/price4251_code.py', 'w').write(code)
out = subprocess.run('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/price4251_code.py 2>&1 | grep -o -E "@@.*|Error.*|rror:.*" | sed "s/^@@//"',
                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
print(out)
if AP:
    os.makedirs(B, exist_ok=True)
    open(B + 'buscador.txt', 'w').write(out + '\n')
    os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
    print('LISTO. Respaldos en ' + B)
else:
    print('Vista previa, no se cambio nada. Para aplicar agregue --aplicar')
