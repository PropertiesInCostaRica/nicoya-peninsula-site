# Solo mira (no cambia nada): como pide paginas KeyCDN al servidor
import subprocess
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
L = "$(ls -t /var/log/ispconfig/httpd/propertiesincostarica.com/*-access.log 2>/dev/null | head -1)"
print('log: ' + sh('echo ' + L))
print('--- pedidos de KeyCDN (ultimos 5) ---'); print(sh("grep -i 'keycdn' " + L + " | tail -5 | cut -c1-300"))
print('--- cuantos pedidos de paginas .html hizo KeyCDN hoy ---'); print(sh("grep -i 'keycdn' " + L + " | grep -c '\\.html'"))
print('--- prueba: el servidor ve el encabezado X-Pull? ---'); print(sh("curl -sI -H 'X-Pull: KeyCDN' https://www.propertiesincostarica.com/beach.html | head -1"))
print('LISTO')
