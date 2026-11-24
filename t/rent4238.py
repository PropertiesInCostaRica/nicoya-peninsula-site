#!/usr/bin/env python3
# #4238 Forest Views condo (Santa Ana) is RENTED: page shows Rented!, cards marked Rented! and moved to the bottom
import os, re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
TS = time.strftime('%Y%m%d-%H%M%S')
P = W + 'properties/santa_ana/for_rent/forest-views.html'
KEY = 'santa_ana/for_rent/forest-views.html'
bk = '/root/respaldos/rent4238-' + TS + '/'
os.makedirs(bk)
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def save(path, s):
    shutil.copy(path, bk + path[len(W):].replace('/', '__'))
    open(path, 'w', encoding='utf-8', errors='surrogateescape').write(s)
TAGDIV = '<div class="sold">Rented! Looking for similar properties? <a href="/contact.html">Contact Us</a></div>'
s = rd(P)
a = s.index('<!-- InstanceBeginEditable name="price" -->') + len('<!-- InstanceBeginEditable name="price" -->')
e = s.index('<!-- InstanceEndEditable -->', a)
save(P, s[:a] + TAGDIV + s[e:])
print('Pagina #4238: Rented!')
card = re.compile(r'(?:<!--#+INI#+-->\s*)?<article class="listing"(?:(?!</article>).)*?forest-views\.html(?:(?!</article>).)*?</article>(?:\s*<!--#+FIN#+-->)?', re.S)
TAG = '<li>' + TAGDIV + '</li>'
n = 0
for root, dirs, files in os.walk(W):
    dirs[:] = [d for d in dirs if d not in ('blog', 'Images', 'images', 'cgi-bin', 'css', 'js', 'properties', 'emails')]
    for f in files:
        if not f.endswith(('.html', '.htm')) or '-nuevo' in f: continue
        p = os.path.join(root, f)
        t = rd(p)
        if KEY not in t: continue
        m = card.search(t)
        if not m: continue
        c = re.search(r'<article class="listing".*?</article>', m.group(0), re.S).group(0)
        if 'Rented!' not in c:
            c2, k = re.subn(r'<li>(?:(?!</li>).)*?Price(?:(?!</li>).)*?</li>', TAG, c, count=1, flags=re.S)
            c = c2 if k else re.sub(r'(<ul>)', lambda x: x.group(1) + TAG, c, count=1)
        block = '<!--###################INI#####################-->\n' + c + '\n<!--###################FIN#####################-->'
        t2 = t[:m.start()] + t[m.end():]
        i = t2.rfind('</article>')
        if i < 0:
            t2 = t[:m.start()] + block + t[m.end():]
        else:
            j = t2.find('<!--###################FIN', i)
            i = t2.find('-->', j) + 3 if 0 < j < i + 40 else i + 10
            t2 = t2[:i] + '\n' + block + t2[i:]
        save(p, t2); n += 1
        print('Tarjeta marcada Rented! y al final en ' + p[len(W):])
print('Paginas actualizadas: %d. Respaldo en %s' % (n, bk))
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
