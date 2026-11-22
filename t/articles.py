#!/usr/bin/env python3
# 1) Homepage: put the Articles page link back (footer menu and blog section).
# 2) Articles page: add the "Whose Name" blog article at the top of the list.
import os, shutil, subprocess, time
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s):
    shutil.copy2(p, '/root/respaldos/' + os.path.basename(p) + '-' + ts)
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)

ART = 'https://www.propertiesincostarica.com/articles/index.htm'
home = None
for n in ('index.html', 'index.htm', 'index.php'):
    p = W + n
    if os.path.exists(p) and 'id="blog-feed"' in rd(p):
        home = p; break
if not home:
    print('Inicio: no encontrado')
else:
    s = rd(home); c = 0
    if 'articles/index.htm' not in s:
        old = '<a href="https://www.propertiesincostarica.com/blog/">BLOG</a><span aria-hidden="true">|</span>'
        if old in s:
            s = s.replace(old, old + '\n      <a href="' + ART + '">ARTICLES</a><span aria-hidden="true">|</span>', 1); c += 1
        old2 = '<a class="ns-more" href="https://www.propertiesincostarica.com/blog/">READ ALL ARTICLES ›</a>'
        if old2 in s:
            s = s.replace(old2, '<span><a class="ns-more" href="' + ART + '">ARTICLES ›</a> &nbsp; ' + old2 + '</span>', 1); c += 1
        if c: wr(home, s)
    print('Inicio (%s): enlaces agregados %d' % (os.path.basename(home), c))

p = W + 'articles/index.htm'
s = rd(p)
URL = 'https://www.propertiesincostarica.com/blog/whose-name-property-title-costa-rica/'
if URL in s:
    print('Articulos: ya estaba')
else:
    anchor = '<li><a href="the-caja-and-the-law'
    i = s.find(anchor)
    if i < 0:
        print('Articulos: no encontre la lista, no se cambio')
    else:
        ind = s[s.rfind('\n', 0, i) + 1:i]
        new = '<li><a href="' + URL + '">Whose Name Should Be on Your Costa Rica Property Title?</a></li>\n' + ind
        s = s[:i] + new + s[i:]
        wr(p, s)
        print('Articulos: Whose Name agregado arriba')
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
