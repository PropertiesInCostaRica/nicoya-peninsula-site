# Solo mira (no cambia nada): como funciona cdn.propertiesincostarica.com
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
print('--- DNS de cdn ---'); print(sh('getent hosts cdn.propertiesincostarica.com; host cdn.propertiesincostarica.com 2>/dev/null | head -5'))
print('--- respuesta de cdn para una pagina ---'); print(sh("curl -sI https://cdn.propertiesincostarica.com/beach.html | grep -i -E '^HTTP|server|via|x-cache|x-amz|cf-|age:|location' | head -12"))
print('--- apache: cdn en la configuracion ---'); print(sh("grep -rn -i 'cdn.propertiesincostarica' /etc/apache2/sites-enabled/ 2>/dev/null | head -10"))
print('--- apache: como llega el CDN al servidor (ultimas visitas con host cdn) ---'); print(sh("grep -h -i 'cdn.propertiesincostarica' /var/log/apache2/other_vhosts_access.log 2>/dev/null | tail -3 | cut -c1-250"))
print('--- .htaccess: reglas que miran el host ---'); print(sh("grep -n -i 'HTTP_HOST\\|cdn' /var/www/propertiesincostarica.com/web/.htaccess | head -10"))
print('LISTO')
