# Solo mira (no cambia nada): ultimos registros y tablas relacionadas del buscador
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
code = r'''from django.db import connection
c = connection.cursor()
c.execute("SHOW TABLES"); print("TABLAS: " + ", ".join(r[0] for r in c.fetchall()))
c.execute("SELECT id, id_code, title, sales_price, status_id, region_id, province_id, district_id, city_id, listed_by_id, exclusive, position, full_url, primary_picture, url FROM listing_listing ORDER BY id DESC LIMIT 6")
for r in c.fetchall(): print("ROW " + " | ".join(unicode(x)[:70] for x in r))
c.execute("SELECT id, id_code, title, sales_price, status_id FROM listing_listing WHERE id_code LIKE '%4128%' OR id_code LIKE '%4228%' OR id_code LIKE '%4241%' OR id_code LIKE '%4233%' OR title LIKE '%Leon%' OR title LIKE '%Whale%' OR title LIKE '%Cradled%'")
for r in c.fetchall(): print("BUSCADO " + " | ".join(unicode(x)[:70] for x in r))
c.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='listing_listing' AND column_name IN ('id_code','sales_price','status_id','exclusive','position','date_created','agreement_end')")
print("TIPOS " + str(c.fetchall()))
for t in ("listing_status", "listing_region", "listing_province", "listing_district", "listing_city"):
    try:
        c.execute("SELECT * FROM %s LIMIT 60" % t); print(t.upper() + " " + str([tuple(unicode(x)[:30] for x in r) for r in c.fetchall()]))
    except Exception as e: print(t + " ERROR " + str(e)[:80])

'''
open('/tmp/dbpeek2_code.py', 'w').write(code)
print(sh('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/dbpeek2_code.py 2>&1 | grep -E "TABLAS|ROW|BUSCADO|TIPOS|LISTING_|ERROR" | cut -c1-3000'))
print('LISTO')
