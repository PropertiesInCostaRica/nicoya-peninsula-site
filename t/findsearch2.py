# Solo mira (no cambia nada): segunda busqueda del buscador /a/search/
import re, subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
def mask(x): return re.sub(r'(?i)(pass(word)?|pwd|secret|key|token)(["\'\s:=>,]+)([^"\'\s,;)]+)', r'\1\3*****', x)
print('--- apache: reglas para /a ---'); print(mask(sh("grep -rn -i -E 'WSGI|ProxyPass|ScriptAlias|Alias +/a|RewriteRule +\\^/?a/|<Location +/a' /etc/apache2/ 2>/dev/null | head -20")))
print('--- carpetas en /var/www ---'); print(sh('ls -la /var/www/ 2>&1 | head -20'))
print('--- donde esta la app (archivos con \"Search App\") ---'); print(sh("grep -rl --include=*.py --include=*.php --include=*.js --include=*.html 'Search+App\\|Search App' /var/www /home /opt /srv 2>/dev/null | grep -v '/web/properties/' | head -15"))
print('--- programas corriendo (python, node, php, gunicorn) ---'); print(sh("ps aux | grep -E 'python|node|gunicorn|uwsgi|php-fpm|mysqld|mariadb|postgres' | grep -v grep | awk '{print $1, $11, $12, $13}' | sort -u | head -15"))
print('LISTO')
