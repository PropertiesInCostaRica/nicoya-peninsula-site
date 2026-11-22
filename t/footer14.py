#!/usr/bin/env python3
# Put the full 14-link bottom menu on every page that has the new design footer.
import re, os, shutil, subprocess, time
W = '/var/www/propertiesincostarica.com/web/'
ts = time.strftime('%Y%m%d-%H%M%S')
B = 'https://www.propertiesincostarica.com/'
items = [('our.html','OUR COMPANY'),('listings.html','LISTINGS'),('list_your_properties.html','LIST YOUR PROPERTY'),
         ('faq.html','F.A.Q.'),('map.html','C.R MAP'),('financing.html','SELLER FINANCING'),
         ('info/sanjose.html','SAN JOSE ATTRACTIONS'),('blog/','BLOG'),('articles/index.htm','ARTICLES'),
         ('videos/index.html','VIDEOS'),('links.html','LINKS'),('inforequest.html','INFO REQUEST'),
         ('testimonials.html','TESTIMONIALS'),('contact.html','CONTACT US')]
sep = '<span aria-hidden="true">|</span>'
body = '\n      ' + ('\n      ' + sep + '\n      ').join('<a href="%s%s">%s</a>' % (B, h, t) for h, t in items) + '\n    '
os.makedirs('/root/respaldos/footer-' + ts, exist_ok=True)
done = []
for root, dirs, files in os.walk(W):
    dirs[:] = [d for d in dirs if d not in ('blog', 'Images', 'images', '.git', 'cgi-bin', 'css', 'js')]
    if root.count('/') - W.count('/') > 3:
        dirs[:] = []
    for f in files:
        if not re.search(r'\.html?$', f):
            continue
        p = os.path.join(root, f)
        try:
            s = open(p, encoding='utf-8', errors='surrogateescape').read()
        except Exception:
            continue
        if 'class="ft-nav"' not in s:
            continue
        s2 = re.sub(r'(<nav class="ft-nav"[^>]*>)(.*?)(</nav>)', lambda m: m.group(1) + body + m.group(3), s, count=1, flags=re.S)
        if s2 != s:
            shutil.copy2(p, '/root/respaldos/footer-' + ts + '/' + p[len(W):].replace('/', '__'))
            open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
            done.append(p[len(W):])
print('Paginas actualizadas: %d' % len(done))
for d in done:
    print('  ' + d)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
