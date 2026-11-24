#!/usr/bin/env python3
# #3751: Matterport 3D tours, 'contact Klaudia Nabialek' links to the contact form,
# photos 3 per row (2 at the end). Backup first.
import re, shutil, time
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
C = 'https://cdn.propertiesincostarica.com/properties/Images/turn-key-ocean-view-estate/opt/'
ROWS = [[24, 25, 11, 0, 1, 2], [3, 4, 5, 6, 7, 8, 9, 10, 12], [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23],
        [26, 27, 28, 29, 30], [31, 32, 33], [34, 35, 36, 37, 38], [39, 40]]
blocks = list(re.finditer(r'<p class="photo">.*?</p>', s, re.S))
if len(blocks) == len(ROWS):
    out = s[:blocks[0].start()]
    for i, (m, nums) in enumerate(zip(blocks, ROWS)):
        alt = 'Ocean view estate, pool, guest casita, Tango Mar, Nicoya Peninsula, house for sale, Costa Rica'
        a = lambda n: '<a href="%s%d.jpg"><img src="%sthumbs/%d.jpg" alt="%s" width="250" height="187"></a>' % (C, n, C, n, alt)
        rows = [nums[k:k + 3] for k in range(0, len(nums), 3)]
        html = '\n'.join('<p class="photo">\n' + ''.join(a(n) for n in r) + ('\n<span class="to_enlarge">Click on the pictures to enlarge</span>' if i == 0 and j == 0 else '') + '\n</p>' for j, r in enumerate(rows))
        out += html + s[m.end():(blocks[i + 1].start() if i + 1 < len(blocks) else len(s))]
    s = out
else:
    print('Grupos de fotos: %d, no se reordenaron' % len(blocks))
a = s.index('<!-- InstanceBeginEditable name="content" -->')
e = s.index('<!-- InstanceEndEditable -->', a)
shutil.copy(P, '/root/respaldos/abundance.html-' + time.strftime('%Y%m%d-%H%M%S'))
if 'TnLrCVA42E3' not in s:
    s = s[:e] + tours + s[e:]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('LISTO: tours 3D, enlace al formulario y fotos de 3 en 3')
