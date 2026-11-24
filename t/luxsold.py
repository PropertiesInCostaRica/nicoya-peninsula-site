#!/usr/bin/env python3
# luxury_estates_in_costa_rica-nuevo.html (PREVIEW): sold listings go back in, at the bottom, marked "Sold!".
import re, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
P = W + 'luxury_estates_in_costa_rica-nuevo.html'
old = open(W + 'luxury_estates_in_costa_rica.html', encoding='utf-8', errors='surrogateescape').read()
s = open(P, encoding='utf-8', errors='surrogateescape').read()
href = lambda c: (re.search(r'href="([^"]+)"', c) or re.search(r'()', c)).group(1)
have = set(href(c) for c in re.findall(r'<article class="listing".*?</article>', s, re.S))
sold = [c for c in re.findall(r'<article class="listing".*?</article>', old, re.S) if 'href=' in c and href(c) not in have]
if not sold:
    print('No hay vendidas que agregar'); raise SystemExit
tag = '<li><div class="sold">Sold! Looking for similar properties? <a href="/contact.html">Contact Us</a></div></li>'
out = []
for c in sold:
    c2, n = re.subn(r'<li>(?:(?!</li>).)*?(?:Sales Price|Price)(?:(?!</li>).)*?</li>', tag, c, count=1, flags=re.S)
    if not n:
        c2 = re.sub(r'(<ul>)', r'\1' + tag, c, count=1)
    out.append('<!--###################INI#####################-->\n' + c2 + '\n<!--###################FIN#####################-->')
i = s.rfind('</article>')
i = s.find('-->', s.find('<!--###################FIN', i)) + 3 if s.find('<!--###################FIN', i) > 0 else i + 10
shutil.copy(P, '/root/respaldos/luxury_estates_in_costa_rica-nuevo.html-' + time.strftime('%Y%m%d-%H%M%S'))
s = s[:i] + '\n' + '\n'.join(out) + s[i:]
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('Vendidas agregadas al final: %d' % len(sold))
print('LISTO: https://www.propertiesincostarica.com/luxury_estates_in_costa_rica-nuevo.html')
