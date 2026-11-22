#!/usr/bin/env python3
# Preparation for the password change (the password is NOT changed here):
# 1) backup of /mnt/pcr_db/access.php  2) move the test file prueba.php (has the password inside)
# out of the public website into the backups folder  3) show the MySQL version.
import shutil, time, os, subprocess
ts = time.strftime('%Y%m%d-%H%M%S')
os.makedirs('/root/respaldos', exist_ok=True)
shutil.copy2('/mnt/pcr_db/access.php', '/root/respaldos/access.php-' + ts)
print('1. Copia de access.php: /root/respaldos/access.php-' + ts)
t = '/mnt/www/clients/client1/web1/web/properties/forms/cgi/prueba.php'
if os.path.exists(t):
    shutil.move(t, '/root/respaldos/prueba.php-' + ts)
    print('2. prueba.php (archivo de prueba con la clave adentro) sacado de la web y guardado en /root/respaldos/prueba.php-' + ts)
else:
    print('2. prueba.php ya no estaba en la web')
print('3. Version de MySQL: ' + subprocess.run('mysql -V', shell=True, stdout=subprocess.PIPE).stdout.decode().strip())
print('LISTO (la clave NO se cambio)')
