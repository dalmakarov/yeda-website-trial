const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#mobile-nav');
function closeMenu(){menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu');nav.classList.remove('is-open');nav.setAttribute('aria-hidden','true');}
nav.hidden=false;
nav.setAttribute('aria-hidden','true');
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close menu':'Open menu');nav.classList.toggle('is-open',open);nav.setAttribute('aria-hidden',String(!open));});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}});
document.addEventListener('click',e=>{if(!e.target.closest('.header-inner'))closeMenu();});
matchMedia('(min-width:601px)').addEventListener('change',e=>{if(e.matches)closeMenu();});
document.querySelectorAll('details .answer').forEach(answer=>{const inner=document.createElement('div');inner.className='answer-inner';while(answer.firstChild)inner.append(answer.firstChild);answer.append(inner);});
if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('revealing');observer.unobserve(entry.target);}});},{threshold:.07});document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));}

const localRoutes={'https://www.getyeda.com/':'/','https://www.getyeda.com/programs':'/programs/','https://www.getyeda.com/about':'/about/','https://www.getyeda.com/team':'/team/','https://www.getyeda.com/contact':'/contact/','https://www.getyeda.com/first-lesson-us':'/first-lesson-us/'};
document.querySelectorAll('a[href]').forEach(link=>{if(localRoutes[link.href])link.href=localRoutes[link.href];});
