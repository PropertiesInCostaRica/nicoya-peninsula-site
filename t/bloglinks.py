#!/usr/bin/env python3
# Adds a "Properties for sale" box at the end of every blog post (small WordPress mu-plugin).
# To undo: delete /var/www/propertiesincostarica.com/web/blog/wp-content/mu-plugins/pcr-listing-links.php
import os, subprocess, time

WEB = '/var/www/propertiesincostarica.com/web'
MU = os.path.join(WEB, 'blog', 'wp-content', 'mu-plugins')
F = os.path.join(MU, 'pcr-listing-links.php')
SITE = 'https://www.propertiesincostarica.com'

PHP = r'''<?php
/*
Plugin Name: PCR listing links
Description: Adds links to PCR listings and area pages at the end of each blog post.
*/
add_filter('the_content', function ($c) {
    if (!is_singular('post') || !in_the_loop() || !is_main_query()) {
        return $c;
    }
    $s = 'https://www.propertiesincostarica.com/';
    $t = strtolower(get_post_field('post_name', get_the_ID()) . ' ' . get_the_title());
    $groups = array(
        array('/guanacaste|tamarindo|samara|nosara|pinilla|flamingo|conchal|liberia|coco|santa-cruz/', array(
            array('tamarindo-real-estate.html', 'Tamarindo homes and condos for sale'),
            array('nosara_real_estate.html', 'Nosara real estate'),
            array('samara_real_estate.html', 'Samara real estate'),
            array('pinilla_real_estate.html', 'Hacienda Pinilla real estate'))),
        array('/tambor|nicoya|montezuma|paquera|santa-teresa|mal-pais|cobano|tango|whale/', array(
            array('tambor_real_estate.html', 'Tambor real estate'),
            array('nicoya_peninsula_real_estate.html', 'Nicoya Peninsula real estate'),
            array('montezuma_real_estate.html', 'Montezuma real estate'),
            array('beach-homes-under-150k.html', 'Beach homes under US$150,000'))),
        array('/dominical|uvita|ojochal|osa|quepos|manuel-antonio|jaco|hermosa|savegre|corcovado/', array(
            array('dominical-real-estate.html', 'Dominical real estate'),
            array('uvita_real_estate.html', 'Uvita real estate'),
            array('manuel_antonio_real_estate.html', 'Manuel Antonio real estate'),
            array('jaco_real_estate.html', 'Jaco real estate'))),
        array('/caribbean|caribe|puerto-viejo|cahuita|limon|manzanillo|tortuguero|afro/', array(
            array('caribbean.html', 'Caribbean coast real estate'),
            array('puerto-viejo-real-estate.html', 'Puerto Viejo real estate'),
            array('beach.html', 'Beach homes and lots for sale'))),
        array('/central-valley|atenas|escazu|santa-ana|grecia|heredia|san-jose|alajuela|belen|rohrmoser|airport|eternal-spring/', array(
            array('central-valley.html', 'Central Valley real estate'),
            array('atenas_real_estate.html', 'Atenas real estate'),
            array('santa_ana.html', 'Santa Ana real estate'),
            array('escazu.htm', 'Escazu real estate'))),
        array('/beach|ocean|surf|turtle|whale|sea/', array(
            array('beach.html', 'Costa Rica beach homes for sale'),
            array('beach-homes-under-150k.html', 'Beach homes under US$150,000'),
            array('homes/ocean_view_homes.html', 'Ocean view homes for sale'))),
    );
    $links = array(
        array('homes.html', 'Costa Rica homes for sale'),
        array('beach-homes-under-150k.html', 'Beach homes under US$150,000'),
        array('residential_lots.html', 'Land and lots for sale'),
        array('central-valley.html', 'Central Valley real estate'));
    foreach ($groups as $g) {
        if (preg_match($g[0], $t)) {
            $links = $g[1];
            break;
        }
    }
    $feat = array(
        array('properties/puntarenas/for_sale/whale-bay-villa.html', 'Whale Bay Villa, Tambor, ID 4241, US$499,000'),
        array('properties/paquera/for-sale/free-standing-bungalow.html', 'Casa Mango, Paquera, ID 4189, US$119,000'),
        array('properties/puntarenas/for_sale/ocean-setting.html', 'Casa Leon del Mar, Tango Mar, ID 4228, US$1,900,000'));
    $h = '<div class="pcr-listing-links" style="clear:both;margin:30px 0 10px;padding:18px 20px;border:1px solid #e2d3a3;background:#fbf8ef">';
    $h .= '<p style="margin:0 0 8px;font-weight:bold;font-size:18px">Looking for property in Costa Rica?</p><ul style="margin:0 0 12px 18px">';
    foreach ($links as $l) {
        $h .= '<li><a href="' . $s . $l[0] . '">' . $l[1] . '</a></li>';
    }
    $h .= '</ul><p style="margin:0 0 6px;font-weight:bold">Featured listings</p><ul style="margin:0 0 12px 18px">';
    foreach ($feat as $l) {
        $h .= '<li><a href="' . $s . $l[0] . '">' . $l[1] . '</a></li>';
    }
    $h .= '</ul><p style="margin:0">Questions? <a href="' . $s . 'contact.html">Contact us</a> or WhatsApp <a href="https://api.whatsapp.com/send?phone=50688225061">+506 8822 5061</a>.</p></div>';
    return $c . $h;
}, 20);
'''

def code(url):
    try:
        return subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url], timeout=30).decode()
    except Exception:
        return 'ERR'

def page(url):
    try:
        return subprocess.check_output(['curl', '-s', url], timeout=30).decode('utf-8', 'replace')
    except Exception:
        return ''

if not os.path.isdir(MU):
    os.makedirs(MU)
    subprocess.call(['chown', '--reference=' + os.path.join(WEB, 'blog', 'wp-content'), MU])
open(F, 'w').write(PHP)
subprocess.call(['chown', '--reference=' + os.path.join(WEB, 'blog', 'wp-content'), F])
try:
    lint = subprocess.call(['php', '-l', F])
except OSError:
    lint = 0
time.sleep(1)
test = SITE + '/blog/pensionado-program-guide/?nocache=' + str(int(time.time()))
c1 = code(SITE + '/blog/')
c2 = code(test)
if lint != 0 or c1 != '200' or c2 != '200':
    os.remove(F)
    raise SystemExit('ERROR (php %s, blog %s, post %s). Quite el archivo, el blog quedo como antes.' % (lint, c1, c2))
html = page(test)
print('Blog: %s  Articulo: %s' % (c1, c2))
print('Caja de propiedades visible: %s' % ('SI' if 'pcr-listing-links' in html else 'NO (puede ser cache, revisar)'))
# Part 2: short intro paragraph at the top of homes.html
import shutil
HP = os.path.join(WEB, 'homes.html')
ANCHOR = '<p align="center"> <a href="top_houses.html">Top Houses in Costa Rica</a></p>'
INTRO = ('<div class="pcr-homes-intro" style="max-width:900px;margin:10px auto 15px;font-size:16px;line-height:24px;text-align:justify">'
         'Looking for a home in Costa Rica? Properties in Costa Rica has helped international buyers find houses, condos and family homes since 1999. '
         'Below are our current homes for sale across the country: beach and ocean view homes in Guanacaste, Tambor and the Nicoya Peninsula, '
         'mountain homes in Atenas and Grecia, and family homes in the Central Valley near Escazu and Santa Ana. '
         'Prices go from under US$100,000 to luxury estates. Every listing has photos, prices and an ID code, '
         'and our bilingual team can arrange private showings, in person or by video.</div>\n')
hs = open(HP, encoding='utf-8', errors='surrogateescape').read()
if 'pcr-homes-intro' in hs:
    print('Homes: la introduccion ya estaba')
elif ANCHOR in hs:
    shutil.copy2(HP, '/root/respaldos/homes-' + time.strftime('%Y%m%d-%H%M%S') + '.html')
    hs = hs.replace(ANCHOR, INTRO + ANCHOR, 1)
    open(HP, 'w', encoding='utf-8', errors='surrogateescape').write(hs)
    print('Homes: introduccion agregada. Pagina responde: ' + code(SITE + '/homes.html'))
else:
    print('Homes: no encontre donde ponerla, no se cambio')
if os.path.exists('/usr/local/bin/pcr-git-respaldo.sh'):
    subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
