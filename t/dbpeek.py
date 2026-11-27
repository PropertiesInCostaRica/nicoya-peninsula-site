# Solo mira (no cambia nada): la tabla listing_listing del buscador
import subprocess, json
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
m = sh('find /home/dapps -maxdepth 3 -name manage.py 2>/dev/null | head -1')
if not m: raise SystemExit('No encontre manage.py')
d = m.rsplit('/', 1)[0]
py = sh("grep -oh 'python-home=[^ ]*' /etc/apache2/sites-enabled/* 2>/dev/null | head -1 | cut -d= -f2")
exe = (py + '/bin/python') if py else 'python3'
code = r'''
from django.db import connection
c = connection.cursor()
c.execute("SHOW COLUMNS FROM listing_listing")
cols = [r[0] for r in c.fetchall()]
print("COLUMNAS:", cols)
idc = [x for x in cols if 'id_code' in x.lower() or x.lower() in ('code','idcode','id_listing')]
print("columna de ID:", idc)
c.execute("SELECT COUNT(*), MAX(id) FROM listing_listing"); print("registros, max id:", c.fetchone())
if idc:
    k = idc[0]
    c.execute("SELECT * FROM listing_listing WHERE %s IN ('4233','4128','4228','4241','4242','4243','4244','4245','4246','4247','4248','4249')" % k)
    names = [x[0] for x in c.description]
    for r in c.fetchall():
        row = dict(zip(names, r))
        print("---", row.get(k)); print({a: (str(b)[:90] if b is not None else None) for a, b in row.items()})
'''
open('/tmp/dbpeek_code.py', 'w').write(code)
print('python:', exe)
print(sh('cd ' + d + ' && ' + exe + ' manage.py shell < /tmp/dbpeek_code.py 2>&1 | tail -60'))
print('LISTO')
