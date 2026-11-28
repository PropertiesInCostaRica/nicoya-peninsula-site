#!/usr/bin/env python3
# #4250: add 6 area photos (Paquera beaches, "Yo amo Paquera" sign, Paquera ferry) from PCR listings #4199 and #4084.
# Preview: python3 beach4250.py      Apply: python3 beach4250.py --aplicar
import os, shutil, sys, time
W = '/var/www/propertiesincostarica.com/web/'
REL = 'properties/paquera/for-sale/paquera-lot.html'
IMG = W + 'properties/Images/paquera-lot/opt/'
CDN = 'https://cdn.propertiesincostarica.com/properties/Images/paquera-lot/opt/'
ALT = 'Beaches and town of Paquera, Nicoya Peninsula, near Vainilla, Costa Rica'
I = 'properties/Images/'
SRC = [  # (new number, big photo, thumb)
 (11, I + 'revenue-home/opt/photo-1.jpg', I + 'revenue-home/opt/thumbs/photo-1.jpg'),
 (12, I + 'revenue-home/opt/photo-3.jpg', I + 'revenue-home/opt/thumbs/photo-3.jpg'),
 (13, I + 'casa-kolibri/opt/25.jpg', I + 'casa-kolibri/opt/thumbs/25.jpg'),
 (14, I + 'revenue-home/opt2/photo-7.jpg', I + 'revenue-home/opt2/thumbs/photo-7.jpg'),
 (15, I + 'revenue-home/opt2/photo-10.jpg', I + 'revenue-home/opt2/thumbs/photo-10.jpg'),
 (16, I + 'casa-kolibri/opt/26.jpg', I + 'casa-kolibri/opt/thumbs/26.jpg'),
]
MARK = '<h2>A Real Blue Zone Experience</h2>'
def row(ns): return '<p class="photo">\n' + ''.join('<a href="%s%d.jpg"><img src="%sthumbs/%d.jpg" alt="%s" width="250" height="187"></a>' % (CDN, n, CDN, n, ALT) for n in ns) + '\n</p>'
ADD = row([11, 12, 13]) + '\n' + row([14, 15, 16]) + '\n<p><em>Beaches, town and ferry of Paquera, near the lot.</em></p>\n'
for n, b, t in SRC:
    for p in (b, t):
        if not os.path.exists(W + p): raise SystemExit('No encuentro ' + p)
s = open(W + REL, encoding='utf-8', errors='surrogateescape').read()
if CDN + 'thumbs/11.jpg' in s: raise SystemExit('Ya estaban agregadas')
if MARK not in s: raise SystemExit('No encontre donde ponerlas')
print('6 fotos encontradas, se agregan antes de "A Real Blue Zone Experience"')
if '--aplicar' not in sys.argv:
    print('Vista previa. Para aplicar: python3 beach4250.py --aplicar'); raise SystemExit
B = '/root/respaldos/beach4250-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
shutil.copy2(W + REL, B + 'paquera-lot.html')
for n, b, t in SRC:
    shutil.copy2(W + b, IMG + '%d.jpg' % n)
    shutil.copy2(W + t, IMG + 'thumbs/%d.jpg' % n)
open(W + REL, 'w', encoding='utf-8', errors='surrogateescape').write(s.replace(MARK, ADD + MARK, 1))
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO. Respaldo en ' + B)
