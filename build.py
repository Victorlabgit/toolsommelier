#!/usr/bin/env python3
"""Static site generator for The Tool Sommelier.

Usage:  python3 build.py
Edit LINKS below to swap official URLs for affiliate links: every page updates.
Articles live in content.py.
"""
import datetime, html, json, pathlib, re

from content import ARTICLES

SITE = "https://toolsommelier.com"
NAME = "The Tool Sommelier"
TAGLINE = "The right AI tool, perfectly paired to your job."
TODAY = datetime.date.today()
ROOT = pathlib.Path(__file__).parent

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
    "Pictory":     {"url": "https://pictory.ai",      "aff": False},
    "Runway":      {"url": "https://runwayml.com",    "aff": False},
    "Otter.ai":    {"url": "https://otter.ai",        "aff": False},
    "Fireflies.ai":{"url": "https://fireflies.ai/?fpr=victor-4901be", "aff": True},
    "Fathom":      {"url": "https://fathom.video",    "aff": False},
    "tl;dv":       {"url": "https://tldv.cello.so/XeSTTwlN4cX", "aff": True},
    "Jasper":      {"url": "https://www.jasper.ai",   "aff": False},
    "Copy.ai":     {"url": "https://www.copy.ai",     "aff": False},
    "Writesonic":  {"url": "https://writesonic.com",  "aff": False},
    "Grammarly":   {"url": "https://www.grammarly.com","aff": False},
}

LOGO_MARK = '<g stroke="#d8bf8a" stroke-width="10"><line x1="170" y1="170" x2="256" y2="140"/><line x1="256" y1="140" x2="342" y2="170"/><line x1="170" y1="170" x2="256" y2="256"/><line x1="342" y1="170" x2="256" y2="256"/><line x1="256" y1="256" x2="170" y2="342"/><line x1="256" y1="256" x2="342" y2="342"/><line x1="170" y1="342" x2="256" y2="372"/><line x1="342" y1="342" x2="256" y2="372"/></g><g fill="#150c0f" stroke="#d8bf8a" stroke-width="10"><circle cx="170" cy="170" r="24"/><circle cx="342" cy="170" r="24"/><circle cx="170" cy="342" r="24"/><circle cx="342" cy="342" r="24"/><circle cx="256" cy="140" r="18"/><circle cx="256" cy="372" r="18"/></g><circle cx="256" cy="256" r="38" fill="#9a2a3b" stroke="#d8bf8a" stroke-width="10"/>'
LOGO_SVG = '<svg width="34" height="34" viewBox="110 90 292 332" aria-hidden="true">' + LOGO_MARK + '</svg>'
FAVICON = "data:image/svg+xml," + ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'><rect width='512' height='512' rx='112' fill='%23150c0f'/>" + LOGO_MARK.replace('"', "'").replace('#', '%23') + '</svg>')
FONTS = '<link rel="preconnect" href="https://fonts.bunny.net"><link rel="stylesheet" href="https://fonts.bunny.net/css?family=cormorant-garamond:400,400i,500,600|manrope:400,500,600&display=swap">'

# Monogram seals stand in for vendor logos (we do not reproduce trademarks).
SEAL_COLORS = ["#7b1e2c", "#2f4a3a", "#3b3561", "#6a4a1e", "#24485e", "#5b2448", "#4a3b2a", "#2d4f4f"]


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
    return f'<a href="{data["url"]}" target="_blank" rel="{rel}"{c}>{html.escape(text or name)}</a>'


def page(title, description, path, body, schema=None):
    canonical = f"{SITE}/{path}"
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
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/linkedin-banner.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
{FONTS}
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="logo" href="/">{LOGO_SVG}<span class="logo-word">The Tool <i>Sommelier</i></span></a>
  <nav class="main"><a href="/#guides">Guides</a><a href="/about.html" class="hide-sm">How we pick</a><a href="/disclosure.html">Disclosure</a></nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <div class="cols">
    <div><p class="brand">The Tool Sommelier</p><p>{TAGLINE}<br>Independent comparisons of AI software, written for people who have a job to do.</p></div>
    <div><a href="/#guides">All guides</a><a href="/about.html">How we pick</a><a href="mailto:contact@toolsommelier.com">Contact</a></div>
    <div><a href="/disclosure.html">Affiliate disclosure</a><a href="/privacy.html">Privacy</a><a href="/legal.html">Legal notice</a></div>
  </div>
  <p class="fine">Some links on this site are affiliate links: if you subscribe through them we may earn a commission, at no extra cost to you. It never changes our rankings. Product names belong to their respective owners; ElevenLabs is a trademark of Eleven Labs Inc. &copy; {TODAY.year} {NAME}.</p>
</div></footer>
</body>
</html>
"""


def render_article(a):
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
  <div class="meta">Updated {TODAY.strftime('%B %Y')}, {a['read']} min read</div>
</div>
</div>
<div class="paper"><div class="wrap"><div class="paper-grid">
<nav class="toc" aria-label="On this page"><strong>On this page</strong>{''.join(toc)}</nav>
<article>
<p class="notice">We may earn a commission if you sign up through our links, at no extra cost to you. <a href="/disclosure.html">How this works</a>.</p>
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
</article>
</div></div></div>"""

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "headline": a["h1"], "description": a["description"],
             "dateModified": TODAY.isoformat(), "author": {"@type": "Organization", "name": NAME},
             "publisher": {"@type": "Organization", "name": NAME}, "mainEntityOfPage": f"{SITE}/{a['slug']}.html"},
            {"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(ans)}}
                for q, ans in a["faq"]]},
        ],
    }
    return page(a["title"], a["description"], f"{a['slug']}.html", body, schema)


CARTE = [
    ("A voiceover that sounds human", "ElevenLabs", "best-ai-voice-generators.html#elevenlabs"),
    ("Training videos, no camera", "Synthesia", "best-ai-video-generators.html#synthesia"),
    ("Your face, in any language", "HeyGen", "synthesia-vs-heygen.html#heygen"),
    ("Meeting notes for free", "Fathom", "best-ai-meeting-note-takers.html#fathom"),
    ("Edit a podcast like a doc", "Descript", "best-ai-voice-generators.html#descript"),
    ("On-brand marketing copy", "Jasper", "best-ai-writing-tools.html#jasper"),
]


def render_home():
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
<section class="section"><div class="wrap">
  <div class="section-head"><h2>How we choose a pairing</h2><p>The same three questions behind every recommendation.</p></div>
  <div class="method">
    <div><h3>What's the job?</h3><p>We start from the task, a voiceover, a meeting recap, a training video, never from the tool.</p></div>
    <div><h3>What does it really cost?</h3><p>Free plans, limits, and the plan most people end up needing.</p></div>
    <div><h3>Who is it for?</h3><p>A solo creator and a 500-person company rarely need the same tool.</p></div>
  </div>
</div></section>"""
    schema = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/",
              "description": TAGLINE}
    return page(f"{NAME}: AI tool comparisons, perfectly paired",
                "Honest, side-by-side comparisons of AI tools for voice, video, meetings and writing. Find the right AI tool for your job.",
                "", body, schema)


def simple(title, slug_, description, inner):
    body = (f'<div class="wrap"><div class="article-top"><h1>{title}</h1></div></div>'
            f'<div class="paper simple"><div class="wrap"><div class="paper-grid"><article>{inner}</article></div></div></div>')
    return page(f"{title} | {NAME}", description, f"{slug_}.html", body)


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
<p>This website does not ask you to create an account and does not collect your name, email address or payment information.</p>
<h2>Hosting</h2>
<p>The site is hosted by GitHub Pages (GitHub, Inc.). Like any web host, GitHub may log technical data such as your IP address for security purposes. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="nofollow noopener" target="_blank">GitHub's privacy statement</a>.</p>
<h2>Fonts</h2>
<p>Our typefaces are served by Bunny Fonts (BunnyWay d.o.o., EU), a privacy-focused font service that does not use cookies or track visitors.</p>
<h2>Cookies</h2>
<p>We do not set advertising or tracking cookies. When you click an outbound link to a software vendor, that vendor's own website may set cookies (including affiliate tracking cookies) under its own privacy policy.</p>
<h2>Your rights</h2>
<p>Under the GDPR you have the right to access, correct and delete personal data about you. Since we do not collect personal data ourselves, there is usually nothing to request; see our <a href="/legal.html">legal notice</a> for publisher and hosting details.</p>
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
    for name, content in pages.items():
        (out / name).write_text(content, encoding="utf-8")

    urls = [""] + [f"{a['slug']}.html" for a in ARTICLES] + ["about.html", "disclosure.html"]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"<url><loc>{SITE}/{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (out / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (out / "CNAME").write_text("toolsommelier.com\n", encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(pages)} pages.")


if __name__ == "__main__":
    main()
