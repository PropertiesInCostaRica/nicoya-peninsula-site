# Vista previa map-nuevo.html con el mapa interactivo de las 7 provincias (la pagina real no cambia)
import re, urllib.request
W = '/var/www/propertiesincostarica.com/web/'
s = open(W + 'map.html', encoding='utf-8', errors='surrogateescape').read()
wid = urllib.request.urlopen('https://www.properties-in-costa-rica.com/t/mapwidget.html').read().decode('utf-8')
a = s.find('<h2>Map of Costa Rica')
b = s.find('})();</script>', a)
if a < 0 or b < 0: raise SystemExit('No encontre el mapa viejo en map.html')
b += len('})();</script>')
s = s[:a] + wid + s[b:]
s = s.replace('</TITLE>', '</TITLE>\n<meta name="robots" content="noindex, nofollow">', 1) if '</TITLE>' in s else s.replace('</title>', '</title>\n<meta name="robots" content="noindex, nofollow">', 1)
open(W + 'map-nuevo.html', 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Vista previa: https://www.propertiesincostarica.com/map-nuevo.html')
print('LISTO (la pagina real no se cambio)')
