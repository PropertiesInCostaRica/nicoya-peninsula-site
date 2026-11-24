#!/usr/bin/env python3
# #3751: adds the two Matterport 3D tours (Main House and Guest House). Backup first.
import shutil, time
P = '/var/www/propertiesincostarica.com/web/properties/nicoya_peninsula/for_sale/abundance.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
if 'TnLrCVA42E3' in s:
    print('Ya estaban los tours'); raise SystemExit
tours = ('\n<h2 id="vitual_tour">3D Virtual Tours</h2>\n'
         '<p><strong>Main House</strong></p>\n'
         '<iframe width="100%" height="480" src="https://my.matterport.com/show/?m=TnLrCVA42E3" frameborder="0" allowfullscreen allow="xr-spatial-tracking"></iframe>\n'
         '<p><strong>Guest House</strong></p>\n'
         '<iframe width="100%" height="480" src="https://my.matterport.com/show/?m=umKihGmmM89" frameborder="0" allowfullscreen allow="xr-spatial-tracking"></iframe>\n')
a = s.index('<!-- InstanceBeginEditable name="content" -->')
e = s.index('<!-- InstanceEndEditable -->', a)
shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
s = s[:e] + tours + s[e:]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('LISTO: tours 3D agregados')
