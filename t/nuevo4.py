#!/usr/bin/env python3
# PREVIEWS (name-nuevo.html, noindex) of old pages using the same design as beach.html.
# Live pages are NOT changed.
import re, os
W = '/var/www/propertiesincostarica.com/web/'
PAGES = {
 'financing.html': 'Homes, land and investment properties in Costa Rica where the owner offers financing.',
 'articles/index.htm': 'Guides about buying, owning and living in Costa Rica.',
 'videos/index.html': 'Video tours of our properties for sale in Costa Rica.',
 'links.html': 'Useful Costa Rica resources for buyers, visitors and new residents.',
 'info/sanjose.html': 'Museums, theatres, parks and markets in downtown San Jose.',
 'map.html': 'Find properties for sale by region on the map of Costa Rica.',
}
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def region(s, n):
    a = s.find('<!-- InstanceBeginEditable name="%s" -->' % n)
    if a < 0: return None
    a = s.index('-->', a) + 3
    e = s.find('<!-- InstanceEndEditable -->', a)
    nxt = s.find('<!-- InstanceBeginEditable', a)
    if e > 0 and (nxt < 0 or e < nxt):
        return s[a:e]
    for end in ('<!--#################Article FIN-->', '<footer'):
        j = s.find(end, a)
        if j > 0:
            c = s[a:j].rstrip()
            return c[:-6] if c.endswith('</div>') else c
    return None
def put(s, n, val):
    a = s.index('<!-- InstanceBeginEditable name="%s" -->' % n)
    a = s.index('-->', a) + 3
    e = s.index('<!-- InstanceEndEditable -->', a)
    return s[:a] + val + s[e:]
shell = rd(W + 'beach.html')
for rel, intro in PAGES.items():
    p = W + rel
    if not os.path.exists(p):
        print(rel + ': no existe'); continue
    s = rd(p)
    content = region(s, 'content')
    if not content or not content.strip():
        print(rel + ': sin contenido, se salta'); continue
    mt = re.search(r'<title>(.*?)</title>', s, re.S | re.I)
    title = mt.group(1).strip() if mt else 'Properties in Costa Rica'
    md = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s, re.I)
    mk = re.search(r'<meta\s+name="keywords"\s+content="([^"]*)"', s, re.I)
    h1 = re.sub(r'<[^>]+>', '', region(s, 'title') or '').strip() or title
    head = region(s, 'head') or ''
    out = shell
    out = put(out, 'doctitle', '\n<TITLE>' + title + '</TITLE>\n')
    out = put(out, 'head', head)
    out = put(out, 'title', h1)
    out = put(out, 'content', content)
    out = re.sub(r'<link rel="canonical"[^>]*>\s*', '', out)
    out = re.sub(r'<meta\s+name="(description|keywords|robots)"[^>]*>\s*', '', out, flags=re.I)
    meta = '<meta name="robots" content="noindex, nofollow">\n<link rel="canonical" href="https://www.propertiesincostarica.com/' + rel + '">\n'
    if md: meta += '<meta name="description" content="' + md.group(1) + '">\n'
    if mk: meta += '<meta name="keywords" content="' + mk.group(1) + '">\n'
    out = out.replace('</TITLE>', '</TITLE>\n' + meta, 1)
    out = re.sub(r'(<h1 id="sp-h1">.*?</h1>\s*)<p>.*?</p>', lambda m: m.group(1) + '<p>' + intro + '</p>', out, count=1, flags=re.S)
    # relative paths: beach.html lives at the root; pages in folders need a base
    depth = rel.count('/')
    if depth:
        out = out.replace('<head>', '<head>\n<base href="https://www.propertiesincostarica.com/' + rel.rsplit('/', 1)[0] + '/">', 1)
        out = re.sub(r'(src|srcset|href)="(images/title-bg)', r'\1="/\2', out)
        out = re.sub(r'(\d+w, )(images/title-bg)', r'\1/\2', out)
    np = re.sub(r'\.(html?)$', r'-nuevo.\1', p)
    open(np, 'w', encoding='utf-8', errors='surrogateescape').write(out)
    print('Vista previa: https://www.propertiesincostarica.com/' + np[len(W):])
print('LISTO (las paginas reales no se cambiaron)')
