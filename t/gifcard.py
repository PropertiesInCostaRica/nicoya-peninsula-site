# Rehace la foto animada (p.gif) de la tarjeta de una propiedad con fotos elegidas.
# Uso: python3 gifcard.py <carpeta-de-imagenes> <subcarpeta> <fotos separadas por coma>
# Ej:  python3 gifcard.py turn-key-ocean-view-estate new 3,1,2,4,11,12,16,7
import os, sys, time, shutil
from PIL import Image
W = '/var/www/propertiesincostarica.com/web/properties/Images/'
folder, sub, nums = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
D = W + folder + '/'
out = D + 'p.gif'
size = (400, 354)
if os.path.exists(out):
    try: size = Image.open(out).size
    except Exception: pass
    os.makedirs('/root/respaldos', exist_ok=True)
    shutil.copy2(out, '/root/respaldos/' + folder + '-p.gif.' + time.strftime('%Y%m%d%H%M'))
frames = []
for n in nums:
    p = D + sub + '/' + n.strip() + '.jpg'
    if not os.path.exists(p): print('No existe ' + p); continue
    im = Image.open(p).convert('RGB')
    r = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
    x = (im.width - size[0]) // 2; y = (im.height - size[1]) // 2
    im = im.crop((x, y, x + size[0], y + size[1]))
    frames.append(im.convert('P', palette=Image.ADAPTIVE, colors=256))
if not frames: raise SystemExit('No hay fotos')
frames[0].save(out, save_all=True, append_images=frames[1:], duration=2500, loop=0, optimize=False)
print('Foto animada nueva: %d fotos, %dx%d, %d KB' % (len(frames), size[0], size[1], os.path.getsize(out) // 1024))
print('https://cdn.propertiesincostarica.com/properties/Images/' + folder + '/p.gif')
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO')
