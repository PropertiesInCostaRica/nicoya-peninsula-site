/* PCR: botones "Request Details" (formulario) y "Schedule a Showing" (WhatsApp) al final de la descripcion */
(function(){
if(document.querySelector('.pcr-req'))return;
var f=document.getElementById('link_to_the_form');
var cu=document.querySelector('.contactus_link');
if(!f||!cu||!cu.parentNode)return;
var css=document.createElement('style');css.id='pcr-req-css';
css.textContent='.pcr-req-wrap{display:flex;flex-direction:column;gap:12px;margin:12px 0 24px;clear:both}'
+'.pcr-req,.pcr-req:link,.pcr-req:visited,.pcr-req:focus,.pcr-req:active{display:inline-flex;align-items:center;justify-content:center;gap:10px;color:#fff!important;font-family:Oswald,"Arial Narrow",sans-serif;font-size:18px;text-transform:uppercase;letter-spacing:2px;text-decoration:none!important;padding:16px 10px;border-radius:2px;width:100%;box-sizing:border-box;border:0!important;outline:none;box-shadow:0 3px 10px rgba(0,0,0,.15);cursor:pointer}'
+'.pcr-req.b1,.pcr-req.b1:link,.pcr-req.b1:visited,.pcr-req.b1:focus{background:#048dc7!important}.pcr-req.b1:hover,.pcr-req.b1:active{background:#0b6f9c!important}'
+'.pcr-req.b2,.pcr-req.b2:link,.pcr-req.b2:visited,.pcr-req.b2:focus{background:#25D366!important}.pcr-req.b2:hover,.pcr-req.b2:active{background:#1ba851!important}'
+'.pcr-req svg{width:20px;height:20px;fill:#fff;flex:none}'
+'@media(min-width:768px){.contactus_link{display:none!important}}'
;
document.head.appendChild(css);
var h=document.querySelector('h1'),t=h?h.textContent.trim():document.title;
var m=document.body.innerText.match(/ID CODE:?\s*#\s*(\d+)/i),id=m?m[1]:'';
var msg='Hi, I would like to schedule a showing of '+t+(id?' (ID #'+id+')':'')+': '+location.href.split('#')[0].split('?')[0];
var w=document.createElement('div');w.className='pcr-req-wrap';
var a=document.createElement('a');a.className='pcr-req b1';a.href='javascript:;';a.textContent='Request Details';
a.onclick=function(e){e.preventDefault();f.click();};
var b=document.createElement('a');b.className='pcr-req b2';b.target='_blank';b.rel='noopener';
b.href='https://wa.me/50688225061?text='+encodeURIComponent(msg);
b.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.52 3.48A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.9 11.9 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.42-8.43zm-8.47 18.32a9.9 9.9 0 0 1-5.05-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.28c0-5.45 4.44-9.89 9.9-9.89 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.9 7c0 5.45-4.44 9.9-9.89 9.9zm5.43-7.41c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.06 2.88 1.21 3.08c.15.2 2.1 3.2 5.08 4.48.71.31 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2.01-1.41.25-.69.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35z"/></svg>Schedule a Showing';
w.appendChild(a);w.appendChild(b);cu.parentNode.insertBefore(w,cu);
})();
