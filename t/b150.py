#!/usr/bin/env python3
# New page: Costa Rica beach homes and lots under US$150,000 (built from beach.html).
import os, re, shutil, subprocess, time

WEB = '/var/www/propertiesincostarica.com/web'
SITE = 'https://www.propertiesincostarica.com'
NEW = 'beach-homes-under-150k.html'
HOMES = ['4218', '3750', '4189', '4063', '4223']
LOTS = ['3985', '3624', '4140', '4024', '4018']
SOURCES = ['beach.html', 'homes.html', 'beach/homes_condos.html', 'residential_lots.html',
           'beach-lots-and-farms.html', 'nicoya_peninsula_real_estate.html', 'caribbean.html',
           'tambor_real_estate.html', 'ocean_view_properties.htm']

TITLE = 'Costa Rica Beach Homes for Sale Under US$150,000 | PCR'
DESC = ('Affordable beach homes and beach lots for sale in Costa Rica under US$150,000, '
        'from Paquera and the Nicoya Peninsula to Guanacaste and the Caribbean. Photos and prices.')
H1 = 'Costa Rica Beach Homes Under US$150,000'
INTRO = ('Yes, you can still buy a home near the beach in Costa Rica for under US$150,000. '
         'These are the most affordable beach homes and beach lots we have for sale right now, '
         'from Paquera and Bahia Gigante on the Nicoya Peninsula to Guanacaste and the Caribbean coast. '
         'Many buyers use them as a vacation home, a rental or a first step into Costa Rica. '
         'Every listing has photos, details and its ID code. Contact us to schedule a visit.')

def read(p):
    return open(os.path.join(WEB, p), encoding='utf-8', errors='surrogateescape').read()
def write(p, s):
    open(os.path.join(WEB, p), 'w', encoding='utf-8', errors='surrogateescape').write(s)

ART = re.compile(r'(?:<!--#+INI#+-->\s*)?<article class="listing">.*?</article>(?:\s*<!--#+FIN#+-->)?', re.S)
cards = {}
for src in SOURCES:
    if not os.path.isfile(os.path.join(WEB, src)):
        continue
    for m in ART.finditer(read(src)):
        block = m.group(0)
        for i in HOMES + LOTS:
            if i not in cards and re.search(r'#\s?%s\b' % i, block):
                cards[i] = block
missing = [i for i in HOMES + LOTS if i not in cards]
print('Tarjetas encontradas: %d de %d %s' % (len(cards), len(HOMES + LOTS), ('faltan ' + ' '.join(missing)) if missing else ''))

s = read('beach.html')
s = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s/%s">' % (SITE, NEW), s, count=1)
s = re.sub(r'<title>.*?</title>', '<TITLE>%s</TITLE>' % TITLE, s, count=1, flags=re.I | re.S)
s = re.sub(r'(<meta name="description" content=)"[^"]*"', r'\1"%s"' % DESC, s, count=1)
s = re.sub(r'(<!-- InstanceBeginEditable name="title" -->).*?(<!-- InstanceEndEditable -->)',
           lambda m: m.group(1) + H1 + m.group(2), s, count=1, flags=re.S)
s = s.replace('<p>Beachfront and ocean view homes, condos and lots in Guanacaste, the Nicoya Peninsula, the Central Pacific and the Caribbean.</p>',
              '<p>Affordable beach homes and lots for sale, all under US$150,000.</p>', 1)
s = re.sub(r'(<h2><a name="house_of_the_month" id="house_of_the_month"></a>)[^<]*(</h2>)',
           lambda m: m.group(1) + 'Beach Homes Under US$150,000' + m.group(2), s, count=1)

first = ART.search(s)
if not first:
    raise SystemExit('No encontre tarjetas en beach.html, no se creo nada')
body = ('<p style="font-size:16px;line-height:24px;margin:0 0 20px">' + INTRO + '</p>\n'
        + '\n'.join(cards[i] for i in HOMES if i in cards)
        + '\n<h2 style="clear:both;padding-top:20px">Beach Lots Under US$150,000</h2>\n'
        + '\n'.join(cards[i] for i in LOTS if i in cards) + '\n')
s = s[:first.start()] + '@@CARDS@@' + s[first.start():]
s = ART.sub('', s)
s = s.replace('@@CARDS@@', body, 1)
write(NEW, s)
print('Pagina creada: /' + NEW)

stamp = time.strftime('%Y%m%d-%H%M%S')
# link from beach.html
b = read('beach.html')
if NEW not in b:
    shutil.copy2(os.path.join(WEB, 'beach.html'), '/root/respaldos/beach-' + stamp + '.html')
    old = '<td><a href="beach_front_properties_only.htm">Beachfront Properties</a></td>'
    if old in b:
        b = b.replace(old, old + '\n                    <td><a href="/%s">Beach Homes Under $150K</a></td>' % NEW, 1)
        write('beach.html', b)
        print('Enlace agregado en beach.html')
    else:
        print('No encontre donde poner el enlace en beach.html')
# sitemap
sm = read('sitemap.xml')
if NEW not in sm:
    shutil.copy2(os.path.join(WEB, 'sitemap.xml'), '/root/respaldos/sitemap-' + stamp + '.xml')
    sm = sm.replace('</urlset>', '<url><loc>%s/%s</loc></url>\n</urlset>' % (SITE, NEW), 1)
    write('sitemap.xml', sm)
    print('Agregada al sitemap')
c = subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', SITE + '/' + NEW]).decode()
print('Pagina nueva responde: ' + c)
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
