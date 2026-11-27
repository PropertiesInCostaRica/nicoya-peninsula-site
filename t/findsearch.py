# Solo mira (no cambia nada): de donde saca los datos el buscador /a/search/
import os, re, subprocess
W = '/var/www/propertiesincostarica.com/web/'
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
def mask(x): return re.sub(r'(?i)(pass(word)?|pwd|secret|key|token)(["\'\s:=>,]+)([^"\'\s,;)]+)', r'\1\3*****', x)
print('--- carpeta /a/ ---'); print(sh('ls -la ' + W + 'a/ 2>&1 | head -30'))
print('--- .htaccess sobre /a/ ---'); print(mask(sh("grep -n -i '^[^#]*\\(/a/\\|\\^a/\\|search\\)' " + W + ".htaccess | head -15")))
print('--- apache: proxy o alias para /a ---'); print(mask(sh("grep -rn -i 'alias\\|proxypass\\|/a/' /etc/apache2/sites-enabled/ 2>/dev/null | head -15")))
print('--- conexiones a base de datos en /a/ (contrasenas ocultas) ---')
print(mask(sh("grep -rn -i -E 'mysqli|new PDO|mysql_connect|DB_HOST|DB_NAME|dbname|host *=|api_url|https?://[a-z0-9.-]+/(api|listing)' " + W + "a/ 2>/dev/null | grep -v '\\.css\\|\\.min\\.js' | head -25")))
print('--- archivos de datos que mencionan 4233 ---'); print(sh("grep -rl '4233' " + W + "a/ 2>/dev/null | head; find / -xdev \\( -name '*.json' -o -name '*.csv' -o -name '*.sqlite*' -o -name '*.db' \\) -newer " + W + "index.html 2>/dev/null | grep -v -E '/proc/|/usr/|/snap/|node_modules' | head -10"))
print('--- servicios de base de datos en este servidor ---'); print(sh("ps aux | grep -i -E 'mysql|mariadb|postgres|mongo' | grep -v grep | awk '{print $11}' | sort -u"))
print('LISTO')
