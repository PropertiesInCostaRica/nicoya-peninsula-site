#!/usr/bin/env python3
# READ ONLY test: can the website connect to the leads database with the password in access.php?
# Never shows the password.
import subprocess
code = ('require "/mnt/pcr_db/access.php"; $m = @new mysqli($hostname_x, $username_x, $password_x, $database_x);'
        'if ($m->connect_error) { echo "FALLA: " . $m->connect_error; } else { $r = $m->query("SELECT COUNT(*) FROM mails"); '
        'echo "CONEXION OK. Leads guardados en mails: " . $r->fetch_row()[0]; }')
r = subprocess.run(['php', '-r', code], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(r.stdout.decode('utf-8', 'replace').replace('using password: YES', 'clave no coincide'))
