#!/usr/bin/env python3
# READ ONLY: find the forms really used by propertiesincostarica.com and show how they connect
# to the leads database. Passwords hidden (short fingerprint only).
import re, hashlib, subprocess, os
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8', 'replace').strip()
real = os.path.realpath('/var/www/propertiesincostarica.com/web')
print('Carpeta real del sitio: ' + real)
def mask(l):
    def rep(m):
        v = m.group(2)
        if v in ('u11', 'db11', 'localhost', '127.0.0.1', 'mysql.priv') or re.search(r'\.(php|inc|ini|html?)$', v) or len(v) < 3 or ' ' in v:
            return m.group(0)
        return m.group(1) + '#' + hashlib.sha256(v.encode()).hexdigest()[:6] + m.group(1)
    return re.sub(r"""(['"])(.*?)\1""", rep, l.rstrip())
seen = set()
for name in ('mailer.php', 'p_recaptcha.php', 'newsletter.php'):
    cands = [real + '/properties/forms/cgi/' + name] + sh("find /var/www -path '*forms/cgi/%s' 2>/dev/null | head -5" % name).split()
    for p in cands:
        rp = os.path.realpath(p)
        if not os.path.exists(rp) or rp in seen: continue
        seen.add(rp)
        print('=== ' + rp)
        txt = open(rp, encoding='latin-1').read().splitlines()
        for i, l in enumerate(txt, 1):
            if re.search(r'mysql|mysqli|PDO|connect|include|require|hostname|username|password|dbname|\$db\b|_user|_pass', l, re.I):
                print('  %4d: %s' % (i, mask(l)[:170]))
        incs = re.findall(r"""(?:include|require)(?:_once)?\s*\(?\s*['"]([^'"]+)['"]""", '\n'.join(txt))
        for inc in incs:
            ip = inc if inc.startswith('/') else os.path.join(os.path.dirname(rp), inc)
            if os.path.exists(ip) and ip not in seen:
                seen.add(ip)
                print('  --- incluye ' + ip)
                for j, l in enumerate(open(ip, encoding='latin-1').read().splitlines(), 1):
                    if re.search(r'mysql|connect|host|user|pass|dbname|define', l, re.I):
                        print('    %4d: %s' % (j, mask(l)[:170]))
print('Clave de u11 en los formularios viejos: #c954fe')
print('LISTO (solo lectura, claves ocultas)')
