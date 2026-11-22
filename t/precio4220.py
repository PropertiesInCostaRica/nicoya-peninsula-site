#!/usr/bin/env python3
# Hotel Carmen Coral (#4220): new price US$865,000 -> US$780,000
# on the listing page, on every card that links to it, and in the website listing database. Backups first.
import re, os, glob, shutil, subprocess, time
W = '/var/www/propertiesincostarica.com/web/'
PAGE = 'properties/tambor/for_sale/renovated-hotel.html'
ts = time.strftime('%Y%m%d-%H%M%S')
BK = '/root/respaldos/precio4220-' + ts + '/'
os.makedirs(BK, exist_ok=True)
OLD = [('865,000', '780,000'), ('865.000', '780.000'), ('865000', '780000'), ('865K', '780K'), ('865k', '780k')]
def fix(t):
    for a, b in OLD: t = t.replace(a, b)
    return t
def save(p, s):
    shutil.copy2(p, BK + p[len(W):].replace('/', '__'))
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
# 1. listing page
p = W + PAGE
s = open(p, encoding='utf-8', errors='surrogateescape').read()
n = sum(s.count(a) for a, _ in OLD)
if n: save(p, fix(s))
print('1. Pagina del hotel: %d cambios' % n)
# 2. cards on all pages
art = re.compile(r'<article class="listing".*?</article>', re.S)
pages = 0; cards = 0
for f in glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*') + glob.glob(W + '*/*/*.htm*'):
    if f == p or '-nuevo.' in f: continue
    try: s = open(f, encoding='utf-8', errors='surrogateescape').read()
    except Exception: continue
    if 'renovated-hotel' not in s: continue
    c = [0]
    def rep(m):
        b = m.group(0)
        if 'renovated-hotel' in b and any(a in b for a, _ in OLD):
            c[0] += 1; return fix(b)
        return b
    s2 = art.sub(rep, s)
    # feature cards (homepage style) linking to the hotel
    s2 = re.sub(r'(<a class="feat-card"[^>]*renovated-hotel[^>]*>.*?</a>)', lambda m: fix(m.group(1)), s2, flags=re.S)
    if s2 != s:
        save(f, s2); pages += 1; cards += max(c[0], 1)
print('2. Tarjetas actualizadas: %d en %d paginas' % (cards, pages))
# 3. website listing database
def q(sql): return subprocess.run(['mysql', '-N', '-e', sql, 'db1pcrappsearch'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8', 'replace')
rid = q("SELECT id FROM listing_listing WHERE full_url LIKE '%renovated-hotel%' LIMIT 2").split()
if len(rid) != 1:
    print('3. Base de datos: no encontre una sola fila del hotel (%s), no se cambio' % rid)
else:
    rid = rid[0]
    cols = q("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='db1pcrappsearch' AND table_name='listing_listing'").strip().splitlines()
    subprocess.run("mysqldump db1pcrappsearch listing_listing --where='id=%s' > %slisting_%s.sql" % (rid, BK, rid), shell=True)
    done = []
    for line in cols:
        c, t = line.split('\t')
        v = q("SELECT `%s` FROM listing_listing WHERE id=%s" % (c, rid)).strip()
        if t in ('int', 'bigint', 'decimal', 'double', 'float') and v.split('.')[0] == '865000':
            q("UPDATE listing_listing SET `%s`=780000 WHERE id=%s" % (c, rid)); done.append(c)
        elif t in ('varchar', 'text', 'longtext', 'mediumtext') and any(a in v for a, _ in OLD):
            for a, b in OLD:
                q("UPDATE listing_listing SET `%s`=REPLACE(`%s`,'%s','%s') WHERE id=%s" % (c, c, a, b, rid))
            done.append(c)
    print('3. Base de datos del sitio (fila %s): columnas cambiadas: %s' % (rid, ', '.join(done) or 'ninguna'))
print('Respaldos en ' + BK)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
