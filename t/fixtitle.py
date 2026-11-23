#!/usr/bin/env python3
# Fix: put back the missing </title> on the 2 pages marked SOLD today (#2568 and #4186). Backup first.
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
for rel in ['properties/puriscal/for_sale/amazing-central-valley-views-lot.html', 'properties/caribe/for-sale/rare-find.html']:
    p = W + rel
    s = open(p, encoding='utf-8', errors='surrogateescape').read()
    head = s[:s.lower().find('</head>')]
    if re.search(r'<title>.*?</title>', head, re.S | re.I):
        print(rel + ': ya estaba bien'); continue
    s2, n = re.subn(r'(<title>SOLD: [^<]*?)(\s*<)', r'\1</title>\2', s, count=1, flags=re.I)
    if n:
        shutil.copy2(p, '/root/respaldos/' + rel.replace('/', '__') + '-titulo-' + ts)
        open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
        print(rel + ': titulo corregido')
    else:
        print(rel + ': no encontre el titulo, no se cambio')
print('LISTO')
