from pathlib import Path
from bs4 import BeautifulSoup

root = Path(__file__).parent / "dist"
pages = {
    "home": root / "index.html",
    "programs": root / "programs/index.html",
    "about": root / "about/index.html",
    "team": root / "team/index.html",
    "contact": root / "contact/index.html",
    "first lesson": root / "first-lesson-us/index.html",
}

errors = []
for name, path in pages.items():
    soup = BeautifulSoup(path.read_text(), "html.parser")
    if len(soup.find_all("h1")) != 1:
        errors.append(f"{name}: expected exactly one H1")
    if not soup.title or not soup.find("meta", attrs={"name": "description"}):
        errors.append(f"{name}: missing title or description")
    if not soup.find("link", rel="canonical"):
        errors.append(f"{name}: missing canonical")
    if len(soup.find_all("link", hreflang=True)) < 2:
        errors.append(f"{name}: missing hreflang")
    if not soup.find("meta", attrs={"name": "robots", "content": lambda x: x and "noindex" in x}):
        errors.append(f"{name}: prototype is not protected by noindex")
    for node in soup.find_all(["img", "source"], src=True):
        src = node["src"]
        if src.startswith("/") and not (root / src.lstrip("/")).exists():
            errors.append(f"{name}: missing local asset {src}")

team = BeautifulSoup(pages["team"].read_text(), "html.parser")
if len(team.select(".person")) != 10:
    errors.append("team: expected 10 current members")
if len(team.select(".profile-button")) != 10:
    errors.append("team: expected 10 profile controls")
app_js = (root / "app.js").read_text()
if app_js.count("bio:") != 10:
    errors.append("team: expected 10 preserved biographies")
first = BeautifulSoup(pages["first lesson"].read_text(), "html.parser")
if "$30" not in first.get_text(" "):
    errors.append("first lesson: current price is missing")

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: 6 pages, one H1 each, metadata/noindex present, local assets resolved, team and first-lesson facts retained")
