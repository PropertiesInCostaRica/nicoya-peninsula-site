# Vista previa: Whale Bay Villa con botones de WhatsApp (la pagina real no cambia)
import urllib.request
W = '/var/www/propertiesincostarica.com/web/'
P = 'properties/puntarenas/for_sale/whale-bay-villa'
s = open(W + P + '.html', encoding='utf-8', errors='surrogateescape').read()
snip = urllib.request.urlopen('https://www.properties-in-costa-rica.com/t/wa-snippet.html').read().decode('utf-8')
s = s.replace('</head>', '<meta name="robots" content="noindex, nofollow">\n</head>', 1)
i = s.rfind('</body>')
s = s[:i] + snip + '\n' + s[i:]
open(W + P + '-wa.html', 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Vista previa: https://www.propertiesincostarica.com/' + P + '-wa.html')
print('LISTO (la pagina real no se cambio)')
