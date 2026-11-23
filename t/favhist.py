#!/usr/bin/env python3
# READ ONLY: history of the favicon, and every old favicon still on the server.
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8', 'replace').strip()
W = '/var/www/propertiesincostarica.com/web'
print('1. Favicon actual: ' + sh("ls -la --time-style=long-iso %s/favicon.png; file %s/favicon.png" % (W, W)))
print('\n2. Historial de cambios del favicon (respaldo git del servidor):')
print(sh("cd %s && git log --date=short --format='%%h %%ad %%an: %%s' -- favicon.png favicon.ico 2>&1 | head -15" % W) or '   sin historial')
print('\n3. Otros archivos favicon en el servidor:')
print(sh("find /var/www /mnt/www /root/respaldos -maxdepth 6 -iname '*favicon*' -not -path '*/node_modules/*' -printf '%TY-%Tm-%Td  %8s  %p\\n' 2>/dev/null | sort -r | head -30"))
print('\nLISTO (solo lectura)')
