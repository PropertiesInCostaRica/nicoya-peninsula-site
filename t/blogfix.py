#!/usr/bin/env python3
# Remove the duplicated photo from the Thanksgiving post content (featured image stays)
import os, subprocess, glob
cands = ['/var/www/propertiesincostarica.com/web/blog/wp-load.php'] + glob.glob('/var/www/*/web/blog/wp-load.php')
WL = next((c for c in cands if os.path.exists(c)), None)
php = r'''<?php
require '%s';
$p = get_page_by_path('thanksgiving-kindness-plant-based-costa-rica', OBJECT, 'post');
if (!$p) { echo "NO ENCONTRE EL POST\n"; exit; }
$c = preg_replace('#^\s*<p><img[^>]*thanksgiving-kindness[^>]*/?>\s*</p>\s*#', '', $p->post_content, 1, $n);
if ($n) { wp_update_post(array('ID'=>$p->ID, 'post_content'=>$c)); echo "Foto repetida quitada\n"; } else { echo "No habia foto repetida\n"; }
echo "Foto principal: ".(has_post_thumbnail($p->ID) ? "si" : "NO")."\n";
echo get_permalink($p->ID)."\n";
''' % WL
open('/root/blogfix.php', 'w').write(php)
r = subprocess.run(['php', '/root/blogfix.php'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
print(r.stdout[-1500:]); os.remove('/root/blogfix.php'); print('LISTO')
