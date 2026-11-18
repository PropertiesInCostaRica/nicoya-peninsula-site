import io,re,shutil,time,os
os.chdir('/var/www/propertiesincostarica.com/web')
F='homes.html'
s=io.open(F,encoding='utf-8',errors='surrogateescape').read()
sec=s.find('</section>',s.find('id="house_of_the_month"'))
arts=[m for m in re.finditer(r'<article class="listing">.*?</article>',s,re.S) if m.start()>sec]
m=[a for a in arts if re.search(r'ID CODE:\s*#4133\b',a.group(0))][0]
card=m.group(0)
shutil.copy(F,'/root/respaldos/homes-antes-m4133-'+time.strftime('%Y%m%d-%H%M'))
blk=re.compile(r'<!--###[^>]*?INI[^>]*?-->\s*'+re.escape(card)+r'\s*<!--###[^>]*?FIN[^>]*?-->\s*',re.S)
s,n=blk.subn('',s,count=1)
assert n==1
arts=[a for a in re.finditer(r'<article class="listing">.*?</article>',s,re.S) if a.start()>sec]
t=arts[8].start()
k=s.rfind('<!--###',sec,t)
pos=k if k>0 and s.find('</article>',k)>t else t
s=s[:pos]+'<!--###################INI#####################-->\n'+card+'\n<!--###################FIN#####################-->\n'+s[pos:]
io.open(F,'w',encoding='utf-8',errors='surrogateescape').write(s)
os.system('chown git:git homes.html; chmod 664 homes.html; /usr/local/bin/pcr-git-respaldo.sh >/dev/null 2>&1')
print('Orden ahora:', ', '.join(re.findall(r'ID CODE:\s*#(\d+)',s[s.find('id="house_of_the_month"'):])[:14])); print('LISTO')
