from bs4 import BeautifulSoup
from pathlib import Path
import json
root=Path(__file__).parent
old=BeautifulSoup((root/'reference/programs.html').read_text(),'html.parser')
new=BeautifulSoup((root/'dist/programs/index.html').read_text(),'html.parser')
def norm(s):return ' '.join(s.split())
checks={}
checks['one_h1']=len(new.select('h1'))==1
checks['three_plans']=len(new.select('.plan'))==3
checks['18_faq_answers']=len(new.select('details'))==18
checks['title']=old.title.text==new.title.text
checks['description']=old.select_one('meta[name=description]')['content']==new.select_one('meta[name=description]')['content']
for sel in ['link[rel=canonical]','link[rel=alternate]','script[type="application/ld+json"]']:
 checks[sel]=[str(x) for x in old.select(sel)]==[str(x) for x in new.select(sel)]
checks['original_links']=set(a['href'].rstrip('/') for a in old.select('a[href]')).issubset(set(a['href'].rstrip('/') for a in new.select('a[href]')))
for b in old.select('button[aria-controls]'):
 q=b.get_text(' ',strip=True);p=old.find(id=b['aria-controls']);answer=' '.join(x.get_text(' ',strip=True) for x in p.select('[data-testid=richTextElement]'))
 d=next(d for d in new.select('details') if d.summary.get_text(' ',strip=True)==q)
 checks[q]=norm(answer)==norm(d.select_one('.answer').get_text(' ',strip=True))
checks['no_legacy_features']=all(t not in new.get_text() for t in ['Senior Academic Mentorship','5 Private 1:1 Lessons','4 Guided Practice Sessions'])
checks['local_assets']=all((root/'dist/programs'/x['src']).exists() for x in new.select('img[src],script[src]'))
(root/'qa/source-checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2));assert all(checks.values())
