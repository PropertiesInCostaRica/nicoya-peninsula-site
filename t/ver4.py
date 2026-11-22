#!/usr/bin/env python3
# READ ONLY: how do the forms that are really used (mailer.php, p_recaptcha.php, newsletter.php)
# connect to the leads database? Passwords are hidden; only a short fingerprint is shown.
import re, hashlib, subprocess, os
D = '/var/www/clients/client1/web50/web/properties/forms/cgi/'
def mask(l):
    def rep(m):
        v = m.group(2)
        if v in ('u11', 'db11', 'localhost', '127.0.0.1', 'mysql.priv') or re.match(r'^[A-Za-z_./-]+\.(php|inc|ini)$', v) or len(v) < 3:
            return m.group(0)
        return m.group(1) + '#' + hashlib.sha256(v.encode()).hexdigest()[:6] + m.group(1)
    return re.sub(r"""(['"])(.*?)\1""", rep, l.rstrip())
for name in ('mailer.php', 'p_recaptcha.php', 'newsletter.php'):
    p = D + name
    print('=== ' + name + (' (no existe)' if not os.path.exists(p) else ''))
    if not os.path.exists(p): continue
    for i, l in enumerate(open(p, encoding='latin-1').read().splitlines(), 1):
        if re.search(r'mysql|mysqli|PDO|connect|include|require|hostname|username|password|\$db|dbname|user\s*=|pass', l, re.I):
            print('  %4d: %s' % (i, mask(l)[:170]))
print('=== Clave de u11 en los formularios viejos: #c954fe. ¿Coincide con alguna de arriba?')
print('LISTO (solo lectura, claves ocultas)')
