#!/usr/bin/env python3
"""
Generates the daily Tech / AI / Product Management digest — for free.

No API key, no billing. This pulls straight from each source's RSS/Atom
feed using feedparser, picks the most recent items, and renders them into
the HTML template. It does NOT summarize or filter with AI — you get real
headlines and links, written by the original publications.

If you later want AI-written summaries and smarter filtering, that's the
paid version of this script (same repo structure, swaps this file for one
that calls the Claude API). This free version is a genuinely solid daily
digest on its own.
"""

import os
from datetime import datetime, timezone

import feedparser

# ---- Your source list ---------------------------------------------------
# Each entry is (display name, RSS/Atom feed URL). Verify these still work
# occasionally — feed URLs do change or get discontinued sometimes.
# Add or remove freely; most blogs and news sites publish a feed even if
# it's not linked anywhere obvious (try adding /feed or /rss to the URL).
SOURCES = {
    "tech": [
        ("The Verge", "https://www.theverge.com/rss/index.xml"),
        ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
        ("TechCrunch", "https://techcrunch.com/feed/"),
        ("Hacker News (front page)", "https://hnrss.org/frontpage"),
    ],
    "ai": [
        ("Simon Willison's blog", "https://simonwillison.net/atom/everything/"),
        ("OpenAI blog", "https://openai.com/blog/rss.xml"),
        ("Hacker News (AI tag)", "https://hnrss.org/newest?q=AI"),
    ],
    "pm": [
        ("Lenny's Newsletter", "https://www.lennysnewsletter.com/feed"),
        ("Product Hunt", "https://www.producthunt.com/feed"),
        ("SVPG", "https://svpg.com/feed/"),
    ],
}

ENTRIES_PER_CATEGORY = 5


def fetch_category(feeds):
    """Pull entries from each feed in this category, merge, sort by date."""
    all_entries = []
    for source_name, feed_url in feeds:
        try:
            parsed = feedparser.parse(feed_url)
            for entry in parsed.entries[:5]:
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                all_entries.append({
                    "title": entry.get("title", "Untitled"),
                    "url": entry.get("link", "#"),
                    "source": source_name,
                    "published_struct": published,
                    "date_display": entry.get("published", entry.get("updated", "")),
                })
        except Exception as e:
            print(f"WARNING: could not fetch {source_name} ({feed_url}): {e}")

    # Sort newest first when we have a parseable date, otherwise keep as-is
    all_entries.sort(
        key=lambda e: e["published_struct"] or datetime.min.timetuple(),
        reverse=True,
    )
    return all_entries[:ENTRIES_PER_CATEGORY]


def render_entries(items):
    if not items:
        return '<p style="color:var(--slate);font-size:14px;">No items retrieved — check the Action logs, a feed URL may have changed.</p>'
    html = []
    for item in items:
        # Trim overly long dates like "Wed, 25 Sep 2026 07:00:00 +0000" to something shorter
        date_short = item["date_display"][:16] if item["date_display"] else ""
        html.append(f'''      <article class="entry">
        <h3><a href="{item['url']}" target="_blank" rel="noopener">{item['title']}</a></h3>
        <div class="meta"><span class="src">{item['source']}</span><span>&middot;</span><span>{date_short}</span></div>
      </article>''')
    return "\n".join(html)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "..", "template.html")
    output_path = os.path.join(script_dir, "..", "docs", "index.html")

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    tech_items = fetch_category(SOURCES["tech"])
    ai_items = fetch_category(SOURCES["ai"])
    pm_items = fetch_category(SOURCES["pm"])

    html = template
    html = html.replace("{{TECH_ENTRIES}}", render_entries(tech_items))
    html = html.replace("{{AI_ENTRIES}}", render_entries(ai_items))
    html = html.replace("{{PM_ENTRIES}}", render_entries(pm_items))
    html = html.replace("{{TECH_COUNT}}", str(len(tech_items)))
    html = html.replace("{{AI_COUNT}}", str(len(ai_items)))
    html = html.replace("{{PM_COUNT}}", str(len(pm_items)))
    html = html.replace(
        "{{GENERATED_AT}}",
        datetime.now(timezone.utc).strftime("%A, %B %d, %Y at %H:%M UTC"),
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
