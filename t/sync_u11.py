#!/usr/bin/env python3
# Makes the database password of u11 EQUAL to the password Mirtha wrote in /mnt/pcr_db/access.php,
# for u11@localhost and u11@%, then tests the connection. Never prints the password.
import re, subprocess
s = open('/mnt/pcr_db/access.php', encoding='latin-1').read()
m = re.search(r"\$password_x\s*=\s*(['\"])(.*?)\1\s*;", s)
if not m or not m.group(2):
    raise SystemExit('No encontre la clave en access.php, no se cambio nada')
pw = m.group(2)
if not re.match(r'^[A-Za-z0-9]{12,}$', pw):
    raise SystemExit('La clave de access.php debe tener solo letras y numeros (12 o mas). Revisela con nano. No se cambio nada.')
sql = ("SET PASSWORD FOR 'u11'@'localhost' = PASSWORD('%s'); SET PASSWORD FOR 'u11'@'%%' = PASSWORD('%s');" % (pw, pw))
r = subprocess.run(['mysql', '-e', sql], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print('Base de datos actualizada con la clave de access.php: ' + ('SI' if r.returncode == 0 else 'NO ' + r.stdout.decode()[:200].replace(pw, 'xxxx')))
code = ('require "/mnt/pcr_db/access.php"; $m = @new mysqli($hostname_x, $username_x, $password_x, $database_x);'
        'echo $m->connect_error ? "FALLA" : "CONEXION OK";')
print('Prueba: ' + subprocess.run(['php', '-r', code], stdout=subprocess.PIPE).stdout.decode())
subprocess.run('> /root/.mysql_history', shell=True)
print('Historial de MySQL borrado. LISTO')
