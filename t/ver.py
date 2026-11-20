#!/usr/bin/env python3
# Read only: shows how listing status is stored in the ID search table. Changes nothing.
import subprocess
def q(sql):
    return subprocess.check_output(['mysql', 'db1pcrappsearch', '-e', sql]).decode()
print(q("SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='db1pcrappsearch' AND TABLE_NAME='listing_listing'"))
for c in ['status', 'status_id', 'active', 'is_active', 'sold', 'published']:
    try:
        print(q('SELECT `%s`, COUNT(*) n FROM listing_listing GROUP BY `%s`' % (c, c)))
    except Exception:
        pass
print(q('SELECT COUNT(*) total FROM listing_listing'))
print('LISTO')
