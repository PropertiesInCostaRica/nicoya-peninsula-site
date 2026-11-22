#!/usr/bin/env python3
# Build PREVIEW copies (name-nuevo.html, noindex) of old-template pages using the new homepage design.
# Live pages are NOT changed.
import re, os, html
W = '/var/www/propertiesincostarica.com/web/'
PAGES = ['map.html', 'financing.html', 'info/sanjose.html', 'articles/index.htm', 'videos/index.html', 'links.html']
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
home = rd(W + 'index.html')
hb = home.index('<body'); hm = home.index('<main id="main">') + len('<main id="main">')
HEADER = home[hb:hm]
FOOTER = home[home.index('</main>'):]
HEADTAIL = home[home.index('<link rel="preconnect"'):home.index('</head>')]
CSS = '''<style>
.pg-wrap{max-width:1100px;margin:0 auto;padding:40px 20px 60px;font-family:'Open Sans',sans-serif;color:#333;line-height:1.6}
.pg-wrap h1{font-family:Oswald,sans-serif;font-weight:400;font-size:32px;letter-spacing:.5px;color:#216B3D;margin:0 0 24px;text-transform:uppercase}
.pg-wrap h2,.pg-wrap h3{font-family:Oswald,sans-serif;font-weight:400;color:#216B3D}
.pg-wrap a{color:#048dc7}
.pg-wrap ul{padding-left:22px}.pg-wrap li{margin:6px 0}
.pg-wrap img{max-width:100%;height:auto}
.pg-wrap table{max-width:100%}
.pg-wrap iframe{max-width:100%}
</style>'''
def region(s, n):
    m = re.search(r'<!--\s*InstanceBeginEditable name="%s"\s*-->(.*?)<!--\s*InstanceEndEditable\s*-->' % n, s, re.S)
    return m.group(1) if m else ''
for rel in PAGES:
    p = W + rel
    if not os.path.exists(p):
        print(rel + ': no existe'); continue
    s = rd(p)
    dt = region(s, 'doctitle')
    mt = re.search(r'<title>(.*?)</title>', dt or s, re.S | re.I)
    title = mt.group(1).strip() if mt else 'Properties in Costa Rica'
    md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s, re.I)
    desc = md.group(1) if md else ''
    h1 = re.sub(r'<[^>]+>', '', region(s, 'title')).strip() or title
    content = region(s, 'content')
    extra = region(s, 'head')
    if not content.strip():
        print(rel + ': sin contenido, se salta'); continue
    canon = 'https://www.propertiesincostarica.com/' + rel
    out = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           '<meta name="robots" content="noindex, nofollow">\n<title>' + title + '</title>\n'
           + ('<meta name="description" content="' + desc + '">\n' if desc else '')
           + '<link rel="canonical" href="' + canon + '">\n' + HEADTAIL + '\n' + extra + '\n' + CSS + '\n</head>\n'
           + HEADER + '\n<section class="pg-wrap">\n<h1>' + h1 + '</h1>\n' + content + '\n</section>\n' + FOOTER)
    np = re.sub(r'\.(html?)$', r'-nuevo.\1', p)
    open(np, 'w', encoding='utf-8', errors='surrogateescape').write(out)
    print('Vista previa: https://www.propertiesincostarica.com/' + np[len(W):])
print('LISTO (las paginas reales no se cambiaron)')
