# Buscador: agregar #4250 (Paquera) y #4251 (Cahuita) a la base del buscador
#   python3 dbnew.py            -> solo muestra lo que haria
#   python3 dbnew.py --aplicar  -> las agrega (guarda respaldo)
import sys, os, re, json, subprocess, time
W = '/var/www/propertiesincostarica.com/web/'
AP = '--aplicar' in sys.argv
NEW = [
 (4251, 'properties/caribe/for-sale/cahuita-lots.html', 'cahuita-lots', 1000, ['Cahuita', 'Caribbean', 'Caribe', 'Limon'], ['Land and Lots', 'Beach Properties', 'Invest']),
 (4250, 'properties/paquera/for-sale/paquera-lot.html', 'paquera-lot', 8444, ['Tambor and Paquera', 'Southern Nicoya Peninsula', 'Nicoya'], ['Land and Lots', 'Southern Nicoya Peninsula']),
]
def sh(c): return subprocess.run(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout.strip()
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
v = lambda x: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', (x or '').replace('&nbsp;', ' ').replace('&amp;', '&'))).strip()
def num(s):
    try: return float(s.replace(',', ''))
    except Exception: return None
items = []
for code, rel, slug, LAND, AREAS, SECS in NEW:
    if not os.path.exists(W + rel): print('Saltada #%d: la pagina no existe todavia (%s)' % (code, rel)); continue
    t = rd(W + rel)
    R = {m.group(1): m.group(2) for m in re.finditer(r'<!-- InstanceBeginEditable name="([^"]+)" -->(.*?)<!-- InstanceEndEditable -->', t, re.S)}
    title = v(R.get('title'))
    pr = v(re.sub(r'<s>.*?</s>', ' ', R.get('price', ''), flags=re.S))
    am = re.findall(r'US\$\s*([\d,]+)', pr); price = int(num(am[-1])) if am else None
    f = v(R.get('features'))
    m2 = re.search(r'Land[^:]*:\s*([\d,\.]+)\s*m', f, re.I); ac = re.search(r'([\d\.]+)\s*acre', f, re.I)
    cm = re.search(r'Construction[^:]*:\s*([\d,\.]+)\s*m', f, re.I)
    bd = re.search(r'Bedrooms?:?\s*(\d+)|(\d+)\s*Bed', f, re.I); ba = re.search(r'Bathrooms?:?\s*([\d\.]+)|([\d\.]+)\s*Bath', f, re.I)
    paras = [v(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', R.get('content', ''), re.S)]
    op = next((p for p in paras if len(p) > 80 and 'Click on the pictures' not in p), '')
    land = float(LAND); cons = num(cm.group(1)) if cm else None
    low = (title + ' ' + f + ' ' + op).lower()
    items.append(dict(id_code=code, title=title, url=rel, full_url='https://www.propertiesincostarica.com/' + rel,
        primary_picture='https://cdn.propertiesincostarica.com/properties/Images/' + slug + '/p.jpg',
        sales_price=price, land_size_meters=land, land_size_feets=round(land * 10.7639, 1) if land else None,
        land_size_hectares=round(land / 10000.0, 3) if land else None,
        land_size_acres=num(ac.group(1)) if ac else (round(land / 4046.86, 3) if land else None),
        construction_meters=cons, construction_feets=round(cons * 10.7639, 1) if cons else None,
        bedrooms=int((bd.group(1) or bd.group(2))) if bd else None, bathrooms=num(ba.group(1) or ba.group(2)) if ba else None,
        header=title[:220], opening_paragraph=op[:1000], meta_title=title[:200], meta_description=op[:160],
        areas=AREAS, secs=SECS))
code = r'''import json, datetime
from django.db import connection
c = connection.cursor()
AP = %s
IT = json.loads(%r)
def q(s, a=None):
    c.execute(s, a or []); return c.fetchall()

tabs = [r[0] for r in q("SHOW TABLES")]
st = [t for t in tabs if t.startswith("listing_section") and t not in ("listing_section_listing", "listing_section_type")][0]
cl = [r[0] for r in q("SHOW COLUMNS FROM " + st)]
nm = "name" if "name" in cl else cl[1]
secs = dict((r[1].strip(), r[0]) for r in q("SELECT id, %%s FROM %%s" %% (nm, st)))
def sid(pat):
    for k, i in secs.items():
        if pat.lower() == k.lower(): return i
    for k, i in sorted(secs.items(), key=lambda x: len(x[0])):
        if pat.lower() in k.lower(): return i

LC = [r[0] for r in q("SHOW COLUMNS FROM listing_listing")]
now = datetime.datetime.utcnow().strftime("%%Y-%%m-%%d %%H:%%M:%%S")
for it in IT:
    if q("SELECT id FROM listing_listing WHERE id_code=%%s", [it["id_code"]]):
        print("@@#%%s ya esta en el buscador, no se toca" %% it["id_code"]); continue
    a = next((sid(p) for p in it["areas"] if sid(p)), None)
    tpl = q("SELECT l.id FROM listing_listing l JOIN listing_section_listing s ON s.listing_id=l.id WHERE s.section_id=%%s AND l.status_id=1 ORDER BY l.id DESC LIMIT 1", [a]) if a else ()
    if not tpl:
        print("@@#%%s: no encontre plantilla para %%s, saltada" %% (it["id_code"], it["areas"])); continue
    T = tpl[0][0]
    row = dict(zip(LC, q("SELECT * FROM listing_listing WHERE id=%%s", [T])[0]))
    for k in ("title","url","full_url","primary_picture","sales_price","land_size_meters","land_size_feets","land_size_hectares","land_size_acres","construction_meters","construction_feets","bedrooms","bathrooms","header","opening_paragraph","meta_title","meta_description","id_code"):
        if k in row: row[k] = it[k]
    for k, val in (("full_description",""),("meta_keywords",""),("rental_price",None),("maids_quarters",None),("parking",None),("status_id",1),("exclusive",0),("position",None),("agreement_end",None),("date_created",now),("date_last_mod",now)):
        if k in row: row[k] = val
    del row["id"]
    want = [a] + [sid(x) for x in it["secs"]]
    want = [w for i, w in enumerate(want) if w and w not in want[:i]]
    tc = q("SELECT property_condition_id FROM listing_listing_property_status WHERE listing_id=%%s", [T])
    print("@@#%%s %%s | US$%%s | %%s m2 | %%s hab %%s banos | zona %%s (copia ubicacion de registro %%s) | secciones %%s | For Sale %%s" %% (it["id_code"], it["title"][:45], it["sales_price"], it["land_size_meters"], it["bedrooms"], it["bathrooms"], [k for k, i in secs.items() if i == a][0], T, ", ".join("%%s %%s" %% (w, [k for k, i in secs.items() if i == w][0]) for w in want), [x[0] for x in tc]))
    if AP:
        ks = list(row.keys())
        c.execute("INSERT INTO listing_listing (" + ",".join(ks) + ") VALUES (" + ",".join(["%%s"] * len(ks)) + ")", [row[k] for k in ks])
        new = q("SELECT id FROM listing_listing WHERE id_code=%%s", [it["id_code"]])[0][0]
        for w in want: c.execute("INSERT INTO listing_section_listing (section_id, listing_id, featured) VALUES (%%s,%%s,0)", [w, new])
        for x in (tc or [(1,)]): c.execute("INSERT INTO listing_listing_property_status (listing_id, property_condition_id) VALUES (%%s,%%s)", [new, x[0]])
        print("@@   AGREGADA como registro %%s" %% new)

if AP:
    try:
        from django.db import transaction; transaction.commit_unless_managed()
    except Exception: pass
    try: connection.commit()
    except Exception: pass
    print("@@APLICADO")

''' % (AP, json.dumps(items))
open('/tmp/dbnew_code.py', 'w').write(code)
if AP:
    open('/root/respaldos/db-buscador-new-' + time.strftime('%Y%m%d%H%M') + '.json', 'w').write(json.dumps(items))
print(sh('cd /home/dapps/pcrappsearch && python2 manage.py shell < /tmp/dbnew_code.py 2>&1 | grep -o -E "@@.*|Error.*|rror:.*" | sed "s/^@@//" | cut -c1-500'))
print('LISTO' + ('' if AP else ' (solo vista previa, no se cambio nada)'))
