# Research Playbook

Detailed tactics per signal source. Each source should produce candidates in this shape:

```
- topic: <short topic name>
  signal: <what was observed>
  evidence: <link + number, e.g. "youtube.com/watch?v=... — 210K views on a 12K-sub channel, posted 3 weeks ago">
```

## Source 1: Dan's own channel data (personal MCP)

Tools are on Dan's personal MCP server (danvega.dev); names end in:
`youtube-get-channel-stats`, `youtube-get-top-videos`, `youtube-get-latest-videos`, `youtube-search-videos-by-topic`, `blog-search-posts-by-keyword`, `blog-get-latest-posts`, `newsletter-search-posts-by-keyword`.

What to extract:

1. Call `youtube-get-channel-stats` for the channel average views/video. Call `youtube-get-top-videos` with `timeRange: "year"` and `"all"`.
2. **Over-performers**: videos above ~2x channel average. What do they share? (Topic, format, title pattern.) Those patterns seed new ideas.
3. **Refresh candidates**: old top videos on topics with a new version out (e.g., a hit Spring Boot 3 video → Spring Boot 4 remake).
4. **Sequel candidates**: recent strong videos with an obvious "part 2" (intro did well → deep dive, build did well → deploy/test/scale it).
5. **Cross-media signals**: blog/newsletter posts with strong engagement that never became videos.

If the MCP tools aren't available, skip — don't guess his stats.

## Source 2: YouTube outlier scan

Goal: find videos where views ≫ what the channel normally gets. Views ÷ channel-average (or views ÷ subscribers) is the outlier score; anything above ~3x is interesting, above ~10x on a small channel is a strong topic signal.

Method (no YouTube API needed):

- Web-search with `site:youtube.com` plus niche terms: `site:youtube.com spring boot <current year>`, `site:youtube.com java virtual threads`, `site:youtube.com spring ai tutorial`, `site:youtube.com claude code java`, etc. Prefer results from the last 3–6 months.
- Check videos published recently by channels in the niche (below). For each promising video, note views, channel size, and age. A YouTube search-results or channel page may be JS-rendered; if a fetch returns an empty shell, use browser tools or rely on the web-search snippet data.
- Look at what formats the outliers use (build-along, "explained", versus/comparison, hot take on news) — format is part of the signal.

Channels to scan (Java/Spring/AI-dev niche, mix of sizes):
Amigoscode, Java Brains, Coding with John, Marco Behler / Marco Codes, Telusko, Bouali Ali, Devtiro, SpringDeveloper (Josh Long), Dan Vega (self-compare), JetBrains Java, ByteByteGo, Fireship (format inspiration, not topic), ThePrimeagen (dev-tool discourse), AI-coding channels covering Claude Code / Cursor / Copilot.

Also scan adjacent winners: a topic blowing up in the Python/JS world ("build an MCP server", "agents explained") with no good Java equivalent yet = prime differentiation play.

## Source 3: Community and web trends

- **Hacker News**: search hn.algolia.com for last-month top stories matching java, spring, jvm, ai coding, llm, agents. Front-page discussion = developer attention.
- **Reddit**: r/java, r/SpringBoot, r/programming, r/ExperiencedDevs, r/ClaudeAI, r/LocalLLaMA — top posts of the month. Recurring questions are tutorial demand; heated debates are "explained/opinion" video demand.
- **Releases and news**: spring.io/blog, Spring release calendar, JDK release notes/JEPs, InfoQ Java, major AI-tool announcements (Anthropic, OpenAI, JetBrains, Microsoft). A release in the last ~30 days or the next ~30 days is a timeliness multiplier — being early to a release is one of the most reliable growth plays for tutorial channels.
- **Conference lineups**: SpringOne, Devoxx, JavaOne accepted talks show what the community bets on next.

## Source 4: Search demand

- Test candidate phrasings the way a learner would type them: "spring boot 4 tutorial", "java ai agent", "spring ai rag example", "<tool> vs <tool>".
- Use Google Trends (trends.google.com) for direction on head terms — rising vs. flat vs. falling.
- Web-search each candidate keyword and inspect what currently ranks: if the top tutorial results are outdated (older framework versions) or low quality, that's a gap worth noting in the Differentiation score.

## Verification pass

Before writing the brief, re-check the two or three numbers that drive the top rankings (view counts, thread scores). If a number can't be confirmed, mark it "unverified" in the evidence line. The brief's credibility is the product's core feature.
