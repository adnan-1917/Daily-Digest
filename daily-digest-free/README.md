# Daily Wire — Tech, AI & PM Digest (Free Version)

A self-updating news page. A GitHub Action runs every morning, pulls the
latest items from each source's RSS feed, and republishes the page via
GitHub Pages — completely free, no API key, no billing.

**What's different from the AI-summarized version:** no one-line summaries,
no smart filtering. You get real headlines and links straight from each
publication, sorted by recency. Still genuinely useful for a daily scan —
you're just doing the "is this worth reading" judgment yourself instead of
having it pre-digested.

## One-time setup

1. **Create a new GitHub repo** and add these files (drag-and-drop upload
   through the GitHub web UI works fine, or `git push` if you're
   comfortable with that).

2. **Enable GitHub Pages**
   - In your repo: Settings → Pages.
   - Under "Build and deployment", set Source to **GitHub Actions**.

3. **Run it once manually to check it works**
   - Go to the "Actions" tab → "Daily Digest (Free)" → "Run workflow".
   - If it succeeds, your page is live at
     `https://<your-username>.github.io/<repo-name>/`.

That's it. From now on it updates automatically every day at 07:00 UTC.

## Customizing sources

Open `scripts/generate_digest.py` and edit the `SOURCES` dictionary. Each
entry is `(display name, feed URL)`. Most blogs and news sites have an RSS
feed even if it's not obviously linked — common patterns to try:
`example.com/feed`, `example.com/rss`, `example.com/feed.xml`,
`example.com/atom.xml`. You can also find a site's feed by searching
"[site name] RSS feed".

A few of the feeds I've pre-filled (Lenny's Newsletter, SVPG, Product Hunt)
are common addresses for those sites but I have not verified every one
still resolves — if a feed comes back empty in the Action logs, that URL
has likely changed; search for the current one and swap it in.

Handy feed-finding tools if a site doesn't advertise one directly:
- https://hnrss.org — turns any Hacker News search into an RSS feed
  (already used for AI-tagged Hacker News posts above)
- Most Substack newsletters (like Lenny's) publish a feed at
  `[newsletter-name].substack.com/feed`

## If a run fails or a column comes up empty

Check the Actions tab → click the failed/empty run → expand the
"Generate today's digest" step. It prints a warning for any feed it
couldn't fetch, which is almost always a changed or dead URL — just
find the new one and edit `SOURCES`.

## Upgrading later

If you ever do want AI-written summaries and real filtering criteria
(not just raw headlines), the paid version of this project reuses the
exact same repo structure — it's a one-file swap (`generate_digest.py`)
plus an `ANTHROPIC_API_KEY` secret. Nothing here needs to be rebuilt from
scratch to add that later.
