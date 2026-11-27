# Solo mira (no cambia nada): como llega /a/search/ a la aplicacion
import re, subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
def mask(x): return re.sub(r'(?i)(pass(word)?|pwd|secret|key|token)(["\'\s:=>,]+)([^"\'\s,;)]+)', r'\1\3*****', x)
v = sh("ls /etc/apache2/sites-enabled/ | grep -i 'propertiesincostarica.com.vhost' | head -1")
print('vhost:', v)
print(mask(sh("grep -n -i -E 'DocumentRoot|ProxyPass|Alias|WSGI|/a/|/a ' /etc/apache2/sites-enabled/" + v + " 2>/dev/null | head -20")))
print('--- app.propertiesincostarica.com (web3) ---'); print(sh('ls /var/www/clients/client1/web3/web/ 2>&1 | head -25'))
print('--- que tipo de app es ---'); print(sh("ls /var/www/clients/client1/web3/web/ /var/www/clients/client1/web3/ 2>/dev/null | grep -i -E 'manage.py|artisan|composer|wp-config|index.php|app.py|package.json' | head"))
print('LISTO')
