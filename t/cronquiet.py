# Que las tareas automaticas (awstats y mysql restart) dejen de mandar correos a root.
#   python3 cronquiet.py            -> solo muestra
#   python3 cronquiet.py --aplicar  -> aplica (guarda respaldo)
import os, sys, time, shutil, subprocess
AP = '--aplicar' in sys.argv
def sh(c, inp=None): return subprocess.run(c, shell=True, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout
os.makedirs('/root/respaldos', exist_ok=True); st = time.strftime('%Y%m%d%H%M')
# 1) awstats: archivo /etc/cron.d/awstats
f = '/etc/cron.d/awstats'
if os.path.exists(f):
    t = open(f).read()
    print('--- ' + f + ' ---\n' + t.strip())
    if 'MAILTO=""' in t: print('awstats ya esta en silencio')
    elif AP:
        shutil.copy2(f, '/root/respaldos/cron.d_awstats.' + st)
        open(f, 'w').write('MAILTO=""\n' + t); print('awstats: listo, ya no manda correos')
    else: print('PLAN: agregar MAILTO="" al inicio (solo silencia este archivo)')
else: print('No existe ' + f)
# 2) mysql restart en el crontab de root
ct = sh('crontab -l 2>/dev/null')
lines = ct.split('\n'); ch = False
for i, l in enumerate(lines):
    if 'mysql restart' in l and not l.lstrip().startswith('#') and '/dev/null' not in l:
        print('crontab root: ' + l.strip()); lines[i] = l.rstrip() + ' >/dev/null 2>&1'; ch = True
if ch:
    if AP:
        open('/root/respaldos/crontab-root.' + st, 'w').write(ct)
        sh('crontab -', '\n'.join(lines)); print('mysql restart: listo, sigue igual pero ya no manda correos')
    else: print('PLAN: agregar >/dev/null 2>&1 a esa linea (la tarea sigue igual, solo sin correo)')
print('LISTO' + ('' if AP else ' (solo vista previa, no se cambio nada)'))
