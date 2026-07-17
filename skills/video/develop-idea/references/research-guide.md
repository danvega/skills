# Single-Topic Research Guide

Tactics per source, pointed at validating **one topic** rather than sweeping for candidates. Each source should return findings in this shape:

```
- finding: <what was observed>
  evidence: <link + number, e.g. "youtube.com/watch?v=... — 210K views on a 12K-sub channel, 2 months old">
  reads-as: <demand signal / saturation signal / gap / risk>
```

## Source 1: Dan's own data (personal MCP)

Tools are on Dan's personal MCP server (danvega.dev); names end in:
`youtube-get-channel-stats`, `youtube-get-top-videos`, `youtube-get-latest-videos`, `youtube-search-videos-by-topic`, `blog-search-posts-by-keyword`, `blog-get-latest-posts`, `newsletter-search-posts-by-keyword`.

For a single topic:

1. `youtube-search-videos-by-topic` with the topic and its neighbors — has Dan already covered this? A prior video changes the question from "should I make this" to "refresh, sequel, or skip".
2. `youtube-get-channel-stats` for the channel average, then compare any prior related videos against it. Over-performance on an adjacent topic is transferable evidence; a flop on the same topic is a caution worth surfacing (though format or timing may explain it).
3. `blog-search-posts-by-keyword` / `newsletter-search-posts-by-keyword` — existing written material on the topic is both a demand signal (if it performed) and a production head start worth mentioning in the scope.

If the MCP tools aren't available, note it and continue — don't guess his stats.

## Source 2: YouTube — demand and competition in one pass

This source feeds both Step 2 (demand) and Step 3 (competition map), so collect enough per video to serve both: **views, channel size, age, format, versions covered, what it skips**.

- Web-search `site:youtube.com <topic>` plus learner phrasings of it ("<topic> tutorial", "<topic> explained", "<topic> java"). Prefer results from the last 6 months, but for the competition map also note the older videos that still rank — stale winners are the easiest to beat.
- Outlier math: views ÷ channel average (or ÷ subscribers). Above ~3x is interesting; above ~10x on a small channel means the *topic* drives the views. One strong outlier on a small channel outweighs a big channel's routine numbers.
- YouTube pages may be JS-rendered; if a fetch returns an empty shell, use browser tools or rely on web-search snippet data.
- Interpret an empty field carefully: zero decent videos on a topic is only a gap if Sources 3–4 show people actually want it. Otherwise it's silence.

Channels to check for coverage (Java/Spring/AI-dev niche, mix of sizes):
Amigoscode, Java Brains, Coding with John, Marco Behler / Marco Codes, Telusko, Bouali Ali, Devtiro, SpringDeveloper (Josh Long), Dan Vega (self-compare), JetBrains Java, ByteByteGo, AI-coding channels covering Claude Code / Cursor / Copilot.

Also check the adjacent-language lane: if the topic is hot in the Python/JS world with no good Java/Spring equivalent, that's the classic differentiation play for this channel.

## Source 3: Community signal

- **Hacker News**: search hn.algolia.com for the topic over the last 1–3 months. Front-page discussion = developer attention; the comment threads tell you what people are confused or arguing about — that confusion is the video's outline material.
- **Reddit**: r/java, r/SpringBoot, r/programming, r/ExperiencedDevs, r/ClaudeAI — search the topic, sort by top of the last month. Recurring questions are tutorial demand; debates are "explained/opinion" demand.
- **Releases**: spring.io/blog, JDK release notes/JEPs, major AI-tool announcements. A release within ~30 days (past or upcoming) is a timeliness multiplier and often the "why now" for the verdict. An idea tied to something announced-but-not-released may earn a *park until GA*.
- **Conference lineups**: SpringOne, Devoxx, JavaOne accepted talks — a talk on the topic means the community is betting on it.

## Source 4: Search demand

- Test the phrasings a learner would type: "<topic> tutorial", "how to <topic> in java", "<tool> vs <tool>". Note which phrasing dominates — it becomes the target keyword handed to `video-packaging`.
- Google Trends (trends.google.com) for direction on the head term: rising, flat, or falling. Falling demand on an evergreen topic isn't fatal; falling demand on a hype topic usually is.
- Inspect what currently ranks for the target phrasing. Outdated versions or thin content in the top results = a Differentiation gap worth citing in the verdict.

## Verification pass

Before writing the brief, re-check the two or three numbers the verdict leans on hardest (view counts, thread scores, trend direction). If a number can't be confirmed, mark it "unverified" in the evidence line — the brief's credibility is the product.
