#!/usr/bin/env python3
# Temporary: copy the old favicons to the PCR website so Claude can show them to Mirtha.
# Nothing in use is changed. (Files named favicon-ver-*.ico, removed later.)
import shutil
W = '/var/www/propertiesincostarica.com/web/'
for i, src in enumerate(['/mnt/www/clients/client1/web50/web/favicon.ico',
                         '/mnt/www/clients/client1/web47/web/_old/favicon.ico',
                         '/mnt/www/clients/client1/web37/web/public/favicon.ico'], 1):
    try:
        shutil.copy2(src, W + 'favicon-ver-%d.ico' % i); print('Copia %d: OK' % i)
    except Exception as e:
        print('Copia %d: %s' % (i, e))
print('LISTO')
