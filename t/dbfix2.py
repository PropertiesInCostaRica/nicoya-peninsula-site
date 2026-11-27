# Buscador: a Whale Bay (#4241) le falta "For Sale" (tabla listing_listing_property_status)
#   python3 dbfix2.py            -> solo muestra
#   python3 dbfix2.py --aplicar  -> lo agrega (guarda respaldo)
import sys, subprocess, time
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
AP = '--aplicar' in sys.argv
BK = '/root/respaldos/db-buscador2-' + time.strftime('%Y%m%d%H%M') + '.txt'
code = r'''from django.db import connection
c = connection.cursor()
AP = %s
def q(s, a=None):
    c.execute(s, a or []); return c.fetchall()

T = "listing_listing_property_status"
cl = [r[0] for r in q("SHOW COLUMNS FROM " + T)]
print("@@columnas: " + ", ".join(cl))
other = [x for x in cl if x not in ("id", "listing_id")][0]
A = q("SELECT id FROM listing_listing WHERE id_code=4219")[0][0]
B = q("SELECT id FROM listing_listing WHERE id_code=4241")[0][0]
va = [r[0] for r in q("SELECT " + other + " FROM " + T + " WHERE listing_id=%%s", [A])]
vb = [r[0] for r in q("SELECT " + other + " FROM " + T + " WHERE listing_id=%%s", [B])]
tabs = [t for (t,) in q("SHOW TABLES") if "status" in t and t not in (T,)]
for t in tabs:
    try: print("@@" + t + ": " + str(q("SELECT * FROM " + t)[:10]))
    except Exception: pass

print("@@Casa Coral tiene: " + str(va) + " | Whale Bay tiene: " + str(vb))
print("@@PLAN: agregar a Whale Bay " + str([v for v in va if v not in vb]) + " y rental_price vacio como Casa Coral")
if AP:
    open("%s", "w").write("whale " + str(B) + " property_status antes: " + str(vb) + "\n")
    for v in va:
        if v not in vb: c.execute("INSERT INTO " + T + " (listing_id, " + other + ") VALUES (%%s,%%s)", [B, v])
    c.execute("UPDATE listing_listing SET rental_price=NULL WHERE id=%%s AND (rental_price=0 OR rental_price IS NULL)", [B])
    try:
        from django.db import transaction; transaction.commit_unless_managed()
    except Exception: pass
    try: connection.commit()
    except Exception: pass
    print("@@APLICADO. Respaldo: %s")

''' % (AP, BK, BK)
open('/tmp/dbfix2_code.py', 'w').write(code)
print(sh('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/dbfix2_code.py 2>&1 | grep -o -E "@@.*|Error.*" | sed "s/^@@//" | cut -c1-400'))
print('LISTO' + ('' if AP else ' (solo vista previa, no se cambio nada)'))
