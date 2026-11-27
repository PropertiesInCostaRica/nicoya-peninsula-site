# Pone una propiedad como primera en Featured. Uso: python3 feat.py <pagina> <ID>
# Si Featured ya tiene 2, la segunda baja a ser la primera de la lista normal.
import re, os, sys, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
p = sys.argv[1].replace('https://www.propertiesincostarica.com/', '').lstrip('/'); pid = sys.argv[2].lstrip('#')
f = W + p; s = open(f, encoding='utf-8', errors='surrogateescape').read()
INI = '<!--###################INI#####################-->'; FIN = '<!--###################FIN#####################-->'
art = r'(?:' + re.escape(INI) + r'\s*)?<article class="listing"(?:(?!</article>).)*?ID CODE:?\s*#' + pid + r'\b.*?</article>(?:\s*' + re.escape(FIN) + r')?'
m = re.search(art, s, re.S)
if not m: raise SystemExit('No encontre la tarjeta #' + pid + ' en ' + p)
card = re.search(r'<article.*</article>', m.group(0), re.S).group(0)
s = s[:m.start()] + s[m.end():]
fs = re.search(r'(<section class="featured_listing_of[^>]*>\s*(?:<h2>.*?</h2>)?)(.*?)(</section>)', s, re.S)
if not fs: raise SystemExit('No encontre la seccion Featured')
inner = fs.group(2)
cards = re.findall(r'<article class="listing".*?</article>', inner, re.S)
w = lambda x: INI + '\n' + x + '\n' + FIN
keep = [card] + cards[:1]; down = cards[1:]
new = fs.group(1) + '\n' + '\n'.join(w(x) for x in keep) + '\n' + fs.group(3) + ''.join('\n' + w(x) for x in down)
s = s[:fs.start()] + new + s[fs.end():]
os.makedirs('/root/respaldos', exist_ok=True)
shutil.copy2(f, '/root/respaldos/' + p.replace('/', '_') + '.feat.' + time.strftime('%Y%m%d%H%M'))
open(f, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Featured: #' + pid + ' primera en https://www.propertiesincostarica.com/' + p)
print('LISTO')
