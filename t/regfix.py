#!/usr/bin/env python3
# region_and_price/index-nuevo.html (PREVIEW): side margins, "All Costa Rica" name, empty link removed.
import re, shutil, time
P = '/var/www/propertiesincostarica.com/web/region_and_price/index-nuevo.html'
s = open(P, encoding='utf-8', errors='surrogateescape').read()
shutil.copy(P, '/root/respaldos/region_index-nuevo.html-' + time.strftime('%Y%m%d-%H%M%S'))
s = s.replace('id="costarica_cr"', 'id="costarica"').replace('<h3>Costarica</h3>', '<h3>All Costa Rica</h3>')
s = re.sub(r'<li>\s*(<a href="[^"]*">\s*</a>)?\s*</li>', '', s)
if 'id="rp-pad"' not in s:
    s = s.replace('</style>\n</head>', '#costa_rica_real_estate,.rp-grid,.rp-loc{box-sizing:border-box}'
                  '.rp-wrap{padding:0 16px}</style>\n</head>', 1) if '</style>\n</head>' in s else s
    a = s.index('<!-- InstanceBeginEditable name="content" -->') + len('<!-- InstanceBeginEditable name="content" -->')
    e = s.index('<!-- InstanceEndEditable -->', a)
    s = s[:a] + '<div class="rp-wrap" id="rp-pad">' + s[a:e] + '</div>' + s[e:]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('LISTO: https://www.propertiesincostarica.com/region_and_price/index-nuevo.html')
