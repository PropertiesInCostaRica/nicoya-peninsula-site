#!/usr/bin/env python3
# Soft 404 fix: send the empty /properties/<area>/ folders to their area pages,
# and remove the one redirecting address from sitemap.xml.
import os, re, shutil, subprocess, time

WEB = '/var/www/propertiesincostarica.com/web'
HT = os.path.join(WEB, '.htaccess')
SM = os.path.join(WEB, 'sitemap.xml')
SITE = 'https://www.propertiesincostarica.com'
MARK = '# PCR soft 404 fixes 2026-11-20'

M = [
    ('ciudad_colon', '/brasil_de_mora-ciudad_colon.html'), ('liberia', '/beach.html'),
    ('hermosa', '/playa-hermosa-real-estate.html'), ('playas_del_coco', '/beach.html'),
    ('montezuma', '/montezuma_real_estate.html'), ('Montezuma', '/montezuma_real_estate.html'),
    ('rohrmoser', '/rohrmoser.html'), ('uvita', '/uvita_real_estate.html'),
    ('santa_ana', '/santa_ana.html'), ('grecia', '/grecia_real_estate.html'),
    ('atenas', '/atenas_real_estate.html'), ('avalon', '/central-valley.html'),
    ('perez_zeledon', '/dominical-real-estate.html'), ('puriscal', '/puriscal.html'),
    ('lindora', '/santa_ana.html'), ('hacienda_pinilla', '/pinilla_real_estate.html'),
    ('naranjo', '/naranjo.html'), ('south_pacific', '/dominical-real-estate.html'),
    ('malpais', '/nicoya_peninsula_real_estate.html'),
    ('puntarenas', '/nicoya_peninsula_real_estate.html'),
    ('manuel_antonio', '/manuel_antonio_real_estate.html'), ('cariari', '/cariari_and_belen.html'),
    ('flamingo', '/flamingo_real_estate.html'), ('nosara', '/nosara_real_estate.html'),
]

def code(path):
    try:
        return subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-L', '--max-redirs', '5',
                                        '-w', '%{http_code}', SITE + path], timeout=30).decode().strip()
    except Exception:
        return 'ERR'

stamp = time.strftime('%Y%m%d-%H%M%S')
bk = '/root/respaldos/htaccess-' + stamp
shutil.copy2(HT, bk)
print('Respaldo: ' + bk)
s = open(HT, encoding='utf-8', errors='surrogateescape').read()
if MARK not in s:
    lines = ['', MARK, '<IfModule mod_rewrite.c>', 'RewriteEngine On']
    for d, t in M:
        lines.append('RewriteRule ^properties/%s/?(index\\.html?)?$ %s [R=301,L]' % (re.escape(d), t))
    lines.append('</IfModule>')
    open(HT, 'w', encoding='utf-8', errors='surrogateescape').write(s.rstrip('\n') + '\n' + '\n'.join(lines) + '\n')
    print('Reglas agregadas: %d' % len(M))

# sitemap: drop the address that redirects
if os.path.isfile(SM):
    sm = open(SM, encoding='utf-8', errors='surrogateescape').read()
    new = re.sub(r'\s*<url>\s*<loc>[^<]*coco_beach_residence\.html</loc>.*?</url>', '', sm, flags=re.S)
    if new != sm:
        shutil.copy2(SM, '/root/respaldos/sitemap-' + stamp + '.xml')
        open(SM, 'w', encoding='utf-8', errors='surrogateescape').write(new)
        print('Sitemap: quite coco_beach_residence.html')
    else:
        print('Sitemap: no habia nada que quitar')
else:
    print('Sitemap: no es un archivo, no se cambio')

time.sleep(1)
home = code('/')
if home != '200':
    shutil.copy2(bk, HT)
    raise SystemExit('ERROR: la pagina principal dio %s. Restaure el respaldo.' % home)
bad = 0
for d, t in M:
    c = subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-L', '-w', '%{http_code} %{url_effective}',
                                 SITE + '/properties/%s/' % d], timeout=30).decode().strip()
    if not c.startswith('200') or c.endswith('/properties/%s/' % d):
        bad += 1
    print('%s  <=  /properties/%s/' % (c.replace(SITE, ''), d))
print('Pagina principal: %s' % home)
print('Siguen mal: %d de %d' % (bad, len(M)))
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
