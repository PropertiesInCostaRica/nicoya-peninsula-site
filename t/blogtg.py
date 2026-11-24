#!/usr/bin/env python3
# Publish the Thanksgiving kindness post on the PCR WordPress blog, with photo as featured image
import os, subprocess, glob
cands = ['/var/www/propertiesincostarica.com/web/blog/wp-load.php'] + glob.glob('/var/www/*/web/blog/wp-load.php') + glob.glob('/var/www/*/blog/wp-load.php')
WL = next((c for c in cands if os.path.exists(c)), None)
if not WL: raise SystemExit('No encontre wp-load.php del blog')
IMG = 'https://www.properties-in-costa-rica.com/t/thanksgiving-kindness.jpg'
TITLE = 'A Thanksgiving of Kindness: Gratitude, Pura Vida and a Plant Based Table in Costa Rica'
SLUG = 'thanksgiving-kindness-plant-based-costa-rica'
BODY = r'''<h2>Gratitude Starts With Kindness</h2>
<p>This Thanksgiving, we invite you to give thanks in a way that reaches a little further: through kindness. Kindness to the people around us, to the animals we share this planet with, and to the land that feeds us.</p>
<p>Here in Costa Rica, we are reminded of that every day. The morning birdsong, the neighbor who waves from the road, the farmer selling fresh mangoes at the corner stand. Gratitude is easy when life is this generous. Kindness is how we give some of it back.</p>
<h2>Kindness, the Pura Vida Way</h2>
<p>Pura vida is more than a greeting. It is a way of living that values people over hurry and simple joys over things.</p>
<p>You see it when a stranger stops to help push a car out of the mud on a rainy afternoon. You see it in the small town <em>ferias</em>, where families share recipes as freely as they share produce. And you see it in the way Costa Ricans make newcomers feel at home.</p>
<p>For many of our clients, this warmth is the real reason they choose Costa Rica. The views bring them here. The kindness makes them stay.</p>
<h2>Kindness to Animals and Nature</h2>
<p>Costa Rica has shown the world what kindness to nature can look like. In 2012 the country banned sport hunting, and about a quarter of its land is protected in national parks and reserves.</p>
<p>Across the country, wildlife rescue centers care for injured sloths, monkeys, toucans and sea turtles, and return them to the wild whenever they can. Many welcome volunteers and visitors, a beautiful way to spend a holiday weekend.</p>
<p>As a vegan, I find this one of the most meaningful parts of living here. Every creature, from the hummingbird at the feeder to the turtle on the beach at night, is a reminder that kindness should not stop at our own species.</p>
<h2>A Plant Based Thanksgiving Table, Costa Rica Style</h2>
<p>A kind table can be just as festive and abundant. Costa Rica's markets make it easy, with fresh, local produce all year round. Here are some ideas for a Thanksgiving feast where no one is left out:</p>
<ul>
<li><strong>Roasted squash with local herbs</strong>: ayote, the Costa Rican pumpkin, roasted with garlic, culantro and a little olive oil.</li>
<li><strong>Gallo pinto stuffing</strong>: rice and black beans with onion, sweet pepper and a touch of Salsa Lizano, a Tico twist on the classic.</li>
<li><strong>Yuca mash</strong>: creamy yuca with garlic and coconut milk instead of butter and cream.</li>
<li><strong>Sweet plantains</strong>: ripe pl&aacute;tano maduro baked until golden and caramelized.</li>
<li><strong>Picadillo de chayote</strong>: a light, colorful side of chayote, corn and sweet pepper.</li>
<li><strong>Pejibaye with lime</strong>: the peach palm fruit, a beloved local snack, perfect as an appetizer.</li>
<li><strong>Tropical fruit pie</strong>: pineapple, mango or guava over a coconut crust, served with fresh coffee from the Central Valley.</li>
</ul>
<p>Every dish celebrates what grows here, supports local farmers, and spares the animals. That feels like a very good reason to give thanks.</p>
<h2>Simple Ways to Share Kindness This Season</h2>
<ol>
<li>Thank someone who makes your daily life easier: the gardener, the guard at the gate, the cashier at the feria.</li>
<li>Visit or support a local wildlife rescue center or animal shelter.</li>
<li>Buy from small farmers and local markets.</li>
<li>Invite a new neighbor or a friend far from home to your table.</li>
<li>Try one plant based dish this holiday and share the recipe.</li>
<li>Pick up trash on your next walk on the beach.</li>
</ol>
<h2>Thank You From All of Us at Properties in Costa Rica</h2>
<p>To our clients, our sellers, our partners and our friends around the world: thank you. Your trust and kindness are the heart of everything we do.</p>
<p>If Costa Rica is calling you, a place where gratitude and kindness are part of everyday life, we would love to help you find your home here. Browse our listings at <a href="https://www.propertiesincostarica.com">https://www.propertiesincostarica.com</a> or call us toll free at 1 888 607 6772.</p>
<p>Happy Thanksgiving, and pura vida.</p>
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
$body = file_get_contents('/root/blogtg_body.html');
$id = wp_insert_post(array('post_title'=>'%s','post_name'=>'%s','post_content'=>$body,'post_status'=>'draft','post_author'=>$u?$u->ID:1), true);
if (is_wp_error($id)) { echo "ERROR: ".$id->get_error_message()."\n"; exit; }
$att = media_sideload_image('%s', $id, 'Mirtha hugging a rescued rooster', 'id');
if (is_wp_error($att)) { echo "FOTO ERROR: ".$att->get_error_message()."\n"; }
else {
  set_post_thumbnail($id, $att);
  $src = wp_get_attachment_url($att);
  $img = '<p><img class="aligncenter size-full" src="'.$src.'" alt="Mirtha hugging a rescued rooster" width="808" height="845" /></p>'."\n";
  wp_update_post(array('ID'=>$id,'post_content'=>$img.$body));
}
wp_update_post(array('ID'=>$id,'post_status'=>'publish'));
echo "PUBLICADO: ".get_permalink($id)."\n";
''' % (WL, SLUG, TITLE.replace("'", "\\'"), SLUG, IMG)
open('/root/blogtg_body.html', 'w').write(BODY)
open('/root/blogtg.php', 'w').write(php)
r = subprocess.run(['php', '/root/blogtg.php'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
print(r.stdout[-2000:])
os.remove('/root/blogtg.php'); os.remove('/root/blogtg_body.html')
print('LISTO')
