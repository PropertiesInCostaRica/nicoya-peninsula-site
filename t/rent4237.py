#!/usr/bin/env python3
# #4237 River Park condo (Santa Ana) is RENTED: price shows "Rented!" and its card is removed from listing pages.
import os, re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
P = W + 'properties/santa_ana/for_rent/spacious-condo.html'
bk = '/root/respaldos/rent4237-' + TS + '/'
os.makedirs(bk)
def save(path, s):
    shutil.copy(path, bk + path[len(W):].replace('/', '__'))
    open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s)
s = open(P, encoding='utf-8', errors='surrogateescape').read()
a = s.index('<!-- InstanceBeginEditable name="price" -->') + len('<!-- InstanceBeginEditable name="price" -->')
e = s.index('<!-- InstanceEndEditable -->', a)
s2 = s[:a] + '<div class="sold">Rented! Looking for similar properties? <a href="/contact.html">Contact Us</a></div>' + s[e:]
save(P, s2)
print('Pagina #4237: Rented!')
card = re.compile(r'(?:<!--#+INI#+-->\s*)?<article class="listing"(?:(?!</article>).)*?spacious-condo\.html(?:(?!</article>).)*?</article>(?:\s*<!--#+FIN#+-->)?', re.S)
n = 0
for root, dirs, files in os.walk(W):
    dirs[:] = [d for d in dirs if d not in ('blog', 'Images', 'images', 'cgi-bin', 'css', 'js', 'properties')]
    for f in files:
        if not f.endswith(('.html', '.htm')): continue
        p = os.path.join(root, f)
        t = open(p, encoding='utf-8', errors='surrogateescape').read()
        if 'santa_ana/for_rent/spacious-condo.html' not in t: continue
        t2, k = card.subn('', t)
        if k:
            save(p, t2); n += k
            print('Tarjeta quitada de ' + p[len(W):])
print('Tarjetas quitadas: %d. Respaldo en %s' % (n, bk))
print('LISTO')
