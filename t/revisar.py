#!/usr/bin/env python3
# READ ONLY security check: logins, SSH attempts, database access attempts. Changes nothing.
import subprocess, re, glob, collections, os
def sh(c):
    try: return subprocess.check_output(c, shell=True, stderr=subprocess.STDOUT).decode('utf-8', 'replace')
    except subprocess.CalledProcessError as e: return e.output.decode('utf-8', 'replace')
print('=== 1. Ultimas entradas al servidor (SSH) ===')
print(sh("last -n 15 -a | head -20"))
print('=== 2. Intentos fallidos de SSH (ultimos logs) ===')
txt = sh("zcat -f /var/log/auth.log* 2>/dev/null | grep -E 'Failed password|Invalid user' | tail -n 20000")
ips = collections.Counter(re.findall(r'from (\d+\.\d+\.\d+\.\d+)', txt))
print('Total intentos fallidos: %d' % sum(ips.values()))
for ip, n in ips.most_common(5): print('  %s  %d' % (ip, n))
ok = sh("zcat -f /var/log/auth.log* 2>/dev/null | grep 'Accepted' | tail -n 10")
print('Entradas aceptadas recientes:\n' + (ok or '  ninguna en el log'))
print('=== 3. Base de datos: quien puede conectarse ===')
print(sh("ss -ltnp 2>/dev/null | grep -E ':3306|:5432' || netstat -ltnp 2>/dev/null | grep -E ':3306|:5432' || echo 'no hay base de datos escuchando en este servidor'"))
print('=== 4. Base de datos: intentos de acceso negados ===')
n = 0; last = []
for f in glob.glob('/var/log/mysql/error.log*') + glob.glob('/var/log/postgresql/*.log*'):
    t = sh("zcat -f '%s'" % f)
    m = [l for l in t.splitlines() if re.search(r'Access denied|authentication failed|password authentication failed', l)]
    n += len(m); last += m[-5:]
print('Intentos negados: %d' % n)
for l in last[-5:]: print('  ' + l[:200])
print('=== 5. Web: intentos de entrar a paneles de base de datos ===')
t = sh("zcat -f /var/log/apache2/*access.log* 2>/dev/null | grep -iE 'phpmyadmin|adminer|pma/|/mysql|\\.env|db\\.sql|backup\\.sql' | tail -n 5000")
lines = t.strip().splitlines() if t.strip() else []
ok200 = [l for l in lines if re.search(r'" 200 ', l)]
print('Intentos: %d   Respuestas exitosas (200): %d' % (len(lines), len(ok200)))
for l in ok200[-5:]: print('  ' + l[:200])
print('LISTO (no se cambio nada)')
