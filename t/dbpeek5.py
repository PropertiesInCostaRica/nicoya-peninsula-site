# Solo mira (no cambia nada): diferencias entre Casa Coral (#4219, sale) y Whale Bay (#4241, no sale)
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
code = r'''from django.db import connection
c = connection.cursor()
def q(s, a=None):
    c.execute(s, a or []); return c.fetchall()

A = q("SELECT id FROM listing_listing WHERE id_code=4219")[0][0]
B = q("SELECT id FROM listing_listing WHERE id_code=4241")[0][0]
cols = [r[0] for r in q("SHOW COLUMNS FROM listing_listing")]
ra = q("SELECT * FROM listing_listing WHERE id=%s", [A])[0]
rb = q("SELECT * FROM listing_listing WHERE id=%s", [B])[0]
for i, k in enumerate(cols):
    if k in ("full_description", "opening_paragraph", "header", "meta_description", "meta_keywords"): print("@@" + k + " largo: coral=%s whale=%s" % (len(ra[i] or ""), len(rb[i] or "")))
    elif ra[i] != rb[i]: print("@@DIF " + k + ": coral=" + unicode(ra[i])[:60] + " | whale=" + unicode(rb[i])[:60])

for (t,) in q("SHOW TABLES"):
    cl = [r[0] for r in q("SHOW COLUMNS FROM " + t)]
    if "listing_id" in cl:
        print("@@TABLA " + t + ": coral=%s whale=%s" % (q("SELECT COUNT(*) FROM " + t + " WHERE listing_id=%s", [A])[0][0], q("SELECT COUNT(*) FROM " + t + " WHERE listing_id=%s", [B])[0][0]))

'''
open('/tmp/dbpeek5_code.py', 'w').write(code)
print(sh('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/dbpeek5_code.py 2>&1 | grep -o -E "@@.*|Error.*" | sed "s/^@@//" | cut -c1-300'))
print('LISTO')
