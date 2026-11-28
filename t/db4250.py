#!/usr/bin/env python3
# Update the search entry for #4250 with the new Vainilla title and text.
import os
T = 'Building Lot of 8,444 m2 in Vainilla, Paquera, Nicoya Peninsula'
OP = 'In the small town of Vainilla, just outside Paquera on the southern Nicoya Peninsula, this lot of 8,444 m2 (over 2 acres) offers room for a home, a vacation retreat or a long term investment. It is offered at US$89,000, about US$10.50 per m2.'
code = '''from django.db import connection
c = connection.cursor()
c.execute("UPDATE listing_listing SET title=%%s, header=%%s, meta_title=%%s, opening_paragraph=%%s, meta_description=%%s WHERE id_code=4250", [%r, %r, %r, %r, %r])
print("@@filas cambiadas: %%s" %% c.rowcount)

try:
    from django.db import transaction; transaction.commit_unless_managed()
except Exception:
    pass

try:
    connection.commit()
except Exception:
    pass

c.execute("SELECT id, title FROM listing_listing WHERE id_code=4250")
print("@@ahora: %%s" %% (c.fetchall(),))

''' % (T, T, T, OP, OP[:160])
open('/tmp/db4250.py', 'w').write(code)
os.system('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/db4250.py 2>&1 | grep -o -E "@@.*|rror.*" | sed "s/^@@//"')
print('LISTO')
