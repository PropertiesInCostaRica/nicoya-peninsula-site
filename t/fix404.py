#!/usr/bin/env python3
# Fix the last 27 broken (404) addresses on propertiesincostarica.com with 301 redirects.
# Makes a backup of .htaccess, adds the rules, tests every address, and restores the
# backup automatically if the home page stops working.
import os, shutil, subprocess, time

WEB = '/var/www/propertiesincostarica.com/web'
HT = os.path.join(WEB, '.htaccess')
SITE = 'https://www.propertiesincostarica.com'
MARK = '# PCR 404 fixes 2026-11-20'

RULES = r'''
# PCR 404 fixes 2026-11-20
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule ^properties/v\.html$ / [R=301,L,NC]
RewriteRule ^properties/puntarenas/for_sale/dreams-at-sea\.ht$ /properties/puntarenas/for_rent/dreams-at-sea.html [R=301,L]
RewriteRule ^ultimate-guide-to-buying-a-property-in-costa-rica/?$ /blog/buying-a-property-in-costa-rica/ [R=301,L]
RewriteRule ^pavones(_real_estate)?\.html$ /beach.html [R=301,L]
RewriteRule ^contac\.html$ /contact.html [R=301,L]
RewriteRule ^contact0_esp\.html$ /contact_esp.html [R=301,L]
RewriteRule ^properties/escazu/five_star_exclusive_properties\.htm$ /luxury_estates_in_costa_rica.html [R=301,L]
RewriteRule ^properties/escazu/jaco_real_estate\.html$ /jaco_real_estate.html [R=301,L]
RewriteRule ^(click|cycle)$ /? [R=301,L]
RewriteRule ^properties/heredia/contact\.html$ /contact.html [R=301,L]
RewriteRule ^properties/colonial\.html$ /listings.html [R=301,L]
RewriteRule ^propiedades-exclusivas\.html$ /luxury_estates_in_costa_rica.html [R=301,L]
RewriteRule ^info\.html$ /contact.html [R=301,L]
RewriteRule ^propiedades-de-lago\.html$ /listings.html [R=301,L]
RewriteRule ^properties/escazu/residential_lots\.html$ /residential_lots.html [R=301,L]
RewriteRule ^region_and_price/costa_rica/price_range/properties/spaciousandbeautifulcondoswamazingview\.html$ /condos.html [R=301,L]
RewriteRule ^properties/fully_furnished_home_for_rent_in_ciudad_colon\.html.+ /long_term_rentals.html [R=301,L]
RewriteRule ^properties/(arboles|hermosa)/big/[0-9]+\.jpg'.* / [R=301,L]
RewriteRule ^costa-rica-real-estate/properties/beach_properties/best_deal/big/thebeach\.jpg'.* /beach.html [R=301,L]
RewriteRule ^properties/machotehtml$ /listings.html [R=301,L]
RewriteRule ^blog/guide-to-investor-residency/?$ /blog/what-buyers-and-investors-should-know/ [R=301,L]
</IfModule>
'''

TESTS = [
    '/properties/v.html', '/properties/puntarenas/for_sale/dreams-at-sea.ht',
    '/ultimate-guide-to-buying-a-property-in-costa-rica', '/pavones_real_estate.html',
    '/pavones.html', '/contac.html', '/contact0_esp.html',
    '/properties/escazu/five_star_exclusive_properties.htm',
    '/properties/escazu/jaco_real_estate.html', '/click?gid=78&id', '/cycle?gid=78&id',
    '/cycle?gid=78&t=_blank&id', '/properties/heredia/contact.html',
    '/properties/colonial.html', '/propiedades-exclusivas.html', '/info.html',
    '/propiedades-de-lago.html', '/properties/escazu/residential_lots.html',
    '/region_and_price/costa_rica/price_range/properties/spaciousandbeautifulcondoswamazingview.html',
    "/properties/fully_furnished_home_for_rent_in_ciudad_colon.html%3E%3CTITLE%3ELuxury%20house",
    "/properties/arboles/big/061.jpg',%27x%27",
    "/properties/hermosa/big/045.jpg',%27x%27",
    "/costa-rica-real-estate/properties/beach_properties/best_deal/big/thebeach.jpg',%27x%27",
    '/properties/machotehtml', '/blog/guide-to-investor-residency',
    '/blog/guide-to-investor-residency/',
]

def code(path):
    try:
        out = subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-L', '--max-redirs', '5',
                                       '-w', '%{http_code}', SITE + path], timeout=30)
        return out.decode().strip()
    except Exception as e:
        return 'ERR'

bk = '/root/respaldos/htaccess-' + time.strftime('%Y%m%d-%H%M%S')
os.makedirs('/root/respaldos', exist_ok=True)
s = open(HT, encoding='utf-8', errors='surrogateescape').read() if os.path.exists(HT) else ''
shutil.copy2(HT, bk) if os.path.exists(HT) else open(bk, 'w').close()
print('Respaldo: ' + bk)

if MARK in s:
    print('Las reglas ya estaban puestas, solo pruebo.')
else:
    open(HT, 'w', encoding='utf-8', errors='surrogateescape').write(s.rstrip('\n') + '\n' + RULES)
    print('Reglas agregadas.')

# The blog (WordPress) has its own .htaccess, so its rule goes there, above WordPress.
BHT = os.path.join(WEB, 'blog', '.htaccess')
BRULE = ('# PCR 404 fixes 2026-11-20\n<IfModule mod_rewrite.c>\nRewriteEngine On\n'
         'RewriteRule ^guide-to-investor-residency/?$ /blog/what-buyers-and-investors-should-know/ [R=301,L]\n'
         '</IfModule>\n\n')
bbk = None
if os.path.exists(BHT):
    b = open(BHT, encoding='utf-8', errors='surrogateescape').read()
    if MARK not in b:
        bbk = '/root/respaldos/blog-htaccess-' + time.strftime('%Y%m%d-%H%M%S')
        shutil.copy2(BHT, bbk)
        open(BHT, 'w', encoding='utf-8', errors='surrogateescape').write(BRULE + b)
        print('Regla del blog agregada. Respaldo: ' + bbk)

time.sleep(1)
if bbk and code('/blog/') != '200':
    shutil.copy2(bbk, BHT)
    print('ERROR en el blog, restaure su respaldo.')
home = code('/')
if home != '200':
    shutil.copy2(bk, HT)
    raise SystemExit('ERROR: la pagina principal dio %s. Restaure el respaldo. No se cambio nada.' % home)

bad = 0
for p in TESTS:
    c = code(p)
    if c != '200':
        bad += 1
    print('%s  %s' % (c, p[:70]))
print('Pagina principal: %s' % home)
print('Siguen mal: %d de %d' % (bad, len(TESTS)))
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
