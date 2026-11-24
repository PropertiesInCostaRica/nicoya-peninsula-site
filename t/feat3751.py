#!/usr/bin/env python3
# #3751 facts box: MAIN HOUSE and GUESTHOUSE in capitals, each on its own line with bedrooms and baths. Backup first.
import re, shutil, time
P = '/var/www/propertiesincostarica.com/web/properties/nicoya_peninsula/for_sale/abundance.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
a = s.index('<!-- InstanceBeginEditable name="features" -->')
a = s.index('-->', a) + 3
e = s.index('<!-- InstanceEndEditable -->', a)
f = '''
                    <ul id="data_table">
                      <li><strong>Land: 3,175 m2 (3/4 acre)</strong></li>
                      <li><strong>Total Construction: 600 m2 (6,500 sq.ft.)</strong></li>
                      <li><strong>MAIN HOUSE: 436 m2 (4,693 sq. ft.) | Bedrooms: 3 | Baths: 3</strong></li>
                      <li><strong>GUESTHOUSE: 75 m2 (800 sq. ft.) | Bedrooms: 2 | Baths: 1</strong></li>
                      <li><strong>Swimming Pool: 75 m2 (800 sq. ft.) | Garage: 4 | Ample Parking</strong></li>
                    </ul>  '''
shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
s = s[:a] + f + s[e:]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('LISTO: MAIN HOUSE y GUESTHOUSE en mayusculas')
