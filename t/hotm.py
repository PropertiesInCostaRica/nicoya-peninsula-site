import io,re,shutil,time,os
os.chdir('/var/www/propertiesincostarica.com/web')
F='homes.html'
s=io.open(F,encoding='utf-8',errors='surrogateescape').read()
i=s.find('id="house_of_the_month"'); assert i>0, 'no encuentro House of the Month'
a=s.find('<article class="listing">',i); b=s.find('</article>',a)+len('</article>')
old=s[a:b]; assert '#4133' in old, 'la tarjeta destacada no es 4133'
m=None
for mm in re.finditer(r'<article class="listing">.*?</article>',s,re.S):
    if mm.start()>b and re.search(r'ID CODE:\s*#4231\b',mm.group(0)): m=mm; break
assert m, 'no encuentro la tarjeta 4231 en la lista'
c4231=m.group(0).replace(' style="display: inline;"','')
shutil.copy(F,'/root/respaldos/homes-antes-hotm-'+time.strftime('%Y%m%d-%H%M'))
# 1. quitar 4231 de la lista (con sus marcas INI/FIN)
blk=re.compile(r'<!--###[^>]*?INI[^>]*?-->\s*'+re.escape(m.group(0))+r'\s*<!--###[^>]*?FIN[^>]*?-->\s*',re.S)
s2,n=blk.subn('',s,count=1)
if n==0: s2=s[:m.start()]+s[m.end():]
s=s2
# 2. 4231 sube a House of the Month
i=s.find('id="house_of_the_month"'); a=s.find('<article class="listing">',i); b=s.find('</article>',a)+len('</article>')
s=s[:a]+c4231+s[b:]
# 3. 4133 baja a la posicion 6 de la lista
sec=s.find('</section>',i)
cards=[mm for mm in re.finditer(r'<!--###[^>]*?INI[^>]*?-->\s*<article class="listing">.*?</article>\s*<!--###[^>]*?FIN[^>]*?-->',s,re.S) if mm.start()>sec]
pos=cards[5].start()
s=s[:pos]+'<!--###################INI#####################-->\n'+old+'\n<!--###################FIN#####################-->\n'+s[pos:]
io.open(F,'w',encoding='utf-8',errors='surrogateescape').write(s)
os.system('chown git:git homes.html; chmod 664 homes.html; /usr/local/bin/pcr-git-respaldo.sh >/dev/null 2>&1')
ids=re.findall(r'ID CODE:\s*#(\d+)',s[s.find('id="house_of_the_month"'):])
print('Orden ahora:', ', '.join(ids[:10])); print('LISTO')
