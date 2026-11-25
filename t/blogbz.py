#!/usr/bin/env python3
# Publish the Thanksgiving kindness post on the PCR WordPress blog, with photo as featured image
import os, subprocess, glob
cands = ['/var/www/propertiesincostarica.com/web/blog/wp-load.php'] + glob.glob('/var/www/*/web/blog/wp-load.php') + glob.glob('/var/www/*/blog/wp-load.php')
WL = next((c for c in cands if os.path.exists(c)), None)
if not WL: raise SystemExit('No encontre wp-load.php del blog')
IMG = 'https://cdn.propertiesincostarica.com/properties/Images/turn-key-ocean-view-estate/new/34.jpg'
TITLE = 'Costa Rica\'s Blue Zone: Longevity Lessons from the Nicoya Peninsula'
SLUG = 'costa-rica-blue-zone-nicoya-peninsula'
BODY = r'''<p>Only five places on Earth have earned the name Blue Zone, and one of them is right here in Costa Rica. On the Nicoya Peninsula, an unusual number of people live into their 90s and beyond while staying active, independent and close to family. For many people dreaming of a life in Costa Rica, that is a powerful reason to look at this corner of the country.</p>
<h2>Where the term Blue Zone comes from</h2>
<p>Demographers Michel Poulain and Giovanni Mario Pes, together with National Geographic explorer Dan Buettner, set out to map the world's longevity hot spots. They named five: Okinawa (Japan), Sardinia (Italy), Ikaria (Greece), Loma Linda (California) and the Nicoya Peninsula (Costa Rica). In each of them, people live noticeably longer than average and suffer less from chronic illnesses such as heart disease and diabetes.</p>
<h2>The numbers behind Nicoya</h2>
<p>The key research was led by Costa Rican demographer Luis Rosero Bixby of the University of Costa Rica, with colleagues from Stanford and the University of California. Because Costa Rica has kept civil birth records since 1883, ages could be verified with confidence. The study found that older adults in Nicoya had a mortality rate roughly 30% lower than other Costa Ricans, and that a 60 year old man there had about double the odds of reaching 90 compared with a man of the same age in the United States.</p>
<p>The study area covers five cantons on the Guanacaste side of the peninsula: Nicoya, Santa Cruz, Carrillo, Hojancha and most of Nandayure. In 2021 these communities counted 57 centenarians and over 1,000 residents in their 90s.</p>
<h2>Eight everyday habits of Nicoya's elders</h2>
<ol>
<li><strong>Plan de vida:</strong> a reason to wake up each morning, whether family, work or community.</li>
<li><strong>Family first:</strong> older people usually live with or next to their children and grandchildren.</li>
<li><strong>Moving naturally:</strong> farming, walking and manual work instead of formal exercise.</li>
<li><strong>Simple, plant based meals:</strong> beans, corn tortillas, rice, squash and fruit, in modest portions, with a light dinner.</li>
<li><strong>Faith and friendship:</strong> strong social bonds that help keep stress low.</li>
<li><strong>Daily sunshine:</strong> plenty of time outdoors in a warm climate.</li>
<li><strong>Calcium rich water:</strong> many locals credit their mineral rich water, though science has not confirmed it.</li>
<li><strong>Health care for all:</strong> Costa Rica's public health system reaches even small rural towns.</li>
</ol>
<h2>A changing picture</h2>
<p>In 2023 Rosero Bixby published new findings showing that the longevity edge is clearest among Nicoyans born before 1930 and is shrinking in younger generations as diets and routines modernize. In other words, the secret is the lifestyle, not the address. Anyone who moves to the peninsula and adopts these habits can enjoy many of the same benefits.</p>
<h2>Making the peninsula your home</h2>
<p>From the Guanacaste beaches in the north to Paquera, Tambor, Tango Mar and Montezuma in the south, the Nicoya Peninsula offers the warm climate, fresh local food, outdoor living and close knit communities that define a Blue Zone. Properties in Costa Rica has homes, land and vacation rentals across the southern peninsula. You can browse them on our Nicoya Peninsula site:<br>
<a href="https://www.properties-in-costa-rica.com/">https://www.properties-in-costa-rica.com/</a></p>
<p>Or call us toll free at 1 888 607 6772 and we will help you find your own place in the Blue Zone.</p>
<p><em>Sources: Luis Rosero Bixby, William H. Dow and David H. Rehkopf, "The Nicoya region of Costa Rica: a high longevity island for elderly males" (Vienna Yearbook of Population Research, 2013); Luis Rosero Bixby, "The vanishing advantage of longevity in Nicoya, Costa Rica: A cohort shift" (Demographic Research, 2023); AARP International, "In the Zone"; Dan Buettner and National Geographic Blue Zones research.</em></p>
<p><strong>Mirtha Gomez</strong><br>Managing Partner, Broker and Owner<br>Properties in Costa Rica</p>'''
php = r'''<?php
require '%s';
require_once ABSPATH.'wp-admin/includes/media.php';
require_once ABSPATH.'wp-admin/includes/file.php';
require_once ABSPATH.'wp-admin/includes/image.php';
$ex = get_page_by_path('%s', OBJECT, 'post');
if ($ex) { echo "YA EXISTE: ".get_permalink($ex->ID)."\n"; exit; }
$u = get_user_by('email','admin@propertiesincostarica.com');
if (!$u) { $a = get_users(array('role'=>'administrator','number'=>1)); $u = $a ? $a[0] : null; }
$body = file_get_contents('/root/blogbz_body.html');
$id = wp_insert_post(array('post_title'=>'%s','post_name'=>'%s','post_content'=>$body,'post_status'=>'draft','post_author'=>$u?$u->ID:1), true);
if (is_wp_error($id)) { echo "ERROR: ".$id->get_error_message()."\n"; exit; }
$att = media_sideload_image('%s', $id, 'Beach on the Nicoya Peninsula, Costa Rica Blue Zone', 'id');
if (is_wp_error($att)) { echo "FOTO ERROR: ".$att->get_error_message()."\n"; }
else {
  set_post_thumbnail($id, $att);
  $src = wp_get_attachment_url($att);
}
wp_update_post(array('ID'=>$id,'post_status'=>'publish'));
echo "PUBLICADO: ".get_permalink($id)."\n";
''' % (WL, SLUG, TITLE.replace("'", "\\'"), SLUG, IMG)
open('/root/blogbz_body.html', 'w').write(BODY)
open('/root/blogbz.php', 'w').write(php)
r = subprocess.run(['php', '/root/blogbz.php'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
print(r.stdout[-2000:])
os.remove('/root/blogbz.php'); os.remove('/root/blogbz_body.html')
print('LISTO')
