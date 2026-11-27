# Redirige una pagina vieja a otra. Uso: python3 redir.py <pagina-vieja> <url-nueva>
import os, sys, time, shutil
W = '/var/www/propertiesincostarica.com/web/'
p = sys.argv[1].replace('https://www.propertiesincostarica.com/', ''); to = sys.argv[2]
f = W + p
if not os.path.exists(f): raise SystemExit('No existe: ' + p)
os.makedirs('/root/respaldos/redir', exist_ok=True)
shutil.copy2(f, '/root/respaldos/redir/' + p.replace('/', '_') + '.' + time.strftime('%Y%m%d%H%M'))
open(f, 'w', encoding='utf-8').write('<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Moved</title>\n'
  '<meta http-equiv="refresh" content="0; url=' + to + '">\n<link rel="canonical" href="' + to + '">\n'
  '<meta name="robots" content="noindex, follow">\n<script>location.replace("' + to + '")</script>\n'
  '</head><body><p>This page moved to <a href="' + to + '">' + to + '</a></p></body></html>\n')
print('Redirigida: https://www.propertiesincostarica.com/' + p + '  ->  ' + to)
print('LISTO')
