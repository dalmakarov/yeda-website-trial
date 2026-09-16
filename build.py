from bs4 import BeautifulSoup
from pathlib import Path
import html,json,re,urllib.request
ROOT=Path(__file__).parent
s=BeautifulSoup((ROOT/'reference/programs.html').read_text(),'html.parser')
def clean(node):
 for el in node.find_all(True):
  el.attrs={k:v for k,v in el.attrs.items() if k in ['href']}
 return node.decode_contents()
faq=[]
for b in s.select('button[aria-controls]'):
 p=s.find(id=b['aria-controls'])
 rich=p.select('[data-testid="richTextElement"]')
 faq.append({'question':b.get_text(' ',strip=True),'answer':''.join(clean(x) for x in rich)})
groups=[('Start Here',faq[14:18]),('What We Offer',faq[10:14]),('Programs & Pricing',faq[4:10]),('Flexibility',faq[0:4])]
plans=[]
for id in ['comp-mttkkvge','comp-mttkzhcx','comp-mttl04hi']:
 c=s.find(id=id); h=c.find('h3');name,price=h.get_text(' ',strip=True).split(' $');texts=[x.strip() for x in ' '.join(x.get_text(' ',strip=True) for x in c.select('p')).split('∙') if x.strip()];
 plans.append({'name':name,'price':'$'+price,'points':texts})
(ROOT/'content.json').write_text(json.dumps({'plans':plans,'faq':groups},ensure_ascii=False,indent=2))
fonts=(ROOT/'reference/fonts.css').read_text()
for w,url in re.findall(r'font-weight: (\d+);.*?url\((.*?)\)',fonts,re.S):
 path=ROOT/f'dist/assets/rubik-{w}.ttf'
 if not path.exists():urllib.request.urlretrieve(url,path)
 fonts=fonts.replace(url,f'assets/rubik-{w}.ttf')
(ROOT/'dist/fonts.css').write_text(fonts)
meta='\n'.join(str(x) for x in s.select('title,meta[name="description"],link[rel="canonical"],link[rel="alternate"],script[type="application/ld+json"]'))
nav=[('Programs','programs'),('About','about'),('Team','team'),('Contact Us','contact')]
def links():return ''.join(f'<a href="https://www.getyeda.com/{url}"'+(' aria-current="page"' if url=='programs' else '')+f'>{label}</a>' for label,url in nav)
def logo():return '<a class="brand" href="https://www.getyeda.com/" aria-label="Yeda home"><img src="assets/yeda-logo.png" width="124" height="65" alt="Yeda Logo"></a>'
def button():return '<a class="button" href="https://www.getyeda.com/contact">Contact Us <span aria-hidden="true">↗</span></a>'
cards=''
for i,p in enumerate(plans):
 pts=p['points'];cards+=f'''<article class="plan plan-{i} reveal" style="--delay:{i*65}ms" aria-labelledby="plan-{i}"><div class="plan-top"><span class="plan-number" aria-hidden="true">0{i+1}</span><h2 id="plan-{i}">{p['name']}</h2></div><p class="price">{p['price']}</p><p class="plan-fit">{pts[2]}</p><div class="plan-rule"></div><p class="schedule">{pts[0]}</p><ul class="plan-details"><li>{pts[1]}</li><li>{pts[3]}</li></ul></article>'''
faqhtml=''
for i,(name,items) in enumerate(groups):
 rows=''.join(f'<details><summary>{html.escape(x["question"])}<span class="plus" aria-hidden="true"></span></summary><div class="answer">{x["answer"]}</div></details>' for x in items)
 faqhtml+=f'<section class="faq-group reveal" id="faq-{i}"><div class="group-label"><span class="group-number" aria-hidden="true">0{i+1}</span><h3>{name}</h3></div><div class="faq-items">{rows}</div></section>'
intro='' 
# Read the exact existing introduction from the first rich text paragraph after the H1.
intro=s.find('h1').find_next('p').get_text(' ',strip=True)
page=f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">{meta}<meta name="robots" content="noindex, nofollow"><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="styles.css?v=2"><script src="app.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="container header-inner">{logo()}<nav class="desktop-nav" aria-label="Main navigation">{links()}</nav><a class="header-contact" href="mailto:hello@getyeda.com">hello@getyeda.com <span aria-hidden="true">↗</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu"><span></span><span></span></button><nav id="mobile-nav" class="mobile-nav" aria-label="Mobile navigation" hidden>{links()}</nav></div></header><main id="main"><section class="programs container"><div class="intro"><div><h1>Programs<span aria-hidden="true">.</span></h1><p>{intro}</p></div><a class="text-link" href="#questions">Questions before starting <span aria-hidden="true">↓</span></a></div><div class="plans">{cards}</div><div class="intake-row reveal"><p>During the free intake, we'll recommend what fits your teen.</p>{button()}</div></section><section class="questions" id="questions" aria-labelledby="faq-title"><div class="container"><div class="faq-intro reveal"><span class="eyebrow">FAQ</span><h2 id="faq-title">Questions parents ask<br class="desktop-break"> before starting</h2></div>{faqhtml}</div></section></main><footer class="site-footer"><div class="container"><div class="footer-grid"><div class="footer-brand">{logo()}<div class="social-links"><a href="https://www.facebook.com/yeda.tutoring.il/">Facebook</a><a href="https://www.instagram.com/yeda.tutoring.il">Instagram</a><a href="https://www.tiktok.com/@yeda.il">TikTok</a><a href="https://www.youtube.com/@Yeda-by-Golan">YouTube</a></div></div><nav class="footer-nav" aria-label="Footer navigation">{links()}<a href="https://www.getyeda.com/blog">Blog</a></nav><div class="office"><h2>Main Office</h2><p>Tiensesteenweg 247<br>Bierbeek, Belgium</p><p>BE1032162449</p></div><div class="footer-contact"><a href="mailto:hello@getyeda.com">hello@getyeda.com</a><a href="https://wa.me/32467300331">+32467300331 <span aria-hidden="true">↗</span></a></div></div><div class="footer-bottom"><span>Yeda BV</span><div><a href="https://www.getyeda.com/privacy-policy">Privacy Policy</a><a href="https://www.getyeda.com/terms-conditions">Terms &amp; Conditions</a></div></div></div></footer></body></html>'''
(ROOT/'dist/index.html').write_text(page)
print('Built',len(plans),'plans;',len(faq),'FAQ answers; metadata retained.')
print(json.dumps(plans,ensure_ascii=False,indent=2))
