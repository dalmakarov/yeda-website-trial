const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#mobile-nav');
function closeMenu(){menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu');nav.classList.remove('is-open');nav.setAttribute('aria-hidden','true');}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close menu':'Open menu');nav.classList.toggle('is-open',open);nav.setAttribute('aria-hidden',String(!open));});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus();}});
document.addEventListener('click',event=>{if(!event.target.closest('.header-inner'))closeMenu();});
matchMedia('(min-width:601px)').addEventListener('change',event=>{if(event.matches)closeMenu();});
if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('revealing');observer.unobserve(entry.target);}}),{threshold:.07});document.querySelectorAll('.reveal').forEach(element=>observer.observe(element));}
