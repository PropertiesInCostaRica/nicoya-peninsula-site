# Publica el mapa de provincias en map.html
import re, os, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
n = W + 'map-nuevo.html'
if not os.path.exists(n): raise SystemExit('Primero corra mapfun.py')
os.makedirs('/root/respaldos', exist_ok=True)
shutil.copy2(W + 'map.html', '/root/respaldos/map.html.' + time.strftime('%Y%m%d%H%M'))
s = open(n, encoding='utf-8', errors='surrogateescape').read()
s = re.sub(r'\n?<meta name="robots" content="noindex, nofollow">', '', s, count=1)
open(W + 'map.html', 'w', encoding='utf-8', errors='surrogateescape').write(s)
os.remove(n)
print('Publicado: https://www.propertiesincostarica.com/map.html')
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
