#!/usr/bin/env python3
# Move Whale Bay Villa photos to a new folder so the CDN loads the new photos.
import os, subprocess, shutil, time

WEB = '/var/www/propertiesincostarica.com/web'
OLD = 'Images/whale-bay-villa/'
NEW = 'Images/whale-bay-villa-2/'
src = os.path.join(WEB, 'properties', OLD)
dst = os.path.join(WEB, 'properties', NEW)
stamp = time.strftime('%Y%m%d-%H%M%S')
bk = '/root/respaldos/wbvcdn-' + stamp
os.makedirs(bk, exist_ok=True)

# 1. copy photo folder (old folder stays)
if not os.path.isdir(dst):
    shutil.copytree(src, dst)
    subprocess.call(['chown', '-R', '--reference=' + src, dst])
n = sum(len(f) for _, _, f in os.walk(dst))
print('Fotos en carpeta nueva: %d' % n)

# 2. update every page that uses the old folder
out = subprocess.check_output(
    ['grep', '-rl', '--include=*.html', '--include=*.htm', '--include=*.php',
     '--exclude-dir=Images', '--exclude-dir=blog', OLD, WEB]).decode().split()
for p in out:
    rel = p.replace(WEB + '/', '').replace('/', '__')
    shutil.copy2(p, os.path.join(bk, rel))
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    c = s.count(OLD)
    s = s.replace(OLD, NEW)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    print('Pagina: %s (%d cambios)' % (p.replace(WEB, ''), c))

# 3. ID search database row
try:
    cols = subprocess.check_output(['mysql', '-N', '-e',
        "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='db1pcrappsearch' "
        "AND TABLE_NAME='listing_listing' AND DATA_TYPE IN ('char','varchar','text','mediumtext','longtext')"]).decode().split()
    subprocess.call('mysqldump db1pcrappsearch listing_listing --where="id=2349" > %s/listing2349.sql' % bk, shell=True)
    sets = ','.join("`%s`=REPLACE(`%s`,'%s','%s')" % (c, c, OLD, NEW) for c in cols)
    subprocess.check_call(['mysql', 'db1pcrappsearch', '-e',
        'UPDATE listing_listing SET %s WHERE id=2349' % sets])
    print('Base de datos ID 4241: OK')
except Exception as e:
    print('Base de datos: no se cambio (%s)' % e)

print('Respaldo: ' + bk)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
