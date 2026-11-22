#!/usr/bin/env python3
# READ ONLY: are these old forms still used? Where does mysql.priv point? Does db11 live here?
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8', 'replace').strip()
print('1. A donde apunta mysql.priv:  ' + (sh("getent hosts mysql.priv mysql2.priv") or 'no existe (no apunta a ningun servidor)'))
print('2. La base db11 esta en este servidor: ' + ('SI' if sh("mysql -N -e \"SHOW DATABASES LIKE 'db11'\"") == 'db11' else 'NO'))
print('   Leads guardados en db11 en los ultimos 30 dias (tablas con fecha):')
print(sh("mysql -N -e \"SELECT table_name, update_time FROM information_schema.tables WHERE table_schema='db11' ORDER BY update_time DESC LIMIT 5\""))
print('3. PHP tiene mysql/mysqli: ' + sh("php -m | grep -iE '^mysql' | tr '\\n' ' '"))
print('4. Visitas a los formularios viejos (cgi) en los logs del sitio:')
print(sh("zcat -f /var/log/apache2/*access.log* /var/www/clients/client1/web50/log/*access* 2>/dev/null | grep -E '/properties/forms/cgi/[a-z_]+\\.php' | grep -oE '\\[[0-9]+/[A-Za-z]+/[0-9]+|/properties/forms/cgi/[a-z_]+\\.php|\" [0-9]{3} ' | paste - - - | awk '{print $2, $3}' | sort | uniq -c | sort -rn | head -12") or '   ninguna visita en los logs')
print('5. Ultima visita a esos formularios:')
print(sh("zcat -f /var/log/apache2/*access.log* /var/www/clients/client1/web50/log/*access* 2>/dev/null | grep -E '/properties/forms/cgi/[a-z_]+\\.php' | tail -3 | cut -c1-200") or '   ninguna')
print('6. Que usan los formularios actuales del sitio (donde se envian):')
print(sh("grep -rhoE 'action=\"[^\"]+\"' /var/www/clients/client1/web50/web/contact.html /var/www/clients/client1/web50/web/properties/puntarenas/for_sale/whale-bay-villa.html 2>/dev/null | sort | uniq -c"))
print('LISTO (solo lectura)')
