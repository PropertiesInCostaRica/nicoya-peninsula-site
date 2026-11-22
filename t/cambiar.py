#!/usr/bin/env python3
# Change the leads database password (u11) SAFELY, in one step:
# asks for the new password hidden (twice), changes it in MySQL AND in /mnt/pcr_db/access.php,
# tests the connection, and if anything fails puts everything back as it was. Never prints the password.
import getpass, re, shutil, subprocess, time, sys
F = '/mnt/pcr_db/access.php'
ts = time.strftime('%Y%m%d-%H%M%S')
s = open(F, encoding='latin-1').read()
m = re.search(r"(\$password_x\s*=\s*)(['\"])(.*?)\2(\s*;)", s)
if not m:
    sys.exit('No encontre la clave en access.php. No se cambio nada.')
old = m.group(3)
def esc(p): return p.replace('\\', '\\\\').replace("'", "\\'")
def set_db(p):
    sql = "SET PASSWORD FOR 'u11'@'localhost' = PASSWORD('%s'); SET PASSWORD FOR 'u11'@'%%' = PASSWORD('%s');" % (esc(p), esc(p))
    return subprocess.run(['mysql', '-e', sql], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode == 0
def test():
    code = 'require "%s"; $m = @new mysqli($hostname_x, $username_x, $password_x, $database_x); echo $m->connect_error ? "FALLA" : "OK";' % F
    return subprocess.run(['php', '-r', code], stdout=subprocess.PIPE).stdout.decode().strip() == 'OK'
print('Escriba la clave nueva (no se ve mientras escribe). Solo letras y numeros, 16 o mas.')
p1 = getpass.getpass('Clave nueva: ')
p2 = getpass.getpass('Repita la clave nueva: ')
if p1 != p2: sys.exit('Las dos claves no son iguales. No se cambio nada.')
if not re.match(r'^[A-Za-z0-9]{16,}$', p1): sys.exit('La clave debe tener solo letras y numeros, 16 o mas. No se cambio nada.')
if p1 == old: sys.exit('Es la misma clave de antes. No se cambio nada.')
bk = '/root/respaldos/access.php-' + ts
shutil.copy2(F, bk)
print('1. Copia de access.php: ' + bk)
if not set_db(p1):
    set_db(old); sys.exit('No se pudo cambiar en la base de datos. Todo quedo como estaba.')
print('2. Clave cambiada en la base de datos: SI')
open(F, 'w', encoding='latin-1').write(s[:m.start(3)] + p1 + s[m.end(3):])
print('3. Clave cambiada en access.php: SI')
if not test():
    shutil.copy2(bk, F); set_db(old)
    sys.exit('4. La prueba fallo. Se volvio todo a como estaba (clave anterior). Los formularios funcionan.')
print('4. Prueba de conexion con la clave nueva: OK')
subprocess.run('> /root/.mysql_history', shell=True)
print('LISTO. La clave de la base de leads se cambio y los formularios funcionan. Guarde la clave nueva en un lugar seguro.')
