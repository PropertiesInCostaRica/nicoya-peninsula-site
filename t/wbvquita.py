#!/usr/bin/env python3
# Whale Bay Villa: remove 8 repeated photos and rebuild the photo rows.
import re, shutil, subprocess, time

P = '/var/www/propertiesincostarica.com/web/properties/puntarenas/for_sale/whale-bay-villa.html'
RM = {19, 22, 24, 27, 32, 33, 34, 36}
# rows per section, in page order (each inner list is one row)
NEWROWS = [
    [[1, 20, 21]],
    [[4, 15, 12], [18, 10, 35]],
    [[5, 16, 17], [6, 7, 23], [25, 26], [28, 29]],
    [[2, 11], [13, 14]],
    [[37, 38]],
    [[3, 30, 31]],
    [[9, 8]],
]

bk = '/root/respaldos/whale-bay-villa-' + time.strftime('%Y%m%d-%H%M%S') + '.html'
shutil.copy2(P, bk)
s = open(P, encoding='utf-8', errors='surrogateescape').read()

row_re = re.compile(r'<p class="photo">.*?</p>', re.S)
link_re = re.compile(r'<a [^>]*?photo-(\d+)\.jpg.*?</a>', re.S)

rows = list(row_re.finditer(s))
links = {}
for r in rows:
    for m in link_re.finditer(r.group(0)):
        links[int(m.group(1))] = m.group(0)
print('Filas actuales: %d, fotos: %d' % (len(rows), len(links)))

# group consecutive rows into sections (rows separated only by whitespace)
sections = []
prev_end = None
for r in rows:
    if prev_end is not None and s[prev_end:r.start()].strip() == '':
        sections[-1].append(r)
    else:
        sections.append([r])
    prev_end = r.end()
print('Secciones: %d' % len(sections))
if len(sections) != len(NEWROWS):
    raise SystemExit('Estructura distinta, no se cambio nada')

sample = rows[0].group(0)
sep = sample[sample.index('>') + 1:sample.index('<a')]  # whitespace before first link
between = '\n'
m2 = re.search(r'</a>(\s*)<a', sample)
if m2:
    between = m2.group(1)
tail = sample[sample.rindex('</a>') + 4:sample.rindex('</p>')]

out = []
pos = 0
for sec, newrows in zip(sections, NEWROWS):
    out.append(s[pos:sec[0].start()])
    indent = s[s.rfind('\n', 0, sec[0].start()) + 1:sec[0].start()]
    built = []
    for row in newrows:
        built.append('<p class="photo">' + sep + between.join(links[n] for n in row) + tail + '</p>')
    out.append(('\n' + indent).join(built))
    pos = sec[-1].end()
out.append(s[pos:])
s2 = ''.join(out)

left = set(int(x) for x in re.findall(r'whale-bay-villa-2/opt/photo-(\d+)\.jpg', s2))
bad = left & RM
print('Fotos en la pagina ahora: %d' % len(left))
if bad:
    raise SystemExit('Error, quedan: %s' % sorted(bad))
open(P, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
print('Respaldo: ' + bk)
subprocess.call(['/usr/local/bin/pcr-git-respaldo.sh'])
print('LISTO')
