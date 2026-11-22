#!/usr/bin/env python3
# READ ONLY: for each PCR form file, show the database server and a short fingerprint of the password
# (never the password itself), and test whether each combination can connect.
import glob, re, hashlib, subprocess
D = '/var/www/clients/client1/web50/web/properties/forms/cgi/'
A = re.compile(r'^\s*\$(hostname|database|username|password)_(\w+)\s*=\s*(["\'])(.*?)\3\s*;')
combos = {}
for f in sorted(glob.glob(D + '*.php')):
    s = open(f, encoding='latin-1').read()
    if not re.search(r'u11|db11', s): continue
    d = {}
    for l in s.splitlines()[:40]:
        m = A.match(l)
        if m: d[m.group(1)] = m.group(4)
    fp = hashlib.sha256(d.get('password', '').encode()).hexdigest()[:6] if 'password' in d else '-'
    key = (d.get('hostname', '-'), d.get('username', '-'), fp, d.get('database', '-'))
    combos.setdefault(key, {'files': [], 'pw': d.get('password')})['files'].append(f.split('/')[-1])
print('Combinaciones distintas: %d' % len(combos))
for (h, u, fp, db), v in combos.items():
    ok = 'no probada'
    if v['pw'] is not None:
        r = subprocess.run(['php', '-r', '$c=function_exists("mysql_connect")?@mysql_connect($argv[1],$argv[2],$argv[3]):@mysqli_connect($argv[1],$argv[2],$argv[3]);echo $c?"CONECTA":"NO CONECTA";', h, u, v['pw']],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
        ok = r.stdout.decode('utf-8', 'replace').strip()[-12:]
    print('--- servidor: %s  usuario: %s  clave: #%s  base: %s  -> %s' % (h, u, fp, db, ok))
    print('    archivos (%d): %s' % (len(v['files']), ', '.join(v['files'])))
print('LISTO (solo lectura, claves nunca mostradas)')
