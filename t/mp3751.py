#!/usr/bin/env python3
# #3751: adds the two Matterport 3D tours, and 'contact Klaudia Nabialek' links to the contact form. Backup first.
import shutil, time
P = '/var/www/propertiesincostarica.com/web/properties/nicoya_peninsula/for_sale/abundance.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
tours = ('\n<h2 id="vitual_tour">3D Virtual Tours</h2>\n'
         '<p><strong>Main House</strong></p>\n'
         '<iframe width="100%" height="480" src="https://my.matterport.com/show/?m=TnLrCVA42E3" frameborder="0" allowfullscreen allow="xr-spatial-tracking"></iframe>\n'
         '<p><strong>Guest House</strong></p>\n'
         '<iframe width="100%" height="480" src="https://my.matterport.com/show/?m=umKihGmmM89" frameborder="0" allowfullscreen allow="xr-spatial-tracking"></iframe>\n')
link = '<a href="#formproperty" onclick="var l=document.getElementById(\'link_to_the_form\');if(l){l.click();return false;}">contact Klaudia Nabialek</a>'
if link not in s:
    s = s.replace('contact Klaudia Nabialek.', link + '.', 1)
a = s.index('<!-- InstanceBeginEditable name="content" -->')
e = s.index('<!-- InstanceEndEditable -->', a)
shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
if 'TnLrCVA42E3' not in s:
    s = s[:e] + tours + s[e:]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('LISTO: tours 3D agregados')
