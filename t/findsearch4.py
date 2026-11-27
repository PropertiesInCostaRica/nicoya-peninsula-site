# Solo mira (no cambia nada): como crear un usuario para el panel /a/admin/
import re, subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
def mask(x): return re.sub(r'(?i)(pass(word)?|pwd|secret|key|token)(["\'\s:=>,]+)([^"\'\s,;)]+)', r'\1\3*****', x)
D = '/home/dapps/pcrappsearch'
print('--- carpeta ---'); print(sh('ls ' + D + ' | head -30'))
print('--- wsgi.py ---'); print(mask(sh('grep -v "^#" ' + D + '/wsgi.py | head -25')))
print('--- python del sitio ---'); print(sh("grep -n -i 'python-home\\|python-path' /etc/apache2/sites-enabled/*app.propertiesincostarica* /etc/apache2/sites-enabled/*propertiesincostarica.com* 2>/dev/null | head -5"))
print('--- manage.py ---'); print(sh('find /home/dapps -maxdepth 3 -name manage.py 2>/dev/null | head -3'))
print('--- usuarios del panel (solo nombres) ---')
m = sh('find /home/dapps -maxdepth 3 -name manage.py 2>/dev/null | head -1')
if m:
    d = m.rsplit('/', 1)[0]
    py = sh("grep -o 'python-home=[^ ]*' /etc/apache2/sites-enabled/* 2>/dev/null | head -1 | cut -d= -f2")
    exe = (py + '/bin/python') if py else 'python3'
    print('python:', exe)
    print(sh('cd ' + d + ' && echo "from django.contrib.auth import get_user_model as g; U=g(); print([(u.username, u.is_superuser, u.is_active) for u in U.objects.all()])" | ' + exe + ' manage.py shell 2>&1 | tail -3'))
print('LISTO')
