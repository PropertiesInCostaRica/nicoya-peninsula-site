# Solo busca (no cambia nada): donde quedo la pagina de la propiedad 4128
import os, subprocess
W = '/var/www/propertiesincostarica.com/web/'
P = 'properties/Montezuma/for_sale/magical-sanctuary.html'
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
print('Existe en la web:', os.path.exists(W + P), sh('ls -la ' + W + P + ' 2>&1'))
print('--- .htaccess:'); print(sh("grep -rn -i 'magical-sanctuary\\|4128' " + W + ".htaccess /etc/apache2/sites-enabled/ /etc/nginx/sites-enabled/ 2>/dev/null | head"))
print('--- archivos con ese nombre:'); print(sh("find / -xdev -iname '*magical-sanctuary*' 2>/dev/null | head -20"))
print('--- fotos:'); print(sh("ls -d " + W + "properties/Images/magical-sanctuary* 2>&1 | head"))
print('--- script de respaldo git:'); print(sh('cat /root/pcr-git-respaldo.sh 2>/dev/null | head -20'))
for d in ('/root/respaldos/web-git', W):
    if os.path.isdir(d + '/.git') or os.path.isdir(d + '.git'):
        print('--- git log en', d); print(sh('cd ' + d + ' && git log --oneline -5 -- ' + P + ' 2>&1'))
print('--- paginas que mencionan 4128:'); print(sh("grep -rl 'ID CODE: #4128\\|ID CODE #4128' " + W + " --include=*.htm* 2>/dev/null | head"))
print('LISTO')
