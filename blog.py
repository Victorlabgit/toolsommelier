"""Blog posts ("The Journal") for The Tool Sommelier.

Each post answers one precise question people type into Google, then sends
readers to the related in-depth guide. Newest posts go at the TOP of POSTS.

Fields:
  slug         URL: /blog/<slug>.html (lowercase, hyphens)
  title        <title> tag, keyword first, under ~60 characters
  h1           visible headline
  description  meta description, 140-160 characters
  date         publication date, ISO format "YYYY-MM-DD"
  category     Voice / Video / Meetings / Writing / ...
  read         minutes to read
  guide        slug of the related guide in content.py
  tools        tool names (keys of LINKS in build.py) shown as seals
  answer       the short answer, 2-3 sentences (shown in a highlighted box)
  body         HTML. Use {{tool:Name}} or {{tool:Name|link text}} for an
               outbound tool link (affiliate when available).
  faq          list of (question, answer) pairs, can be empty
"""

POSTS = [
{
"slug": "is-fireflies-ai-free",
"title": "Is Fireflies.ai Free? What the Free Plan Really Includes",
"h1": "Is Fireflies.ai free? What the free plan really includes",
"description": "Yes, Fireflies.ai has a free-forever plan with unlimited transcription. Here is what it includes, where the limits are, and when it is worth upgrading.",
"date": "2026-11-26",
"category": "Meetings",
"read": 4,
"guide": "best-ai-meeting-note-takers",
"tools": ["Fireflies.ai", "Fathom", "tl;dv"],
"answer": "<p>Yes. Fireflies.ai offers a free-forever plan, not a time-limited trial. It transcribes your Zoom, Google Meet and Teams calls without a cap on transcription, but storage, AI features and downloads are limited, so it suits occasional meetings better than daily use.</p>",
"body": """
<p>Fireflies.ai is one of the best-known AI note takers: it joins your calls, records them, writes a transcript and summarizes what was said. The question most people ask before installing it is simple: do you have to pay? Here is what the free plan gives you, based on Fireflies' official pricing page at the time of writing.</p>

<h2>What you get on the free plan</h2>
<ul>
<li><strong>Unlimited transcription</strong> of your meetings (the pricing page marks this with a footnote, so check the fine print for fair-use rules).</li>
<li><strong>Works where you meet:</strong> Zoom, Google Meet and Microsoft Teams, plus file uploads.</li>
<li><strong>100+ languages</strong> for transcription.</li>
<li><strong>Search and AskFred:</strong> you can search your meetings and ask Fireflies' AI assistant questions about them.</li>
<li><strong>Desktop, mobile and Chrome</strong> access.</li>
</ul>

<h2>Where the free plan stops</h2>
<p>The limits are less about transcription and more about what you can keep and do afterwards:</p>
<ul>
<li><strong>Storage is capped.</strong> The free plan stores a limited number of meeting minutes in total (not per month), so older meetings eventually have to go. Paid plans raise or remove this cap.</li>
<li><strong>AI summaries and AI credits are limited.</strong> You get a small allowance of AI credits for the advanced AI features.</li>
<li><strong>No video recording and no downloads</strong> of transcripts or recordings on the free tier.</li>
<li><strong>Shorter recordings</strong> than on the higher plans.</li>
</ul>
<p>Numbers change regularly, so check the pricing page on the official {{tool:Fireflies.ai|Fireflies website}} for the current storage and credit figures before you decide.</p>

<h2>When the free plan is enough</h2>
<p>If you have a handful of calls a week, mostly need a searchable transcript and don't need to download files, the free plan does the job. It is also a good way to see whether your team actually reads AI meeting notes before you pay for seats.</p>

<h2>When it is worth upgrading</h2>
<p>Upgrade when you hit the storage cap, when you need the full AI summaries on every call, or when notes must flow into your CRM and project tools automatically. That last point is where Fireflies shines for sales and customer teams, which is why we pair it with them in our <a href="/best-ai-meeting-note-takers.html">guide to the best AI meeting note takers</a>.</p>

<h2>Free alternatives worth a look</h2>
<p>If the storage limit bothers you, two other note takers are known for generous free plans: {{tool:Fathom}}, often cited as the most generous free option for individuals, and {{tool:tl;dv}}, popular for recording and clipping Zoom and Google Meet calls. We compare all of them side by side in the <a href="/best-ai-meeting-note-takers.html">full guide</a>.</p>
""",
"faq": [
("Is Fireflies.ai free forever?", "Yes. Fireflies presents its free tier as a free-forever plan rather than a timed trial. You can keep using it without paying, within its limits."),
("Does the Fireflies free plan limit transcription minutes?", "Fireflies advertises unlimited transcription on the free plan. The main limit is how many meeting minutes you can store in total."),
("Can I download transcripts on the Fireflies free plan?", "No. According to Fireflies' pricing page, downloading transcripts and recordings requires a paid plan."),
("Which is better for free: Fireflies or Fathom?", "Fathom is often considered more generous for individuals on a free plan, while Fireflies is stronger when notes need to sync into CRMs and team tools on a paid plan."),
],
},
]
