#!/usr/bin/env python3
"""Static site generator for The Tool Sommelier.

Usage:  python3 build.py
Edit LINKS below to swap official URLs for affiliate links: every page updates.
Articles live in content.py.
"""
import datetime, html, json, pathlib

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
    "ElevenLabs":  {"url": "https://elevenlabs.io",   "aff": False},
    "Murf AI":     {"url": "https://murf.ai",         "aff": False},
    "Descript":    {"url": "https://www.descript.com","aff": False},
    "Speechify":   {"url": "https://speechify.com",   "aff": False},
    "Synthesia":   {"url": "https://www.synthesia.io","aff": False},
    "HeyGen":      {"url": "https://www.heygen.com",  "aff": False},
    "Pictory":     {"url": "https://pictory.ai",      "aff": False},
    "Runway":      {"url": "https://runwayml.com",    "aff": False},
    "Otter.ai":    {"url": "https://otter.ai",        "aff": False},
    "Fireflies.ai":{"url": "https://fireflies.ai",    "aff": False},
    "Fathom":      {"url": "https://fathom.video",    "aff": False},
    "tl;dv":       {"url": "https://tldv.io",         "aff": False},
    "Jasper":      {"url": "https://www.jasper.ai",   "aff": False},
    "Copy.ai":     {"url": "https://www.copy.ai",     "aff": False},
    "Writesonic":  {"url": "https://writesonic.com",  "aff": False},
    "Grammarly":   {"url": "https://www.grammarly.com","aff": False},
}

LOGO_SVG = ('<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true">'
            '<path d="M9 3h14c0 7-2.6 11.5-7 12.3C11.6 14.5 9 10 9 3z" fill="#6b1d2a"/>'
            '<path d="M16 15.3V26M10.5 28.5h11" stroke="#1f1a17" stroke-width="2" stroke-linecap="round"/>'
            '<circle cx="16" cy="8" r="1.8" fill="#c9a24a"/><path d="M12.5 8h1.7M17.8 8h1.7" stroke="#c9a24a" stroke-width="1.3"/>'
            '</svg>')
FAVICON = "data:image/svg+xml," + LOGO_SVG.replace('"', "'").replace("#", "%23").replace('aria-hidden=\'true\'', "xmlns='http://www.w3.org/2000/svg'")


def link(name, text=None, cls=None):
    """Outbound link to a tool, with the right rel attributes."""
    data = LINKS[name]
    rel = "sponsored nofollow noopener" if data["aff"] else "nofollow noopener"
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{data["url"]}" target="_blank" rel="{rel}"{c}>{html.escape(text or name)}</a>'


def page(title, description, path, body, schema=None):
    canonical = f"{SITE}/{path}".rstrip("/") + ("/" if path in ("",) else "")
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head>
<body>
<header class="site-header"><div class="wrap">
  <a class="logo" href="/">{LOGO_SVG}<span>The Tool <b>Sommelier</b></span></a>
  <nav><a href="/#guides">Guides</a><a href="/about.html" class="hide-sm">How we pick</a><a href="/disclosure.html">Disclosure</a></nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
  <div class="cols">
    <div><strong>{NAME}</strong><br>{TAGLINE}</div>
    <div><a href="/about.html">How we pick</a><br><a href="/disclosure.html">Affiliate disclosure</a></div>
    <div><a href="/privacy.html">Privacy</a><br><a href="/legal.html">Legal notice</a></div>
  </div>
  <p class="small">Some links on this site are affiliate links: if you buy through them we may earn a commission, at no extra cost to you. It never changes our rankings. Product names and logos belong to their respective owners. &copy; {TODAY.year} {NAME}.</p>
</div></footer>
</body>
</html>
"""


def render_article(a):
    picks_html = ""
    for i, p in enumerate(a["picks"], 1):
        pros = "".join(f"<li>{x}</li>" for x in p["pros"])
        cons = "".join(f"<li>{x}</li>" for x in p["cons"])
        picks_html += f"""
<div class="pick" id="{p['tool'].lower().replace('.', '').replace(';', '').replace(' ', '-')}">
  <div class="rank">#{i} · {p['label']}</div>
  <h3>{p['tool']}</h3>
  <p class="best-for"><strong>Best for:</strong> {p['best_for']}</p>
  <p class="tasting">Tasting note: {p['note']}</p>
  <p>{p['body']}</p>
  <div class="pros-cons"><div><strong>Why we like it</strong><ul>{pros}</ul></div>
  <div><strong>Watch out for</strong><ul>{cons}</ul></div></div>
  {link(p['tool'], f"Try {p['tool']} →", "btn small")}
</div>"""

    rows = "".join(
        f"<tr><td><strong>{p['tool']}</strong></td><td>{p['best_for']}</td><td>{p['free']}</td><td>{link(p['tool'], 'Visit site')}</td></tr>"
        for p in a["picks"])
    table = f"""<div class="table-scroll"><table class="compare">
<tr><th>Tool</th><th>Best for</th><th>Free option</th><th></th></tr>{rows}</table></div>
<p class="meta">Plans and prices change often. Always check the official pricing page before you buy.</p>"""

    faq_html = "".join(f"<h3>{q}</h3><p>{ans}</p>" for q, ans in a["faq"])
    sections = "".join(f"<h2>{h}</h2>{b}" for h, b in a.get("extra", []))

    body = f"""
<div class="wrap narrow">
<div class="article-head">
  <div class="crumbs"><a href="/">Home</a> › <a href="/#guides">Guides</a></div>
  <h1>{a['h1']}</h1>
  <div class="meta">Updated {TODAY.strftime('%B %Y')} · {a['read']} min read</div>
  <div class="disclosure-box">We may earn a commission if you sign up through our links, at no extra cost to you. <a href="/disclosure.html">Learn more</a>.</div>
</div>
<article>
{a['intro']}
<div class="verdict"><h2>The short answer</h2>{a['verdict']}</div>
<h2>At a glance</h2>
{table}
<h2>Our picks, in detail</h2>
{picks_html}
{sections}
<h2>How to choose</h2>
{a['how_to_choose']}
<div class="faq"><h2>FAQ</h2>{faq_html}</div>
<p class="meta">Our rankings are based on each tool's official documentation, published plans and independent user reviews. <a href="/about.html">How we pick</a>.</p>
</article>
</div>"""

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


def render_home():
    cards = "".join(f"""
<a class="card" href="/{a['slug']}.html"><div class="tag">{a['category']}</div>
<h3>{a['h1']}</h3><p>{a['description']}</p><span class="more">Read the guide →</span></a>"""
                    for a in ARTICLES)
    body = f"""
<div class="wrap hero">
  <span class="eyebrow">AI tools, pairing advice</span>
  <h1>Find the AI tool that <em>fits your job</em>, not the hype.</h1>
  <p>A sommelier doesn't pour you the most expensive bottle. They pour the right one. We do the same with AI tools: clear comparisons, honest trade-offs, no fluff.</p>
  <a class="btn" href="#guides">Browse the guides</a>
</div>
<section id="guides"><div class="wrap">
  <h2 class="section-title">Pairing guides</h2>
  <p class="section-sub">Side-by-side comparisons for the jobs people actually hire AI for.</p>
  <div class="grid">{cards}</div>
</div></section>
<section><div class="wrap">
  <h2 class="section-title">How we pick</h2>
  <p class="section-sub">Three questions, every time.</p>
  <div class="steps">
    <div class="step"><strong>1. What's the job?</strong><span>We start from the task (a voiceover, a meeting recap, a training video), not from the tool.</span></div>
    <div class="step"><strong>2. What does it really cost?</strong><span>Free plans, limits, and the plan most people actually need.</span></div>
    <div class="step"><strong>3. Who is it for?</strong><span>A solo creator and a 500-person company rarely need the same tool.</span></div>
  </div>
  <p style="margin-top:22px"><a href="/about.html">Read our full method →</a></p>
</div></section>"""
    schema = {"@context": "https://schema.org", "@type": "WebSite", "name": NAME, "url": SITE + "/",
              "description": TAGLINE}
    return page(f"{NAME}: AI tool comparisons, perfectly paired",
                "Honest, side-by-side comparisons of AI tools for voice, video, meetings and writing. Find the right AI tool for your job.",
                "", body, schema)


def simple(title, slug, description, inner):
    body = f'<div class="wrap narrow"><div class="article-head"><h1>{title}</h1></div><article>{inner}</article></div>'
    return page(f"{title} | {NAME}", description, f"{slug}.html", body)


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
