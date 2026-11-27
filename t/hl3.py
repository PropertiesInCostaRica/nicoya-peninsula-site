# Cambia el titulo "Highlights" por titulos propios
import os, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/hl3-' + time.strftime('%Y%m%d%H%M') + '/'
T = {'properties/hacienda_pinilla/for_sale/charming-colonial-home.html': 'Colonial Charm at a Glance', 'properties/caribe/for-sale/colorful-vibes.html': 'Why This Business Works', 'properties/caribe/for-sale/tranquil-terrain.html': 'Key Features', 'properties/caribe/for-sale/paradise-compound.html': 'Live, Vacation and Earn', 'properties/caribe/for-sale/extraordinary-compound.html': 'The Compound at a Glance', 'properties/caribe/for-sale/dream-tropical-jungle.html': 'What Makes It Special', 'properties/tamarindo/for_sale/opportunity.html': 'Development Potential', 'properties/dominical/for_sale/ocean-view-eco-development-land.html': 'Why Develop Here', 'properties/dominical/for_sale/ocean_view_home_and_extra_land.html': 'What Makes This Home Special', 'properties/caribe/for-sale/caribbean-gem.html': 'The Compound at a Glance', 'properties/tambor/for_rent/oceanfront-estate.html': 'Why Book This Estate', 'properties/bahia-ballena/for-sale/oceanview-development-lands.html': 'Property Features', 'properties/herradura/for_sale/house_with_pool_and_equine_quarters.html': 'Property Features'}
n = 0
for p, title in T.items():
    f = W + p
    if not os.path.exists(f): print('NO EXISTE:', p); continue
    t = open(f, encoding='utf-8', errors='surrogateescape').read()
    nt = t.replace('<div class="highlights"><h2>Highlights</h2>', '<div class="highlights"><h2>' + title + '</h2>')
    if nt != t:
        os.makedirs(B, exist_ok=True); shutil.copy2(f, B + p.replace('/', '_'))
        open(f, 'w', encoding='utf-8', errors='surrogateescape').write(nt); n += 1
        print('Titulo nuevo:', title, '|', p)
print('Titulos cambiados:', n); print('LISTO')
