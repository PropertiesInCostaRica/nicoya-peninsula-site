# Limpieza de logs del servidor
#   python3 logclean.py            -> solo muestra (no cambia nada)
#   python3 logclean.py --aplicar  -> comprime y borra lo indicado
# 1) Comprime (gzip) los logs diarios de visitas con mas de 2 dias (no se pierde nada, ocupan ~10%)
# 2) Borra logs viejos ya comprimidos o rotados con mas de 60 dias
import os, re, sys, time, glob, gzip, shutil, subprocess
AP = '--aplicar' in sys.argv
now = time.time(); D = 86400
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
print('Disco antes: ' + sh('df -h / | tail -1'))
comp, old = [], []
for root, dirs, files in os.walk('/var/log'):
    for fn in files:
        f = os.path.join(root, fn)
        try: st = os.stat(f)
        except Exception: continue
        age = (now - st.st_mtime) / D
        if re.match(r'^\d{8}-(access|error)\.log$', fn) and age > 2: comp.append((f, st.st_size))
        elif (fn.endswith('.gz') or re.search(r'\.\d+(\.log)?$', fn)) and age > 60: old.append((f, st.st_size))
mb = lambda l: sum(s for _, s in l) / 1048576.0
print('1) Comprimir %d logs diarios de mas de 2 dias: %.0f MB (quedarian en unos %.0f MB)' % (len(comp), mb(comp), mb(comp) * 0.1))
print('2) Borrar %d logs viejos de mas de 60 dias: %.0f MB' % (len(old), mb(old)))
for f, s in sorted(old, key=lambda x: -x[1])[:5]: print('   ejemplo: %s (%.1f MB)' % (f, s / 1048576.0))
M = '/var/mail/root'
VM = '--vaciar-correo' in sys.argv
if os.path.exists(M):
    print('3) Correo automatico de root: %.0f MB. Asuntos mas repetidos:' % (os.path.getsize(M) / 1048576.0))
    print(sh("grep '^Subject:' " + M + " | sort | uniq -c | sort -rn | head -5"))
    if VM:
        sh('tail -c 2000000 ' + M + ' > /root/respaldos/correo-root-ultimos.txt')
        open(M, 'w').close()
        print('   Correo de root vaciado (lo ultimo quedo en /root/respaldos/correo-root-ultimos.txt)')
    else:
        print('   (para vaciarlo: python3 /root/logclean.py --aplicar --vaciar-correo)')
if AP:
    for f, s in comp:
        try:
            with open(f, 'rb') as a, gzip.open(f + '.gz', 'wb') as b: shutil.copyfileobj(a, b)
            shutil.copystat(f, f + '.gz'); os.remove(f)
        except Exception as e: print('no pude comprimir ' + f + ': ' + str(e))
    for f, s in old:
        try: os.remove(f)
        except Exception as e: print('no pude borrar ' + f + ': ' + str(e))
    sh('journalctl --vacuum-time=30d')
    print('Disco despues: ' + sh('df -h / | tail -1'))
    print('LISTO')
else:
    print('LISTO (solo vista previa, no se cambio nada)')
