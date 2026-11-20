#!/usr/bin/env python3
# Read only: what status_id 1 and 3 mean. Changes nothing.
import subprocess
def q(sql):
    try:
        return subprocess.check_output(['mysql', 'db1pcrappsearch', '-e', sql], stderr=subprocess.DEVNULL).decode()
    except Exception:
        return '(no)\n'
print(q("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='db1pcrappsearch' AND TABLE_NAME LIKE '%status%'"))
for t in ['listing_status', 'listing_listingstatus', 'listing_statuslisting']:
    print(q('SELECT * FROM %s' % t))
print(q("SELECT id, status_id, RIGHT(full_url, 60) url FROM listing_listing WHERE full_url LIKE '%whale-bay-villa%' OR full_url LIKE '%house-with-apartment%' OR full_url LIKE '%free-standing-bungalow%' OR full_url LIKE '%coco_beach_residence%'"))
print('LISTO')
