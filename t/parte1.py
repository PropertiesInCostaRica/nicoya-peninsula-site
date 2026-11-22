#!/usr/bin/env python3
# PART 1 (password does NOT change): move the leads DB connection settings of the forms
# into ONE private settings file outside the public web folder. Full backup first.
# If anything fails, everything is restored from the backup. Passwords are never printed.
import glob, re, os, shutil, subprocess, time, tarfile, sys
SITE = '/var/www/clients/client1/web50/'
D = SITE + 'web/properties/forms/cgi/'
PRIV = SITE + 'private/'
CONF = PRIV + 'pcr_leads_db.php'
ts = time.strftime('%Y%m%d-%H%M%S')
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8', 'replace')
def rd(p): return open(p, encoding='latin-1').read()
def wr(p, s): open(p, 'w', encoding='latin-1').write(s)

# 0. backup
bk = '/root/respaldos/forms-cgi-' + ts + '.tgz'
with tarfile.open(bk, 'w:gz') as t:
    t.add(D, arcname='cgi')
print('1. Respaldo completo de los formularios: ' + bk)
def restore(msg):
    print('ERROR: ' + msg)
    with tarfile.open(bk) as t:
        for m in t.getmembers():
            if m.isfile():
                m.name = m.name[len('cgi/'):]
                t.extract(m, D)
    if os.path.exists(CONF) and not os.path.exists(CONF + '.keep'):
        os.remove(CONF)
    print('Todo restaurado como estaba. No se cambio nada.')
    sys.exit(1)

if os.path.exists(CONF):
    print('Ya existe ' + CONF + ', no se hace nada.'); sys.exit(0)

# 1. read current values (must be identical in all standard files)
files = sorted(f for f in glob.glob(D + '*.php') if re.search(r'u11|db11', rd(f)))
A = re.compile(r'^(\s*\$(hostname|database|username|password)_(\w+)\s*=\s*)(["\'])(.*?)\4(\s*;.*)$')
vals = {}
for f in files:
    for l in rd(f).splitlines()[:40]:
        m = A.match(l)
        if m:
            vals.setdefault(m.group(2), set()).add(m.group(5))
uval = {k: v for k, v in vals.items()}
if 'u11' not in uval.get('username', set()):
    restore('no encontre el usuario u11')
# the u11 password = password used in files whose username is u11
pw = set(); host = set()
for f in files:
    s = rd(f).splitlines()[:40]
    d = {}
    for l in s:
        m = A.match(l)
        if m: d[m.group(2)] = m.group(5)
    if d.get('username') == 'u11':
        pw.add(d.get('password')); host.add(d.get('hostname'))
if len(pw) != 1 or len(host) != 1 or None in pw:
    restore('los archivos no tienen todos la misma clave o servidor de u11 (%d claves, %d servidores)' % (len(pw), len(host)))
PW = pw.pop(); HOST = host.pop()
print('2. Archivos con u11/db11: %d  (misma clave en todos: SI)' % len(files))

# 2. check that PHP of this site may read the private folder
ob = sh("grep -rh 'open_basedir' /etc/apache2/sites-enabled/ /etc/php*/ /etc/php/*/ 2>/dev/null | grep -i web50 | head -3")
if ob.strip() and 'private' not in ob:
    restore('la configuracion de PHP no deja leer la carpeta private')
print('3. PHP puede leer la carpeta private: SI')

# 3. write the private settings file
os.makedirs(PRIV, exist_ok=True)
conf = ("<?php\n// PCR leads database settings. Only place where this password lives.\n"
        "define('PCR_DB_HOST', '%s');\ndefine('PCR_DB_USER', 'u11');\ndefine('PCR_DB_PASS', '%s');\ndefine('PCR_DB_NAME', 'db11');\n"
        % (HOST.replace("'", "\\'"), PW.replace("'", "\\'")))
wr(CONF, conf)
st = os.stat(D)
os.chown(CONF, st.st_uid, st.st_gid); os.chmod(CONF, 0o640)
print('4. Archivo de configuracion unico creado: ' + CONF)

# 4. change the forms to use it
REQ = "require_once('" + CONF + "');"
changed = 0
for f in files:
    s = rd(f); orig = s
    out = []
    for l in s.split('\n'):
        m = A.match(l)
        if m:
            kind, val = m.group(2), m.group(5)
            if kind == 'password' and val == PW: l = m.group(1) + 'PCR_DB_PASS' + m.group(6)
            elif kind == 'hostname' and val == HOST: l = m.group(1) + 'PCR_DB_HOST' + m.group(6)
            elif kind == 'username' and val == 'u11': l = m.group(1) + 'PCR_DB_USER' + m.group(6)
            elif kind == 'database' and val == 'db11': l = m.group(1) + 'PCR_DB_NAME' + m.group(6)
        out.append(l)
    s = '\n'.join(out)
    if s != orig:
        s = re.sub(r'<\?php', '<?php ' + REQ, s, count=1)
        if REQ not in s:
            restore('no encontre <?php en ' + os.path.basename(f))
        wr(f, s); changed += 1
left = [os.path.basename(f) for f in files if PW in rd(f)]
print('5. Formularios actualizados: %d   Archivos que todavia tienen la clave escrita: %d %s' % (changed, len(left), ' '.join(left)))

# 5. syntax check every file
bad = [os.path.basename(f) for f in files if 'No syntax errors' not in sh("php -l '%s'" % f)]
if bad:
    restore('error de sintaxis en ' + ', '.join(bad))
print('6. Revision de errores en todos los archivos: OK')

# 6. connection test with the new settings file
t = sh("php -r \"require '%s'; \\$c = function_exists('mysql_connect') ? @mysql_connect(PCR_DB_HOST, PCR_DB_USER, PCR_DB_PASS) : @mysqli_connect(PCR_DB_HOST, PCR_DB_USER, PCR_DB_PASS, PCR_DB_NAME); echo \\$c ? 'CONEXION_OK' : 'CONEXION_FALLA';\"" % CONF)
if 'CONEXION_OK' not in t:
    restore('la prueba de conexion fallo')
print('7. Prueba de conexion a la base de leads con el archivo nuevo: OK')
sh('/usr/local/bin/pcr-git-respaldo.sh')
print('LISTO. La clave NO cambio todavia. Ahora vive en un solo archivo, fuera de la web.')
