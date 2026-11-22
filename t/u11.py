#!/usr/bin/env python3
# READ ONLY: find every file on the server that uses the leads database user u11 (or database db11).
# Prints file names and line numbers only. Passwords are never printed. Changes nothing.
import os, re
ROOTS = ['/var/www', '/etc', '/root', '/home', '/usr/local/bin', '/opt', '/srv']
SKIP_DIRS = {'.git', 'node_modules', 'Images', 'images', 'respaldos', 'cache', 'uploads', 'proc'}
EXT = re.compile(r'\.(php|py|ini|cnf|conf|cfg|env|json|ya?ml|inc|sh|pl|js|txt)$|(^|/)\.env$|settings|config', re.I)
PAT = re.compile(r"""['"=:\s]u11['"\s;,]|['"=:\s/]db11['"\s;,]|user(name)?\s*=\s*u11\b|dbname\s*=\s*db11\b""", re.I)
found = []
for root in ROOTS:
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            p = os.path.join(d, f)
            if not EXT.search(p):
                continue
            try:
                if os.path.getsize(p) > 2000000:
                    continue
                with open(p, encoding='utf-8', errors='ignore') as fh:
                    for i, line in enumerate(fh, 1):
                        if PAT.search(line):
                            found.append((p, i))
            except Exception:
                pass
files = {}
for p, i in found:
    files.setdefault(p, []).append(i)
print('Archivos que usan u11 o db11: %d' % len(files))
for p, lines in sorted(files.items()):
    print('  %s  (lineas %s)' % (p, ', '.join(map(str, lines[:8]))))
print('LISTO (solo lectura, no se cambio nada y no se mostraron claves)')
