#!/usr/bin/env python3
# Redirect visitors who land on the CDN copy of a page (cdn.propertiesincostarica.com)
# to the real page on www. Every page loads modernizr from www, so a small line
# added to that file covers the whole site. Backup is made first.
# Usage: python3 cdnjs.py            (preview)
#        python3 cdnjs.py --aplicar  (apply)
#        python3 cdnjs.py --quitar   (remove)
import sys, shutil, time, os
F = '/var/www/propertiesincostarica.com/web/js/vendor/modernizr-2.5.3.min.js'
MARK = '/*pcr-cdn-redirect*/'
SNIP = ('\n' + MARK + ';(function(){try{if(location.hostname==="cdn.propertiesincostarica.com"'
        '&&!/\\.(jpe?g|png|gif|webp|css|js|pdf)$/i.test(location.pathname)){'
        'location.replace("https://www.propertiesincostarica.com"+location.pathname+location.search+location.hash)}'
        '}catch(e){}})();\n')
src = open(F, encoding='utf-8', errors='replace').read()
has = MARK in src
print('Archivo:', F, '| tamano', len(src), '| ya tiene la linea:', has)
if '--quitar' in sys.argv:
    if not has: print('Nada que quitar'); sys.exit()
    new = src[:src.index('\n' + MARK)]
elif '--aplicar' in sys.argv:
    if has: print('Ya estaba aplicado'); sys.exit()
    new = src + SNIP
else:
    print('Vista previa. Se agregaria:', SNIP.strip())
    print('Para aplicar: python3 cdnjs.py --aplicar'); sys.exit()
os.makedirs('/root/respaldos', exist_ok=True)
b = '/root/respaldos/modernizr-' + time.strftime('%Y%m%d%H%M%S') + '.js'
shutil.copy2(F, b)
open(F, 'w', encoding='utf-8').write(new)
print('OK. Respaldo:', b)
