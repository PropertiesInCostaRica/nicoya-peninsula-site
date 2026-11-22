#!/usr/bin/env python3
# READ ONLY: show how the forms connect to the leads database, with passwords hidden.
import glob, re, collections
D = '/var/www/clients/client1/web50/web/properties/forms/cgi/'
files = sorted(f for f in glob.glob(D + '*.php') if re.search(r'u11|db11', open(f, encoding='utf-8', errors='ignore').read()))
print('Archivos de formularios con u11/db11: %d' % len(files))
def mask(l):
    def rep(m):
        v = m.group(2)
        keep = v in ('u11', 'db11', 'localhost', '127.0.0.1') or re.match(r'^[a-z_]+$', v) and len(v) < 4
        return m.group(1) + (v if keep else '*' * 6) + m.group(1)
    return re.sub(r"""(['"])(.*?)\1""", rep, l.rstrip())
shapes = collections.Counter()
for f in files:
    lines = open(f, encoding='utf-8', errors='ignore').read().splitlines()
    idx = [i for i, l in enumerate(lines[:30]) if re.search(r'u11|db11|pass|pwd|mysql|mysqli|PDO|host', l, re.I)]
    shapes[tuple(mask(lines[i]).strip() for i in idx[:6])] += 1
print('Formas distintas de conexion: %d' % len(shapes))
for shape, n in shapes.most_common(6):
    print('--- usada en %d archivos:' % n)
    for l in shape: print('   ' + l[:160])
print('Otros lugares fuera de cgi con u11/db11:')
import subprocess
print(subprocess.run("grep -rlE \"['\\\"]u11['\\\"]|['\\\"]db11['\\\"]\" --include='*.php' --include='*.py' /var/www 2>/dev/null | grep -v '/forms/cgi/' | head -20", shell=True, stdout=subprocess.PIPE).stdout.decode())
print('LISTO (solo lectura, claves ocultas)')
