#!/usr/bin/env python3
# #2568 Puriscal 52 acres: mark as SOLD (page stays online with a Sold banner and links to similar
# properties; card removed from the active listing pages; status Sold in the website database). Backups first.
import re, os, glob, shutil, subprocess, time
W = '/var/www/propertiesincostarica.com/web/'
PAGE = 'properties/puriscal/for_sale/amazing-central-valley-views-lot.html'
KEY = 'amazing-central-valley-views-lot'
ts = time.strftime('%Y%m%d-%H%M%S')
BK = '/root/respaldos/sold2568-' + ts + '/'
os.makedirs(BK, exist_ok=True)
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def save(p, s):
    shutil.copy2(p, BK + p[len(W):].replace('/', '__'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
# 1. listing page: price -> SOLD, banner at top of content
p = W + PAGE; s = rd(p)
if 'class="sold">SOLD' in s:
    print('1. La pagina ya decia SOLD')
else:
    s = re.sub(r'(<!-- InstanceBeginEditable name="price" -->).*?(<!-- InstanceEndEditable -->)',
               r'\1 <strong style="color:#c0392b">SOLD</strong> \2', s, count=1, flags=re.S)
    banner = ('\n<p class="sold">SOLD!!! Looking for similar properties? '
              '<a href="https://www.propertiesincostarica.com/residential_lots.html">See land for sale</a> | '
              '<a href="https://www.propertiesincostarica.com/puriscal.html">Puriscal properties</a> | '
              '<a href="https://www.propertiesincostarica.com/mountain.html">Farms and mountain properties</a></p>\n')
    s = s.replace('<!-- InstanceBeginEditable name="content" -->', '<!-- InstanceBeginEditable name="content" -->' + banner, 1)
    s = re.sub(r'(<title>)(.*?)(</title>)', lambda m: m.group(1) + 'SOLD: ' + m.group(2) if 'SOLD' not in m.group(2) else m.group(0), s, count=1, flags=re.I | re.S)
    save(p, s)
    print('1. Pagina marcada como SOLD con enlaces a propiedades similares')
# 2. remove its card from active listing pages
art = re.compile(r'(?:<!--[^>]*INI[^>]*-->\s*)?<article class="listing".*?</article>(?:\s*<!--[^>]*FIN[^>]*-->)?', re.S)
done = []
for f in glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*') + glob.glob(W + '*/*/*.htm*'):
    if f == p or '-nuevo.' in f: continue
    try: s = rd(f)
    except Exception: continue
    if KEY not in s: continue
    s2, n = art.subn(lambda m: '' if KEY in m.group(0) else m.group(0), s)
    if s2 != s:
        save(f, s2); done.append('%s (%d)' % (f[len(W):], s.count('<article class="listing"') - s2.count('<article class="listing"')))
print('2. Tarjeta quitada de: ' + (', '.join(done) or 'ninguna pagina'))
# 3. website database status -> sold (3)
def q(sql): return subprocess.run(['mysql', '-N', '-e', sql, 'db1pcrappsearch'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode().strip()
rid = q("SELECT id FROM listing_listing WHERE full_url LIKE '%%%s%%'" % KEY).split()
if len(rid) == 1:
    subprocess.run("mysqldump db1pcrappsearch listing_listing --where='id=%s' > %slisting.sql" % (rid[0], BK), shell=True)
    q("UPDATE listing_listing SET status_id=3 WHERE id=%s" % rid[0])
    print('3. Base de datos (fila %s): estado = vendida (3)' % rid[0])
else:
    print('3. Base de datos: no encontre una sola fila (%s), no se cambio' % rid)
print('Respaldos en ' + BK)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
