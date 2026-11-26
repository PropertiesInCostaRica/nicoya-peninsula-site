#!/usr/bin/env python3
# Cynthia's shared listings go AFTER PCR and Klaudia exclusives on every category page
# (never in Featured), right before Sold/Rented cards. Except Tamarindo, Conchal, Pinilla and Flamingo. Also makes sure they are on Luxury and Sea Side Homes.
import re, os, glob, shutil, time
W = '/var/www/propertiesincostarica.com/web/'
EV = ['properties/guanacaste/for_sale/modern-tropical-pool-home.html',
      'properties/guanacaste/for_sale/tamarindo-pool-home.html',
      'properties/guanacaste/for_sale/modern-home-casita-tamarindo.html',
      'properties/guanacaste/for_sale/ocean-view-estate-flamingo.html',
      'properties/guanacaste/for_sale/courtyard-home-playa-grande.html',
      'properties/guanacaste/for_sale/golf-view-residence-conchal.html',
      'properties/guanacaste/for_sale/beach-villa-avellanas.html',
      'properties/guanacaste/for_sale/golf-villa-conchal.html',
      'properties/guanacaste/for_sale/hacienda-estate-playa-grande.html']
ALWAYS = ['luxury_estates_in_costa_rica.html', 'homes/sea_side_homes.html']
# Area pages where PCR has no own listings: Cynthia's can stay first and Featured there
# Mirtha: only on Beach it matters that PCR and Klaudia listings go first
ONLY = ['beach.html']
SKIP = ['tamarindo-real-estate.html', 'conchal.html', 'pinilla_real_estate.html', 'flamingo_real_estate.html']
BLK = re.compile(r'<!--#+INI#+-->\s*<article class="listing".*?</article>\s*<!--#+FIN#+-->', re.S)
B = '/root/respaldos/evorder-' + time.strftime('%Y%m%d%H%M') + '/'
os.makedirs(B, exist_ok=True)
def rd(p): return open(p, encoding='utf-8', errors='surrogateescape').read()
def wr(p, s): open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
def ev_of(c):
    for i, r in enumerate(EV):
        if 'href="/' + r + '"' in c: return i
    return -1
def gone(c): return bool(re.search(r'Sold!|>\s*SOLD\b|RENTED|Rented!', c))
cards = {}
for f in ('homes.html', 'beach.html', 'tamarindo-real-estate.html'):
    for m in BLK.finditer(rd(W + f)):
        i = ev_of(m.group(0))
        if i >= 0 and i not in cards: cards[i] = m.group(0)
pages = [p for p in glob.glob(W + '*.htm*') + glob.glob(W + '*/*.htm*') if '-nuevo' not in p and '/properties/' not in p]
changed = 0
for p in sorted(pages):
    s = rd(p)
    rel = p[len(W):]
    if rel in SKIP or rel not in ONLY: continue
    if rel not in ALWAYS and not any(('href="/' + r + '"') in s for r in EV): continue
    fi = s.find('featured_listing_of')
    fs = s.rfind('<section', 0, fi) if fi >= 0 else -1
    fe = s.find('</section>', fi) + len('</section>') if fi >= 0 else -1
    have = {}
    # pull EV cards out of the list part (after featured)
    head, feat, tail = (s[:fs], s[fs:fe], s[fe:]) if fi >= 0 else (s[:0], '', s)
    def take(txt):
        out = []
        def rep(m):
            i = ev_of(m.group(0))
            if i >= 0:
                have[i] = m.group(0); return ''
            return m.group(0)
        return BLK.sub(rep, txt)
    nfeat_ev = sum(1 for m in BLK.finditer(feat) if ev_of(m.group(0)) >= 0)
    feat = take(feat)
    tail = take(tail)
    if fi < 0: tail = s[:0] + tail; head = ''
    # refill featured with the first PCR cards from the list
    for _ in range(nfeat_ev):
        m = next((m for m in BLK.finditer(tail) if not gone(m.group(0))), None)
        if not m: break
        tail = tail[:m.start()] + tail[m.end():]
        j = feat.rfind('</section>')
        feat = feat[:j] + m.group(0) + '\n' + feat[j:]
    if rel in ALWAYS:
        for i, c in cards.items():
            if i not in have and os.path.exists(W + EV[i]): have[i] = c
    if not have: continue
    lst = list(BLK.finditer(tail))
    sold = [m for m in lst if gone(m.group(0))]
    if sold: pos = sold[0].start()
    elif lst: pos = lst[-1].end()
    else: pos = 0
    block = '\n' + '\n'.join(have[i] for i in sorted(have)) + '\n'
    tail = re.sub(r'\n{3,}', '\n\n', tail[:pos] + block + tail[pos:])
    new = head + feat + tail
    if new != s:
        shutil.copy2(p, B + rel.replace('/', '_'))
        wr(p, new); changed += 1
        print('Ordenado: %s (%d de Cynthia al final%s)' % (rel, len(have), ', sacadas de Featured' if nfeat_ev else ''))
os.system('bash /root/pcr-git-respaldo.sh >/dev/null 2>&1')
print('LISTO evorder (%d paginas)' % changed)
