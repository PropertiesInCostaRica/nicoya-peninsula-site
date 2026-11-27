# 4128: precio nuevo US$225,000, diseno nuevo y tarjeta de vuelta en sus secciones
import os, re, shutil, time, subprocess, urllib.request
W = '/var/www/propertiesincostarica.com/web/'
P = 'properties/Montezuma/for_sale/magical-sanctuary.html'
B = '/root/respaldos/relist4128-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
def rd(p): return open(W + p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s):
    shutil.copy2(W + p, B + p.replace('/', '_'))
    open(W + p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
PRICE = 'Sales Price: <s>US$250,000</s> Reduced to US$225,000'
# 1. precio en la pagina
t = rd(P)
t = re.sub(r'(<!-- InstanceBeginEditable name="price" -->).*?(<!-- InstanceEndEditable -->)', lambda m: m.group(1) + PRICE + m.group(2), t, count=1, flags=re.S)
t = t.replace('235,000', '225,000')
wr(P, t); print('Precio nuevo en la pagina: US$225,000')
# 2. diseno nuevo
open('/root/newprop.py', 'wb').write(urllib.request.urlopen('https://www.properties-in-costa-rica.com/t/newprop.py').read())
print(subprocess.run(['python3', '/root/newprop.py', P], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip())
# 3. tarjeta en las secciones, justo despues de Featured
CARD = ('<!--###################INI#####################-->\n<article class="listing">\n'
 '<div class="listing_img"> <a href="/' + P + '"> <img src="/images/spacer.gif" data-src="https://cdn.propertiesincostarica.com/properties/Images/magical-sanctuary/p.gif" alt="Cradled by Nature, Hidden in the Blue Zone, land for sale in Montezuma" border="0" /> </a> <span class="idcodes">ID CODE: #4128</span></div>\n'
 '<div class="listing_data">\n<h3><a href="/' + P + '">Cradled by Nature, Hidden in the Blue Zone</a></h3>\n<ul>\n<li>Land: 1.31 acres (5,308 m2)</li>\n<li>' + PRICE + '</li>\n</ul>\n'
 '<div class="listing_content">Private land in Montezuma with its own legal water source, private access to the waterfall trail and the ocean only three minutes away, in the heart of the Nicoya Peninsula Blue Zone. <a href="/' + P + '"> More Information... </a> </div>\n'
 '</div>\n</article>\n<!--###################FIN#####################-->\n')
for pg in ('montezuma_real_estate.html', 'invest/income_producing.html', 'invest/land_development.html', 'beach-lots-and-farms.html',
           'eco-friendly.html', 'invest.html', 'mountain.html', 'residential_lots.html'):
    if not os.path.exists(W + pg): print('No existe', pg); continue
    s = rd(pg)
    if '#4128' in s: print('Ya estaba en', pg); continue
    a = s.find('featured_listing_of')
    e = s.find('</section>', a) if a >= 0 else -1
    if e < 0: print('No encontre Featured en', pg); continue
    e += len('</section>')
    s = s[:e] + '\n' + CARD + s[e:]
    wr(pg, s); print('Tarjeta agregada: https://www.propertiesincostarica.com/' + pg)
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
