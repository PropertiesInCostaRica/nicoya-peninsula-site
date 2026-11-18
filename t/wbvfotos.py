import io,re,os,shutil,time
os.chdir('/var/www/propertiesincostarica.com/web')
SLUG='whale-bay-villa'; D='properties/Images/'+SLUG; P='properties/puntarenas/for_sale/'+SLUG+'.html'
SRC='https://www.properties-in-costa-rica.com/img/whale-bay-villa'; N=38
CDN='https://cdn.propertiesincostarica.com/'+D
ts=time.strftime('%Y%m%d-%H%M')
tmp='/tmp/wbvnew'; shutil.rmtree(tmp,ignore_errors=True); os.makedirs(tmp+'/opt/thumbs')
bad=0
for i in range(1,N+1):
    for sub in ('opt','opt/thumbs'):
        bad+=os.system('wget -q -O %s/%s/photo-%d.jpg %s/%s/photo-%d.jpg'%(tmp,sub,i,SRC,sub,i))!=0
bad+=os.system('wget -q -O %s/p.gif %s/p.gif'%(tmp,SRC))!=0
assert bad==0,'fallo la descarga de fotos, no cambie nada'
shutil.move(D,'/root/respaldos/'+SLUG+'-fotos-antes-'+ts)
shutil.copytree(tmp,D)
s=io.open(P,encoding='utf-8',errors='surrogateescape').read()
shutil.copy(P,'/root/respaldos/'+SLUG+'-pagina-antes-'+ts)
m=re.search(r'(<!-- InstanceBeginEditable name="content" -->)(.*?)(<!-- InstanceEndEditable -->)',s,re.S)
c=m.group(2)
alt=re.search(r'alt="([^"]*)"',c).group(1)
c=re.sub(r'<p class="photo">.*?</p>\n?','',c,flags=re.S)
def pb(fs): return '<p class="photo">\n'+''.join('<a href="%s/opt/%s"><img src="%s/opt/thumbs/%s" alt="%s" width="250" height="187"></a>'%(CDN,f,CDN,f,alt) for f in fs)+'\n<span class="to_enlarge">Click on the pictures to enlarge</span>\n</p>\n'
G=[[1,9,20,21],[4,15,12,18],[5,16,17,6,7,23,24,25,26,27,28,29],[2,10,11,13,14,19,22],[36,37,38],[3,30,31,32,33,34,35],[8]]
assert sorted(x for g in G for x in g)==list(range(1,N+1))
def blocks(g):
    fs=['photo-%d.jpg'%i for i in g]
    return ''.join(pb(fs[i:i+3]) for i in range(0,len(fs),3))
parts=re.split(r'(?=<p>)',c)
out='';k=0
for p in parts:
    out+=p
    if p.startswith('<p>') and k<len(G) and not p.startswith('<p><strong>Property Highlights'):
        out+=blocks(G[k]); k+=1
assert k==len(G),'parrafos: %d'%k
s=s[:m.start(2)]+out+s[m.end(2):]
io.open(P,'w',encoding='utf-8',errors='surrogateescape').write(s)
os.system('chown -R git:git %s %s; find %s -type d -exec chmod 775 {} +; find %s -type f -exec chmod 664 {} +; chmod 664 %s; /usr/local/bin/pcr-git-respaldo.sh >/dev/null 2>&1'%(D,P,D,D,P))
print('Fotos en la pagina:',s.count('/opt/thumbs/photo-')); print('LISTO')
