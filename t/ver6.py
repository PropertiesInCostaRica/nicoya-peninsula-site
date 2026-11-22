#!/usr/bin/env python3
# READ ONLY: every file that uses the leads DB user u11. For each: does it read /mnt/pcr_db/access.php,
# or does it have the password written inside (fingerprint only)? Is it the CURRENT password?
import re, hashlib, subprocess, os
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8', 'replace')
cur = None
for l in open('/mnt/pcr_db/access.php', encoding='latin-1'):
    m = re.search(r"\$password_x\s*=\s*['\"](.*?)['\"]", l)
    if m: cur = m.group(1)
fp = lambda v: hashlib.sha256(v.encode()).hexdigest()[:6]
print('Clave actual (access.php): #' + fp(cur))
files = set(sh("grep -rlIE \"u11|db11|pcr_db/access\\.php\" --include='*.php' --include='*.py' --include='*.inc' /var/www /mnt/www /mnt/pcr_db 2>/dev/null").split())
files = sorted(set(os.path.realpath(f) for f in files))
usa, actual, vieja = [], [], []
for f in files:
    s = open(f, encoding='latin-1').read()
    if f == '/mnt/pcr_db/access.php': continue
    pws = set(m.group(2) for m in re.finditer(r"""\$\w*(pass|pwd)\w*\s*=\s*['"](.*?)['"]""", s, re.I))
    if cur in pws or (cur and cur in s): actual.append(f)
    elif 'pcr_db/access.php' in s: usa.append(f)
    else: vieja.append(f)
print('\nA) Leen el archivo unico access.php (se actualizan solos): %d' % len(usa))
for f in usa: print('   ' + f)
print('\nB) Tienen la CLAVE ACTUAL escrita adentro (hay que cambiarlos tambien): %d' % len(actual))
for f in actual: print('   ' + f)
print('\nC) Tienen una clave vieja o no conectan (no se afectan): %d' % len(vieja))
print('LISTO (solo lectura, claves ocultas)')
