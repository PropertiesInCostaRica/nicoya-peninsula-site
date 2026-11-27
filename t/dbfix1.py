# Buscador: Whale Bay (#4241) sin secciones y #4128 apagado.
#   python3 dbfix1.py            -> solo muestra lo que haria (no cambia nada)
#   python3 dbfix1.py --aplicar  -> hace los cambios (guarda respaldo antes)
import sys, subprocess, time
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
AP = '--aplicar' in sys.argv
BK = '/root/respaldos/db-buscador-' + time.strftime('%Y%m%d%H%M') + '.txt'
code = r'''from django.db import connection
c = connection.cursor()
AP = %s
def q(s, a=None):
    c.execute(s, a or []); return c.fetchall()

def lid(code): return q("SELECT id FROM listing_listing WHERE id_code=%%s", [code])[0][0]

tabs = [r[0] for r in q("SHOW TABLES")]
st = [t for t in tabs if t.startswith("listing_section") and t not in ("listing_section_listing", "listing_section_type")]
names = {}
if st:
    cl = [r[0] for r in q("SHOW COLUMNS FROM " + st[0])]
    nm = "name" if "name" in cl else ("title" if "title" in cl else cl[1])
    for r in q("SELECT id, %%s FROM %%s" %% (nm, st[0])): names[r[0]] = r[1]

W, COR, LEON, MZ = lid(4241), lid(4219), lid(4228), lid(4128)
cor = [r[0] for r in q("SELECT section_id FROM listing_section_listing WHERE listing_id=%%s", [COR])]
print("@@Casa Coral (#4219, misma zona) esta en: " + ", ".join("%%s %%s" %% (s, names.get(s, "?")) for s in cor))
print("@@Casa Leon (#4228) esta en: " + ", ".join("%%s %%s" %% (r[0], names.get(r[0], "?")) for r in q("SELECT section_id FROM listing_section_listing WHERE listing_id=%%s", [LEON])))
print("@@#4128 esta en: " + ", ".join("%%s %%s" %% (r[0], names.get(r[0], "?")) for r in q("SELECT section_id FROM listing_section_listing WHERE listing_id=%%s", [MZ])))
w = q("SELECT region_id, status_id FROM listing_listing WHERE id=%%s", [W])[0]
cr = q("SELECT region_id FROM listing_listing WHERE id=%%s", [COR])[0][0]
print("@@PLAN 1: Whale Bay (#4241) entra en las mismas secciones que Casa Coral; region %%s -> %%s" %% (w[0], cr))
print("@@PLAN 2: #4128 Cradled by Nature: Online y precio 225000 (ahora: " + str(q("SELECT status_id, sales_price FROM listing_listing WHERE id=%%s", [MZ])[0]) + ")")
if AP:
    bk = open("%s", "w")
    for r in q("SELECT id, region_id, status_id, sales_price FROM listing_listing WHERE id IN (%%s,%%s)", [W, MZ]): bk.write("listing " + str(r) + "\n")
    for r in q("SELECT * FROM listing_section_listing WHERE listing_id IN (%%s,%%s)", [W, MZ]): bk.write("section " + str(r) + "\n")
    bk.close()
    have = [r[0] for r in q("SELECT section_id FROM listing_section_listing WHERE listing_id=%%s", [W])]
    for s in cor:
        if s not in have: c.execute("INSERT INTO listing_section_listing (section_id, listing_id, featured) VALUES (%%s,%%s,0)", [s, W])
    c.execute("UPDATE listing_listing SET region_id=%%s WHERE id=%%s", [cr, W])
    c.execute("UPDATE listing_listing SET status_id=1, sales_price=225000 WHERE id=%%s", [MZ])
    try:
        from django.db import transaction; transaction.commit_unless_managed()
    except Exception: pass
    try: connection.commit()
    except Exception: pass
    print("@@APLICADO. Respaldo: %s")

''' % (AP, BK, BK)
open('/tmp/dbfix1_code.py', 'w').write(code)
print(sh('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/dbfix1_code.py 2>&1 | grep -o -E "@@.*|Error.*|error.*" | sed "s/^@@//" | cut -c1-1200'))
print('LISTO' + ('' if AP else ' (solo vista previa, no se cambio nada)'))
