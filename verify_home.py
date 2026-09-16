from bs4 import BeautifulSoup
from pathlib import Path
import json

root = Path(__file__).parent
old = BeautifulSoup((root / "reference/home.html").read_text(), "html.parser")
new = BeautifulSoup((root / "dist/index.html").read_text(), "html.parser")

checks = {
    "one_h1": len(new.select("h1")) == 1,
    "six_team_members": len(new.select(".team-card")) == 6,
    "six_method_cards": len(new.select(".method-card")) == 6,
    "three_reasons": len(new.select(".reason")) == 3,
    "two_local_videos": len(new.select("video source")) == 2,
    "title": old.title.text == new.title.text,
    "description": old.select_one('meta[name="description"]')["content"] == new.select_one('meta[name="description"]')["content"],
    "canonical": old.select_one('link[rel="canonical"]')["href"] == new.select_one('link[rel="canonical"]')["href"],
    "hreflang": [str(x) for x in old.select('link[rel="alternate"][hreflang]')] == [str(x) for x in new.select('link[rel="alternate"][hreflang]')],
    "json_ld_count": len(old.select('script[type="application/ld+json"]')) == len(new.select('script[type="application/ld+json"]')),
    "local_assets": all((root / "dist" / x.get("src")).exists() for x in new.select("img[src],video source[src],script[src]")),
    "forms_do_not_submit": not new.select("form[action],button[type=submit]"),
}

(root / "qa/home-source-checks.json").write_text(json.dumps(checks, indent=2))
print(json.dumps(checks, indent=2))
assert all(checks.values())
