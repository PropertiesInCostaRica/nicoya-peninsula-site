# -*- coding: utf-8 -*-
# Testimonios nuevos (resenas reales de Google 2025 y 2026) en la pagina de inicio y en testimonials.html
import re, os, time, shutil, html
W = '/var/www/propertiesincostarica.com/web/'
B = '/root/respaldos/testi-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
def rd(p): return open(W + p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s):
    shutil.copy2(W + p, B + p.replace('/', '_'))
    open(W + p, 'w', encoding='utf-8', errors='surrogateescape').write(s)

# (nombre, rol, anio, texto completo tal como esta en Google)
R = [
('Mike Zoto', 'Buyer', '2026', 'My agent Mirtha Gomez turned a complicated purchase into a successful closing. The lending institution had required 3 extensions which made the seller and his agent very uncomfortable. She was able to smooth them over each time an extension was requested. She also helped with the escrow company and lawyers from the bank. I am not sure this transaction would have happened without her. Thanks Mirtha, I was extremely lucky to have you.'),
('Donna Papazian', 'Buyer', '2026', 'Mirtha and her team are incredible. As a client, I felt listened to and valued to find the perfect property for my needs. I never felt pressured and could trust she would patiently deliver my dream home, which she did!! The best in the business!'),
('James VanderWoude', 'Seller', '2026', 'Mirtha is a Great asset and helped us sell our home and took care of so many details. I highly recommend her and her team!'),
('Jean Claude Blaise', 'Seller', '2026', 'Excellent professional service to help find the right buyer for our farm, and assist until final signature.'),
('Raquel Moya', 'Client', '2026', 'Fue una gran experiencia trabajar con Mirtha!'),
('Kasie Agarwal', 'Buyer', '2026', 'Mirtha, is an excellent agent. She goes above &amp; beyond to help her clients. She is patient &amp; understanding. We are new to Costa Rica and she eased the process for us. We are fortunate to have found her.'),
('Keelay Busamonte', 'Buyer', '2026', 'Mirtha has a way of figuring out how to get things done, and I\'ve been following her for years through her emails. After seeing many, many properties, we found the property of our dreams thanks to her. I would highly recommend Mirtha as she is great to work with and has an amazing heart. Pura Vida'),
('Julio Garay', 'Tenant', '2026', 'If I have anything to say about this company is that they literally go above and beyond what is required of them. Mirtha was a saving grace for my family and I. We came to Costa Rica thinking we had a house ready for us but ended up not being the case. After getting contact with Properties in Costa Rica and Mirtha in particular we found a beautiful 2/2 apartment in Santa Ana. She helped us navigate how to pay for the electricity and water. Got me in contact with a internet company to get wifi connected. Words can not express how grateful we are to her.'),
('Leonardo Cervantes', 'Seller', '2025', 'I listed my property in Costa Rica in November of 2023. By February of the following year, we had already received an offer and proceeded directly to closing. The entire process was seamless, a testament to the professionalism, hard work and transparency of Ms. Mirtha Gomez and her team at Properties in Costa Rica.'),
('David Gorrell', 'Buyer', '2025', 'Mirtha was wonderful! I can\'t begin to explain how helpful she was in finding and closing on a property in San Jose. Not only did she make that transaction happen smoothly but she was also invaluable in helping me open a corporation, open bank accounts, help with purchasing a car, and quite a few other challenges I faced. She goes above and beyond any expectations I had for a real estate agent/broker. I can\'t recommend her enough!'),
('Scott', 'Buyer', '2025', 'Mirtha worked tirelessly to help me purchase property in Costa Rica and went "above and beyond" in solving the many problems a new ex-pat faces. Everything from recommending a lawyer to helping me find a car to translation services and advice... I cannot recommend her highly enough.'),
('Wendy Meritt', 'Client', '2025', 'We\'ve been using this company for about 4 years and the service is A++! She has found us a few amazing properties in Costa Rica and we couldn\'t be happier! The constant support we get from the Broker and staff is second to none and I highly recommend this Brokerage firm!'),
('Camden Dore', 'Buyer', '2025', 'The team at Properties in Costa Rica are very professional and honest. They went above and beyond to make my property purchase possible.'),
('Debra Peredo', 'Tenant', '2025', 'Everyone at Properties in Costa Rica is a professional and experts at what they do. They know the land and market and answered every question I had throughout the process of looking for a rental property.'),
]
def short(n):
    p = n.split()
    return (p[0] + ' ' + p[-1][0] + '.') if len(p) > 1 else p[0]

# ---------- testimonials.html ----------
t = rd('testimonials.html')
if 'Google Review' in t:
    print('testimonials.html ya tiene las resenas de Google')
else:
    rows = ''
    for n, rol, y, x in R:
        rows += ('\n<tr>\n                  <td bgcolor="#FFFFF4" style="border:1px solid #FFCC00;">\n'
                 '                    <p><small>Google Review, ' + y + ' &#9733;&#9733;&#9733;&#9733;&#9733;</small></p>\n'
                 '                    <p>"' + x + '"</p>\n'
                 '                    <p><strong>' + short(n) + '</strong> &middot; ' + rol + '</p>\n'
                 '                  </td>\n                </tr> <!-- end -->\n')
    a = '<table width="100%" height="72" border="0" cellpadding="6" cellspacing="8" class="testimon">'
    if a not in t: raise SystemExit('No encontre la tabla de testimonios')
    t = t.replace(a, a + '\n' + rows, 1)
    wr('testimonials.html', t)
    print('Agregadas %d resenas: https://www.propertiesincostarica.com/testimonials.html' % len(R))

# ---------- pagina de inicio ----------
H = {
'Mike Zoto': 'My agent Mirtha Gomez turned a complicated purchase into a successful closing... I am not sure this transaction would have happened without her.',
'Donna Papazian': 'Mirtha and her team are incredible. I never felt pressured and could trust she would patiently deliver my dream home, which she did!! The best in the business!',
'Leonardo Cervantes': 'I listed my property in November of 2023. By February we had already received an offer and proceeded directly to closing. The entire process was seamless.',
}
YR = {n: (rol, y) for n, rol, y, x in R}
h = rd('index.html')
g = re.search(r'(<div class="testi-grid">)(.*?)(</div>\s*</div>\s*</section>)', h, re.S)
if not g: raise SystemExit('No encontre los testimonios del inicio')
figs = re.findall(r'<figure>.*?</figure>', g.group(2), re.S)
if not figs: raise SystemExit('No hay figuras')
svg = re.search(r'<svg.*?</svg>', figs[0], re.S).group(0)
new = ''
for n, x in H.items():
    rol, y = YR[n]
    new += ('\n<figure> ' + svg + ' <blockquote>' + x + '</blockquote> <figcaption>' + short(n).upper() +
            ' <span>&middot; ' + rol + ', ' + y + ' &middot; Google Review</span></figcaption> </figure>')
h = h[:g.start(2)] + new + '\n' + h[g.end(2):]
wr('index.html', h)
print('Inicio con testimonios nuevos: https://www.propertiesincostarica.com/')
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
