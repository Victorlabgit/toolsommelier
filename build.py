#!/usr/bin/env python3
"""Static site generator for The Tool Sommelier.

Usage:  python3 build.py
Edit LINKS below to swap official URLs for affiliate links: every page updates.
Articles live in content.py.
"""
import datetime, html, json, pathlib, re

from content import ARTICLES
from blog import POSTS

SITE = "https://toolsommelier.com"
NAME = "The Tool Sommelier"
TAGLINE = "The right AI tool, perfectly paired to your job."
TODAY = datetime.date.today()
ROOT = pathlib.Path(__file__).parent
import hashlib
CSS_VERSION = hashlib.md5((ROOT / "assets" / "style.css").read_bytes()).hexdigest()[:8]
INDEXNOW_KEY = "6569fc83f4f3f0dc3af02b621d2590d1"  # key file /<key>.txt is written by main(); ping https://api.indexnow.org/indexnow?url=<url>&key=<key>

# Real publication / modification dates, tracked by content hash (dates.json, commit it).
DATES_FILE = ROOT / "dates.json"
DATES = json.loads(DATES_FILE.read_text()) if DATES_FILE.exists() else {}


def stamp(key, obj):
    h = hashlib.md5(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:12]
    t = TODAY.isoformat()
    e = DATES.get(key)
    if not e:
        e = DATES[key] = {"hash": h, "published": t, "modified": t}
    elif not e.get("hash"):
        e["hash"] = h
    elif e["hash"] != h:
        e.update(hash=h, modified=t)
    return e


def og_image(key, kicker, title):
    """Per-page 1200x630 social card in the cellar style. Returns its absolute URL."""
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    name = re.sub(r"[^a-z0-9-]+", "-", key.lower()).strip("-") or "home"
    path = ROOT / "assets" / "og" / f"{name}.png"
    sig = hashlib.md5((kicker + title).encode()).hexdigest()[:10]
    e = DATES.setdefault("og:" + key, {})
    if path.exists() and e.get("sig") == sig:
        return f"{SITE}/assets/og/{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#150c0f")
    glow = Image.new("RGB", (W, H), "#150c0f")
    ImageDraw.Draw(glow).ellipse((W - 520, -320, W + 260, 380), fill="#5e1622")
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(140)), 0.9)
    d = ImageDraw.Draw(img)
    d.rectangle((28, 28, W - 29, H - 29), outline="#d8bf8a", width=2)
    fdir = "/usr/share/fonts/truetype/liberation/"
    f_k = ImageFont.truetype(fdir + "LiberationSerif-Italic.ttf", 34)
    f_s = ImageFont.truetype(fdir + "LiberationSans-Regular.ttf", 26)
    d.text((84, 84), kicker, font=f_k, fill="#d8bf8a")
    size = 68
    while True:
        f_t = ImageFont.truetype(fdir + "LiberationSerif-Bold.ttf", size)
        words, lines, cur = title.split(), [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if d.textlength(test, font=f_t) > W - 200 and cur:
                lines.append(cur); cur = w
            else:
                cur = test
        lines.append(cur)
        if len(lines) <= 4 or size <= 44:
            break
        size -= 6
    y = 150 + (4 - len(lines)) * size * 0.35
    for ln in lines:
        d.text((84, y), ln, font=f_t, fill="#f1e9dd"); y += size * 1.15
    d.text((84, H - 96), "toolsommelier.com", font=f_s, fill="#d8bf8a")
    try:
        logo = Image.open(ROOT / "assets" / "logo.png").convert("RGBA"); logo.thumbnail((92, 92))
        img.paste(logo, (W - 84 - logo.width, H - 76 - logo.height), logo)
    except Exception:
        pass
    img.save(path, optimize=True)
    e["sig"] = sig
    return f"{SITE}/assets/og/{name}.png"

# ---------------------------------------------------------------------------
# One place for every outbound link. Replace a URL with your affiliate link
# once you are approved, set "aff": True, then run build.py again.
# ---------------------------------------------------------------------------
LINKS = {
    "ElevenLabs":  {"url": "https://try.elevenlabs.io/q2j4i44qw31b", "aff": True},
    "Murf AI":     {"url": "https://murf.ai",         "aff": False},
    "Descript":    {"url": "https://www.descript.com","aff": False},
    "Speechify":   {"url": "https://speechify.com",   "aff": False},
    "Synthesia":   {"url": "https://www.synthesia.io/?via=victor-wagner", "aff": True},
    "HeyGen":      {"url": "https://www.heygen.com",  "aff": False},
    "Runway":      {"url": "https://runwayml.com",    "aff": False},
    "Otter.ai":    {"url": "https://otter.ai",        "aff": False},
    "Fireflies.ai":{"url": "https://fireflies.ai/?fpr=victor-4901be", "aff": True},
    "Fathom":      {"url": "https://www.fathom.ai",   "aff": False},
    "tl;dv":       {"url": "https://tldv.cello.so/XeSTTwlN4cX", "aff": True},
    "Jasper":      {"url": "https://www.jasper.ai",   "aff": False},
    "Copy.ai":     {"url": "https://www.copy.ai",     "aff": False},
    "Writesonic":  {"url": "https://writesonic.com",  "aff": False},
    "Grammarly":   {"url": "https://www.grammarly.com","aff": False},
    "Surfer":      {"url": "https://surfer.ai",       "aff": False},
    "Frase":       {"url": "https://www.frase.io",    "aff": False},
    "NeuronWriter":{"url": "https://neuronwriter.com","aff": False},
    "Semrush":     {"url": "https://www.semrush.com", "aff": False},
}

LOGO_MARK = '<g stroke="#d8bf8a" stroke-width="10"><line x1="170" y1="170" x2="256" y2="140"/><line x1="256" y1="140" x2="342" y2="170"/><line x1="170" y1="170" x2="256" y2="256"/><line x1="342" y1="170" x2="256" y2="256"/><line x1="256" y1="256" x2="170" y2="342"/><line x1="256" y1="256" x2="342" y2="342"/><line x1="170" y1="342" x2="256" y2="372"/><line x1="342" y1="342" x2="256" y2="372"/></g><g fill="#150c0f" stroke="#d8bf8a" stroke-width="10"><circle cx="170" cy="170" r="24"/><circle cx="342" cy="170" r="24"/><circle cx="170" cy="342" r="24"/><circle cx="342" cy="342" r="24"/><circle cx="256" cy="140" r="18"/><circle cx="256" cy="372" r="18"/></g><circle cx="256" cy="256" r="38" fill="#9a2a3b" stroke="#d8bf8a" stroke-width="10"/>'
LOGO_SVG = '<svg width="34" height="34" viewBox="110 90 292 332" aria-hidden="true">' + LOGO_MARK + '</svg>'
FAVICON = "data:image/svg+xml," + ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'><rect width='512' height='512' rx='112' fill='%23150c0f'/>" + LOGO_MARK.replace('"', "'").replace('#', '%23') + '</svg>')
FONTS = '<link rel="preconnect" href="https://fonts.bunny.net"><link rel="stylesheet" href="https://fonts.bunny.net/css?family=cormorant-garamond:400,400i,500,600|manrope:400,500,600&display=swap">'

# Monogram seals stand in for vendor logos (we do not reproduce trademarks).
SEAL_COLORS = ["#7b1e2c", "#2f4a3a", "#3b3561", "#6a4a1e", "#24485e", "#5b2448", "#4a3b2a", "#2d4f4f"]

SOCIALS = [
    ("Instagram", "https://www.instagram.com/toolsommelier/", '<path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM12 3.6c2.7 0 3 0 4.1.1 2.7.1 4 1.4 4.1 4.1.1 1.1.1 1.4.1 4.1s0 3-.1 4.1c-.1 2.7-1.4 4-4.1 4.1-1.1.1-1.4.1-4.1.1s-3 0-4.1-.1c-2.7-.1-4-1.4-4.1-4.1C3.7 15 3.7 14.7 3.7 12s0-3 .1-4.1C3.9 5.2 5.2 3.9 7.9 3.8 9 3.7 9.3 3.6 12 3.6zM12 2c-2.7 0-3.1 0-4.1.1C4.2 2.2 2.2 4.2 2.1 7.9 2 8.9 2 9.3 2 12s0 3.1.1 4.1c.1 3.7 2.1 5.7 5.8 5.8 1 .1 1.4.1 4.1.1s3.1 0 4.1-.1c3.7-.1 5.7-2.1 5.8-5.8.1-1 .1-1.4.1-4.1s0-3.1-.1-4.1c-.1-3.7-2.1-5.7-5.8-5.8C15.1 2 14.7 2 12 2z"/>'),
    ("LinkedIn", "https://www.linkedin.com/company/147035173/", '<path d="M20.4 2H3.6C2.7 2 2 2.7 2 3.6v16.8c0 .9.7 1.6 1.6 1.6h16.8c.9 0 1.6-.7 1.6-1.6V3.6c0-.9-.7-1.6-1.6-1.6zM8 19H5V9.5h3V19zM6.5 8.2a1.7 1.7 0 1 1 0-3.5 1.7 1.7 0 0 1 0 3.5zM19 19h-3v-4.6c0-1.1 0-2.5-1.5-2.5s-1.8 1.2-1.8 2.4V19h-3V9.5h2.9v1.3c.4-.8 1.4-1.6 2.9-1.6 3.1 0 3.6 2 3.6 4.6V19z"/>'),
    ("Facebook", "https://www.facebook.com/profile.php?id=61597053747157", '<path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/>'),
]


def social_links(cls="socials"):
    return f'<div class="{cls}">' + "".join(
        f'<a href="{u}" target="_blank" rel="noopener me" aria-label="{n}" title="{n}"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">{d}</svg></a>'
        for n, u, d in SOCIALS) + "</div>"


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace(".", "").replace(";", "")).strip("-")


def seal(name, size=None):
    letters = re.sub(r"[^A-Za-z]", "", name.split(".")[0])
    second = next((c for c in letters[1:] if c.isupper()), letters[1] if len(letters) > 1 else "")
    initials = (letters[0].upper() + second.lower()) if second else letters.upper()
    color = SEAL_COLORS[sum(map(ord, name)) % len(SEAL_COLORS)]
    st = f"--c:{color}" + (f";--s:{size}px" if size else "")
    return f'<span class="seal" style="{st}" aria-hidden="true">{initials}</span>'


def link(name, text=None, cls=None):
    """Outbound link to a tool, with the right rel attributes."""
    data = LINKS[name]
    rel = "sponsored nofollow noopener" if data["aff"] else "nofollow noopener"
    c = f' class="{cls}"' if cls else ""
    ev = "affiliate-click" if data["aff"] else "outbound-click"
    track = f' data-umami-event="{ev}" data-umami-event-tool="{html.escape(name)}"'
    return f'<a href="{data["url"]}" target="_blank" rel="{rel}"{c}{track}>{html.escape(text or name)}</a>'


def page(title, description, path, body, schema=None, og=None, ptype="website", dates=None):
    canonical = f"{SITE}/{path}"
    og = og or f"{SITE}/assets/linkedin-banner.png"
    art = (f'<meta property="article:published_time" content="{dates["published"]}">\n<meta property="article:modified_time" content="{dates["modified"]}">\n') if dates else ""
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#150c0f">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{ptype}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
{art}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<link rel="alternate" type="application/rss+xml" title="{NAME} Journal" href="{SITE}/blog/feed.xml">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/style.css?v={CSS_VERSION}">
<script defer src="https://cloud.umami.is/script.js" data-website-id="ad65cc86-b768-4880-a7d9-c9a12f0486d1"></script>
{ld}
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="logo" href="/">{LOGO_SVG}<span class="logo-word">The Tool <i>Sommelier</i></span></a>
  <nav class="main"><a href="/#guides">Guides</a><a href="/blog/">Journal</a><a href="/about.html" class="hide-sm">How we pick</a>{social_links("socials head hide-sm")}</nav>
</div></header>
<main>
<div class="subscribed-banner" id="subscribed" hidden><div class="wrap">You're in. Welcome to The Weekly Pairing: your first email is on its way.</div></div>
<script>if(location.search.indexOf("subscribed=1")>-1){{document.getElementById("subscribed").hidden=false}}</script>
{body}
</main>
<footer><div class="wrap">
  <div class="cols">
    <div><p class="brand">The Tool Sommelier</p><p>{TAGLINE}<br>Independent comparisons of AI software, written for people who have a job to do.</p><p class="follow">Follow the cellar</p>{social_links()}</div>
    <div><a href="/#guides">All guides</a><a href="/blog/">The Journal</a><a href="/about.html">How we pick</a><a href="mailto:contact@toolsommelier.com">Contact</a></div>
    <div><a href="/disclosure.html">Affiliate disclosure</a><a href="/privacy.html">Privacy</a><a href="/legal.html">Legal notice</a></div>
  </div>
  <p class="fine">Some links are affiliate links; they never change our rankings. Product names belong to their respective owners; ElevenLabs is a trademark of Eleven Labs Inc. &copy; {TODAY.year} {NAME}.</p>
</div></footer>
</body>
</html>
"""


NEWSLETTER_FORM_ID = "355046cc-7ca6-4d5c-a011-d2f49d56e5b0"


def newsletter_block(variant="dark"):
    return f"""
<aside class="newsletter {variant}" id="newsletter">
  <div class="nl-copy">
    <p class="kind">The Weekly Pairing</p>
    <h2>One short email a week. The AI tools worth your time.</h2>
    <p>New guides, honest picks and what changed in the tools you use. Free, no spam, unsubscribe in one click.</p>
  </div>
  <div class="nl-form"><script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" data-beehiiv-form="{NEWSLETTER_FORM_ID}"></script></div>
</aside>"""


def render_article(a):
    dt = stamp(a["slug"], a)
    og = og_image(a["slug"], a["category"], a["h1"])
    picks_html = ""
    toc = ['<a href="#at-a-glance">At a glance</a>']
    for p in a["picks"]:
        pros = "".join(f"<li>{x}</li>" for x in p["pros"])
        cons = "".join(f"<li>{x}</li>" for x in p["cons"])
        toc.append(f'<a href="#{slug(p["tool"])}">{p["tool"]}</a>')
        best = p['best_for'][0].lower() + p['best_for'][1:]
        picks_html += f"""
<section class="pick" id="{slug(p['tool'])}">
  {seal(p['tool'])}
  <div>
    <p class="rank">{p['label']}</p>
    <h3>{p['tool']}</h3>
    <p class="best-for">Best for {best}. Free option: {p['free'][0].lower() + p['free'][1:]}.</p>
    <p class="tasting">{p['note']}</p>
    <p>{p['body']}</p>
    <div class="pros-cons"><div><strong>Why we like it</strong><ul>{pros}</ul></div>
    <div><strong>Watch out for</strong><ul>{cons}</ul></div></div>
    {link(p['tool'], f"Visit {p['tool']}", "btn ink")}
  </div>
</section>"""
    for h, _ in a.get("extra", []):
        toc.append(f'<a href="#{slug(h)}">{h}</a>')
    toc += ['<a href="#how-to-choose">How to choose</a>', '<a href="#faq">FAQ</a>']

    rows = "".join(
        f"<tr><td><span class=\"tcell\">{seal(p['tool'], 34)}{p['tool']}</span></td><td>{p['best_for']}</td><td>{p['free']}</td><td>{link(p['tool'], 'Visit')}</td></tr>"
        for p in a["picks"])
    table = f"""<div class="table-scroll"><table class="compare">
<tr><th>Tool</th><th>Best for</th><th>Free option</th><th></th></tr>{rows}</table></div>
<p class="small-note">Plans and prices change often. Check the official pricing page before you buy.</p>"""

    faq_html = "".join(f"<h3>{q}</h3><p>{ans}</p>" for q, ans in a["faq"])
    sections = "".join(f'<h2 id="{slug(h)}">{h}</h2>{b}' for h, b in a.get("extra", []))
    seals = "".join(seal(p["tool"]) for p in a["picks"])

    body = f"""
<div class="wrap">
<div class="article-top">
  <div class="crumbs"><a href="/">Home</a> / <a href="/#guides">Guides</a></div>
  <h1>{a['h1']}</h1>
  <p class="standfirst">{a['description']}</p>
  <div class="seals">{seals}</div>
  <div class="meta">Updated {fmt_date(dt['modified'])}, {a['read']} min read</div>
</div>
</div>
<div class="paper"><div class="wrap"><div class="paper-grid">
<nav class="toc" aria-label="On this page"><strong>On this page</strong>{''.join(toc)}</nav>
<article>
<p class="notice">Contains affiliate links. <a href="/disclosure.html">Disclosure</a></p>
{a['intro']}
<div class="verdict"><h2>The short answer</h2>{a['verdict']}</div>
<h2 id="at-a-glance">At a glance</h2>
{table}
{picks_html}
{sections}
<h2 id="how-to-choose">How to choose</h2>
{a['how_to_choose']}
<div class="faq"><h2 id="faq">FAQ</h2>{faq_html}</div>
<p class="small-note">Our rankings are based on each tool's official documentation, published plans and independent user reviews. <a href="/about.html">How we pick</a>.</p>
{related_reading(a)}
{newsletter_block()}
</article>
</div></div></div>"""

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": a["h1"], "description": a["description"],
             "datePublished": dt["published"], "dateModified": dt["modified"], "image": og,
             "author": {"@type": "Organization", "name": NAME, "url": SITE + "/about.html"},
             "publisher": {"@type": "Organization", "name": NAME, "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo.png"}},
             "mainEntityOfPage": f"{SITE}/{a['slug']}.html"},
            {"@type": "ItemList", "name": a["h1"], "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": p["tool"], "url": f"{SITE}/{a['slug']}.html#{slug(p['tool'])}"}
                for i, p in enumerate(a["picks"])]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Guides", "item": SITE + "/#guides"},
                {"@type": "ListItem", "position": 3, "name": a["h1"], "item": f"{SITE}/{a['slug']}.html"}]},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(ans)}}
                for q, ans in a["faq"]]},
        ],
    }
    return page(a["title"], a["description"], f"{a['slug']}.html", body, schema, og=og, ptype="article", dates=dt)


def related_reading(a):
    """Internal links from a guide: Journal notes on the same guide, then sibling guides sharing a tool."""
    from blog import POSTS as _P
    notes = sorted([q for q in _P if q["guide"] == a["slug"]], key=lambda q: q["date"], reverse=True)[:5]
    tools = {p["tool"] for p in a["picks"]}
    sibs = [g for g in ARTICLES if g["slug"] != a["slug"] and (tools & {p["tool"] for p in g["picks"]} or g["category"] == a["category"])]
    sibs += [g for g in ARTICLES if g["slug"] != a["slug"] and g not in sibs]
    out = ""
    if notes:
        out += '<h2 id="from-the-journal">Questions people ask</h2><ul class="related">' + "".join(
            f'<li><a href="/blog/{q["slug"]}.html">{q["h1"]}</a></li>' for q in notes) + "</ul>"
    out += '<div class="more-notes"><h2>More pairings</h2><ul>' + "".join(
        f'<li><a href="/{g["slug"]}.html">{g["h1"]}</a></li>' for g in sibs[:4]) + "</ul></div>"
    return out


CARTE = [
    ("A voiceover that sounds human", "ElevenLabs", "best-ai-voice-generators.html#elevenlabs"),
    ("Training videos, no camera", "Synthesia", "best-ai-video-generators.html#synthesia"),
    ("Your face, in any language", "HeyGen", "synthesia-vs-heygen.html#heygen"),
    ("Meeting notes for free", "Fathom", "best-ai-meeting-note-takers.html#fathom"),
    ("Edit a podcast like a doc", "Descript", "best-ai-voice-generators.html#descript"),
    ("On-brand marketing copy", "Jasper", "best-ai-writing-tools.html#jasper"),
]


def render_home():
    latest = sorted(POSTS, key=lambda p: p["date"], reverse=True)[:3]
    journal = (f'<section class="section"><div class="wrap"><div class="section-head"><h2>From the Journal</h2>'
               f'<p>Quick answers to the questions people ask before they choose. <a href="/blog/">All notes</a></p></div>'
               f'<div class="post-grid">{"".join(post_card(p) for p in latest)}</div></div></section>') if latest else ""
    carte = "".join(f'<li><a href="/{href}"><span class="job">{job}</span><span class="leader"></span><span class="tool">{tool}</span></a></li>'
                    for job, tool, href in CARTE)
    cards = ""
    for i, a in enumerate(ARTICLES):
        seals = "".join(seal(p["tool"]) for p in a["picks"][:4])
        cls = "label feature" if i < 2 else "label"
        cards += f"""
<a class="{cls}" href="/{a['slug']}.html"><div class="seals">{seals}</div>
<p class="kind">{a['category']}</p><h3>{a['h1']}</h3><p>{a['description']}</p><span class="open">Read the guide</span></a>"""
    body = f"""
<div class="wrap hero">
  <div>
    <h1>Every job has its perfect AI pairing.</h1>
    <p class="lede">A sommelier doesn't pour the most expensive bottle. They pour the right one. We compare AI tools the same way: by the job you need done.</p>
    <div class="hero-actions"><a class="btn" href="#guides">Browse the guides</a><a class="btn quiet" href="/about.html">How we pick</a></div>
  </div>
  <div class="carte">
    <h2>Tonight's pairings</h2>
    <p class="sub">What you need, and what to pour</p>
    <ol>{carte}</ol>
    <p class="foot">Tap a pairing to read why.</p>
  </div>
</div>
<section class="section" id="guides"><div class="wrap">
  <div class="section-head"><h2>The cellar</h2><p>In-depth comparisons for the jobs people actually hire AI for: voice, video, meetings and writing.</p></div>
  <div class="cellar">{cards}</div>
</div></section>
{journal}
<section class="section"><div class="wrap">{newsletter_block("home")}</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>How we choose a pairing</h2><p>The same three questions behind every recommendation.</p></div>
  <div class="method">
    <div><h3>What's the job?</h3><p>We start from the task, a voiceover, a meeting recap, a training video, never from the tool.</p></div>
    <div><h3>What does it really cost?</h3><p>Free plans, limits, and the plan most people end up needing.</p></div>
    <div><h3>Who is it for?</h3><p>A solo creator and a 500-person company rarely need the same tool.</p></div>
  </div>
</div></section>"""
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "name": NAME, "url": SITE + "/", "description": TAGLINE},
        {"@type": "Organization", "name": NAME, "url": SITE + "/", "logo": SITE + "/assets/logo.png",
         "sameAs": [u for _, u, _ in SOCIALS]}]}
    return page(f"{NAME}: AI tool comparisons, perfectly paired",
                "Honest, side-by-side comparisons of AI tools for voice, video, meetings and writing. Find the right AI tool for your job.",
                "", body, schema, og=og_image("home", "The Tool Sommelier", "Every job has its perfect AI pairing"))


# ---------------------------------------------------------------------------
# Blog ("The Journal")
# ---------------------------------------------------------------------------
GUIDES = {a["slug"]: a for a in ARTICLES}


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def tool_links(text):
    def rep(m):
        name, _, label = m.group(1).partition("|")
        return link(name.strip(), label.strip() or None)
    return re.sub(r"\{\{tool:([^}]+)\}\}", rep, text)


def post_card(p):
    seals = "".join(seal(t, 40) for t in p["tools"][:3])
    return (f'<a class="post-card" href="/blog/{p["slug"]}.html"><div class="seals">{seals}</div>'
            f'<p class="kind">{p["category"]} &middot; {fmt_date(p["date"])}</p><h3>{p["h1"]}</h3>'
            f'<p>{p["description"]}</p><span class="open">Read the note</span></a>')


def render_post(p):
    g = GUIDES[p["guide"]]
    dt = stamp("blog/" + p["slug"], p)
    dt["published"] = p["date"]
    if dt["modified"] < p["date"]:
        dt["modified"] = p["date"]
    og = og_image("blog-" + p["slug"], "The Journal · " + p["category"], p["h1"])
    others = [q for q in POSTS if q["slug"] != p["slug"]]
    others.sort(key=lambda q: q["date"], reverse=True)
    related = sorted(others, key=lambda q: q["guide"] != p["guide"])[:3]
    related_html = "".join(f'<li><a href="/blog/{q["slug"]}.html">{q["h1"]}</a></li>' for q in related)
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in p["faq"])
    seals = "".join(seal(t) for t in p["tools"][:4])
    body = f"""
<div class="wrap">
<div class="article-top">
  <div class="crumbs"><a href="/">Home</a> / <a href="/blog/">Journal</a></div>
  <h1>{p['h1']}</h1>
  <p class="standfirst">{p['description']}</p>
  <div class="seals">{seals}</div>
  <div class="meta">{p['category']}, {fmt_date(p['date'])}, {p['read']} min read</div>
</div>
</div>
<div class="paper simple"><div class="wrap"><div class="paper-grid">
<article>
<p class="notice">Contains affiliate links. <a href="/disclosure.html">Disclosure</a></p>
<div class="verdict"><h2>The short answer</h2>{tool_links(p['answer'])}</div>
{tool_links(p['body'])}
{f'<div class="faq"><h2 id="faq">FAQ</h2>{faq_html}</div>' if p['faq'] else ''}
<aside class="pairing-box">
  <p class="kind">The full pairing</p>
  <h2>{g['h1']}</h2>
  <p>{g['description']}</p>
  <a class="btn ink" href="/{g['slug']}.html">Read the guide</a>
</aside>
{newsletter_block()}
{f'<div class="more-notes"><h2>More from the Journal</h2><ul>{related_html}</ul></div>' if related_html else ''}
</article>
</div></div></div>"""
    url = f"{SITE}/blog/{p['slug']}.html"
    graph = [{"@type": "BlogPosting", "headline": p["h1"], "description": p["description"],
              "datePublished": dt["published"], "dateModified": dt["modified"],
              "author": {"@type": "Organization", "name": NAME},
              "publisher": {"@type": "Organization", "name": NAME, "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo.png"}},
              "mainEntityOfPage": url, "image": og},
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Journal", "item": SITE + "/blog/"},
                 {"@type": "ListItem", "position": 3, "name": p["h1"], "item": url}]}]
    if p["faq"]:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
            for q, a in p["faq"]]})
    return page(f"{p['title']} | {NAME}", p["description"], f"blog/{p['slug']}.html", body,
                {"@context": "https://schema.org", "@graph": graph}, og=og, ptype="article", dates=dt)


def render_blog_index():
    posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)
    cards = "".join(post_card(p) for p in posts)
    body = f"""
<div class="wrap">
<div class="article-top">
  <div class="crumbs"><a href="/">Home</a> / Journal</div>
  <h1>The Journal</h1>
  <p class="standfirst">Short, straight answers to the questions people ask before they pick an AI tool. Each note points to the full pairing guide.</p>
</div>
</div>
<section class="section journal"><div class="wrap"><div class="post-grid">{cards}</div></div></section>"""
    schema = {"@context": "https://schema.org", "@type": "Blog", "name": f"{NAME} Journal", "url": f"{SITE}/blog/"}
    return page(f"The Journal: quick answers about AI tools | {NAME}",
                "Short, honest answers to common questions about AI tools: free plans, pricing tiers, how-tos and comparisons for voice, video, meetings and writing.",
                "blog/", body, schema, og=og_image("blog", "The Journal", "Quick, honest answers about AI tools"))


def simple(title, slug_, description, inner):
    body = (f'<div class="wrap"><div class="article-top"><h1>{title}</h1></div></div>'
            f'<div class="paper simple"><div class="wrap"><div class="paper-grid"><article>{inner}</article></div></div></div>')
    return page(f"{title} | {NAME}", description, f"{slug_}.html", body, og=f"{SITE}/assets/og/home.png")


ABOUT = """
<p>The Tool Sommelier helps you choose AI software the way a good sommelier chooses a wine: by starting from what you need, not from what is loudest.</p>
<h2>Our method</h2>
<ul>
<li><strong>Job first.</strong> Every guide answers one concrete need: creating voiceovers, recording meetings, producing videos, writing content.</li>
<li><strong>Primary sources.</strong> We read each tool's official documentation, feature pages and pricing pages, and cross-check them with independent user reviews.</li>
<li><strong>Trade-offs, not hype.</strong> Every pick lists what it does well and where it falls short.</li>
<li><strong>Kept fresh.</strong> AI tools change monthly. Each guide shows the date of its last update, and we revise guides as plans and features change.</li>
</ul>
<h2>How we make money</h2>
<p>Some links are affiliate links. If you subscribe through them, the vendor may pay us a commission. You pay the same price. Commissions never decide a ranking: a tool with no affiliate program can, and does, rank first. See our <a href="/disclosure.html">affiliate disclosure</a>.</p>
<h2>Spotted an error?</h2>
<p>Prices and features move fast. We review every guide regularly. Spotted something out of date? Write to <a href="mailto:contact@toolsommelier.com">contact@toolsommelier.com</a>.</p>
"""

DISCLOSURE = """
<p>The Tool Sommelier is reader-supported. Some of the links on this website are affiliate links. If you click one and then buy or subscribe, we may receive a commission from the vendor, <strong>at no extra cost to you</strong>.</p>
<p>Affiliate links are marked with <code>rel="sponsored"</code> in our code, and every guide shows a short notice at the top.</p>
<p>Our recommendations are independent. We rank tools on fit, features, ease of use and value. Whether a tool pays a commission plays no part in its ranking.</p>
<p>Product names, logos and brands are property of their respective owners. Mentioning them does not imply endorsement by those companies.</p>
"""

PRIVACY = """
<p><em>Last updated: {date}</em></p>
<p>This website does not ask you to create an account and does not collect payment information. The only personal data we collect is your email address, and only if you choose to subscribe to our newsletter.</p>
<h2>Hosting</h2>
<p>The site is hosted by GitHub Pages (GitHub, Inc.). Like any web host, GitHub may log technical data such as your IP address for security purposes. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="nofollow noopener" target="_blank">GitHub's privacy statement</a>.</p>
<h2>Newsletter</h2>
<p>If you subscribe to The Weekly Pairing, your email address is collected and stored by our newsletter provider, beehiiv (Beehiiv Inc., United States), which sends the emails on our behalf. We use it only to send you the newsletter. The legal basis is your consent (GDPR art. 6(1)(a)): you confirm your subscription by clicking a link in a confirmation email (double opt-in), and you can unsubscribe at any time with the link at the bottom of every email, after which your address is no longer used for sending. beehiiv may record whether emails are opened and links clicked, to help us understand what readers find useful. See <a href="https://www.beehiiv.com/privacy" rel="nofollow noopener" target="_blank">beehiiv's privacy policy</a>. The signup form on our pages is loaded from beehiiv's servers.</p>
<h2>Audience measurement</h2>
<p>We count visits and clicks on outbound links with Umami Cloud (Umami Software, data hosted in the EU), a privacy-friendly analytics service that uses no cookies, does not track you across websites and does not collect personal data such as your IP address in a way that identifies you. We use these aggregated statistics only to understand which pages and recommendations are useful. See <a href="https://umami.is/privacy" rel="nofollow noopener" target="_blank">Umami's privacy policy</a>.</p>
<h2>Fonts</h2>
<p>Our typefaces are served by Bunny Fonts (BunnyWay d.o.o., EU), a privacy-focused font service that does not use cookies or track visitors.</p>
<h2>Cookies</h2>
<p>We do not set advertising or tracking cookies. When you click an outbound link to a software vendor, that vendor's own website may set cookies (including affiliate tracking cookies) under its own privacy policy.</p>
<h2>Your rights</h2>
<p>Under the GDPR you have the right to access, correct and delete personal data about you. For newsletter subscribers, you can unsubscribe at any time or write to <a href="mailto:contact@toolsommelier.com">contact@toolsommelier.com</a> to have your address deleted. See our <a href="/legal.html">legal notice</a> for publisher and hosting details.</p>
"""

LEGAL = """
<p><strong>Publisher:</strong> this website is published by a private individual (non-professional publisher) who, in accordance with Article 6-III-2 of the French law n°2004-575 of 21 June 2004 (LCEN), has chosen not to disclose their identity publicly. Their identification details have been provided to the hosting provider named below.<br>
<strong>Contact:</strong> <a href="mailto:contact@toolsommelier.com">contact@toolsommelier.com</a></p>
<p><strong>Hosting:</strong> GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States. <a href="https://github.com" rel="nofollow noopener" target="_blank">github.com</a></p>
<p><strong>Domain registrar:</strong> IONOS SARL, France.</p>
<p>All content on this website is provided for general information. Prices and features of third-party tools may change without notice; always check the vendor's official website before buying.</p>
"""


def main():
    out = ROOT
    pages = {"index.html": render_home()}
    for a in ARTICLES:
        pages[f"{a['slug']}.html"] = render_article(a)
    pages["about.html"] = simple("How we pick AI tools", "about", "Our method for comparing and ranking AI tools.", ABOUT)
    pages["disclosure.html"] = simple("Affiliate disclosure", "disclosure", "How The Tool Sommelier earns money.", DISCLOSURE)
    pages["privacy.html"] = simple("Privacy policy", "privacy", "Privacy policy of The Tool Sommelier.", PRIVACY.format(date=TODAY.strftime('%B %d, %Y')))
    pages["legal.html"] = simple("Legal notice", "legal", "Legal notice (mentions légales) of The Tool Sommelier.", LEGAL)
    pages["404.html"] = simple("Page not found", "404", "Page not found.", '<p>This bottle is not in our cellar. <a href="/">Back to the guides →</a></p>')
    pages["blog/index.html"] = render_blog_index()
    for p in POSTS:
        assert p["guide"] in GUIDES, f"unknown guide {p['guide']} in post {p['slug']}"
        pages[f"blog/{p['slug']}.html"] = render_post(p)
    (out / "blog").mkdir(exist_ok=True)
    for name, content in pages.items():
        (out / name).write_text(content, encoding="utf-8")

    def lm(u):
        if u.startswith("blog/") and u.endswith(".html"):
            return DATES["blog/" + u[5:-5]]["modified"]
        if u.endswith(".html") and u[:-5] in DATES:
            return DATES[u[:-5]]["modified"]
        return None
    content_urls = [f"{a['slug']}.html" for a in ARTICLES] + [f"blog/{p['slug']}.html" for p in POSTS]
    latest = max(lm(u) for u in content_urls)
    latest_post = max([lm(f"blog/{p['slug']}.html") for p in POSTS] or [latest])
    urls = [("", latest)] + [(u, lm(u)) for u in content_urls[:len(ARTICLES)]] + [("blog/", latest_post)] + \
           [(u, lm(u)) for u in content_urls[len(ARTICLES):]] + [("about.html", None), ("disclosure.html", None)]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"<url><loc>{SITE}/{u}</loc>" + (f"<lastmod>{d}</lastmod>" if d else "") + "</url>" for u, d in urls]
    sitemap.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    # RSS feed of the Journal (helps discovery by aggregators and AI crawlers)
    def rfc(iso):
        return datetime.datetime.combine(datetime.date.fromisoformat(iso), datetime.time(8)).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = "".join(
        f"<item><title>{html.escape(p['h1'])}</title><link>{SITE}/blog/{p['slug']}.html</link>"
        f"<guid>{SITE}/blog/{p['slug']}.html</guid><pubDate>{rfc(p['date'])}</pubDate>"
        f"<description>{html.escape(p['description'])}</description></item>"
        for p in sorted(POSTS, key=lambda p: p["date"], reverse=True)[:30])
    (out / "blog" / "feed.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{NAME} Journal</title>'
        f"<link>{SITE}/blog/</link><description>Quick, honest answers about AI tools.</description>"
        f"<language>en</language>{items}</channel></rss>", encoding="utf-8")

    # llms.txt: a plain map of the site for AI assistants and answer engines
    llms = [f"# {NAME}", "", f"> {TAGLINE} Independent comparisons of AI software (voice, video, meetings, writing), organized by the job you need done.", "",
            "## Guides"] + [f"- [{a['h1']}]({SITE}/{a['slug']}.html): {html.unescape(a['description'])}" for a in ARTICLES] + \
           ["", "## Journal (quick answers)"] + [f"- [{p['h1']}]({SITE}/blog/{p['slug']}.html): {html.unescape(p['description'])}"
                                                for p in sorted(POSTS, key=lambda p: p["date"], reverse=True)] + \
           ["", "## About", f"- [How we pick]({SITE}/about.html): our method", f"- [Affiliate disclosure]({SITE}/disclosure.html)"]
    (out / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (out / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    DATES_FILE.write_text(json.dumps(DATES, indent=1, sort_keys=True), encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (out / "CNAME").write_text("toolsommelier.com\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    # Google Search Console ownership file: never delete
    (out / "googlebe370e82df618218.html").write_text("google-site-verification: googlebe370e82df618218.html", encoding="utf-8")
    print(f"Built {len(pages)} pages.")


if __name__ == "__main__":
    main()
