#!/usr/bin/env python3
# READ ONLY (fast): find config files that use the leads database user u11 or database db11.
# Uses grep on settings files only. Prints file names and line numbers, never passwords.
import subprocess
cmd = ("grep -rIlE --include='*.php' --include='*.py' --include='*.ini' --include='*.cnf' "
       "--include='*.conf' --include='*.env' --include='*.inc' --include='*.json' --include='*.yml' "
       "--exclude-dir=Images --exclude-dir=images --exclude-dir=.git --exclude-dir=node_modules "
       "--exclude-dir=uploads --exclude-dir=cache "
       "-e \"['\\\"]u11['\\\"]\" -e \"['\\\"]db11['\\\"]\" -e 'user=u11' -e 'dbname=db11' "
       "/var/www /etc /root /home /opt /srv 2>/dev/null")
out = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, timeout=170).stdout.decode('utf-8', 'ignore').split()
print('Archivos que usan u11 o db11: %d' % len(out))
for f in sorted(set(out)):
    n = subprocess.run("grep -nE \"u11|db11\" '%s' | cut -d: -f1 | head -8 | tr '\\n' ' '" % f, shell=True, stdout=subprocess.PIPE).stdout.decode().strip()
    print('  %s  (lineas %s)' % (f, n))
print('LISTO (solo lectura, no se cambio nada y no se mostraron claves)')
