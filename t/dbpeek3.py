# Solo mira (no cambia nada): por que una propiedad sale o no en el buscador
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
code = r'''from django.db import connection
c = connection.cursor()
def q(s):
    try:
        c.execute(s); return c.fetchall()
    except Exception as e: return "ERR " + str(e)[:100]

def cols(t):
    r = q("SHOW COLUMNS FROM " + t)
    return r if isinstance(r, str) else [x[0] for x in r]

print("@@COLS_SL " + str(cols("listing_section_listing")))
print("@@COLS_ST " + str(cols("listing_section_type")))
print("@@COLS_CITY " + str(cols("location_city")))
print("@@TYPE74 " + str(q("SELECT * FROM listing_section_type WHERE id=74")))
print("@@CITY " + str(q("SELECT * FROM location_city WHERE id IN (69,88,151)")))
print("@@DIST " + str(q("SELECT * FROM location_district WHERE id IN (404,88,151)")))
for k in ("4233","4241","4228","4128","4219","4242","4245","4249"):
    r = q("SELECT id, id_code, sales_price, status_id, region_id, province_id, district_id, city_id FROM listing_listing WHERE id_code=" + k)
    print("@@L" + k + " " + str(r))
    if r and not isinstance(r, str): print("@@S" + k + " " + str(q("SELECT * FROM listing_section_listing WHERE listing_id=" + str(r[0][0]))))

'''
open('/tmp/dbpeek3_code.py', 'w').write(code)
print(sh('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/dbpeek3_code.py 2>&1 | grep -o "@@.*" | cut -c3-1500'))
print('LISTO')
