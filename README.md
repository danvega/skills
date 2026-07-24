# Dan Vega's Skills

A growing collection of agent skills, straight from my `.claude` directory. Spring,
Java, and the workflows I run every day, with more landing over time.

Each skill is small, composable, and built to encode the things models get *wrong*,
not to re-teach what they already know. This repo is the home for all of them.

Works with any agent that supports skills (Claude Code, and others via
[skills.sh](https://skills.sh)).

## Using these skills

A skill is just a folder with a `SKILL.md` in it — there's nothing to install. Clone
the repo and copy (or symlink) the folders you want to wherever your agent discovers
skills. For Claude Code that's:

```bash
git clone https://github.com/danvega/skills.git

# available in every session
cp -R skills/skills/spring/spring-boot-4/http-interface-clients ~/.claude/skills/

# or just for one project
cp -R skills/skills/blog/seo-optimize my-project/.claude/skills/
```

Symlinking instead of copying keeps them updated when you pull:

```bash
ln -s "$(pwd)/skills/skills/spring/spring-boot-4/null-safety" ~/.claude/skills/null-safety
```

The `spring-boot-4` skills cross-reference each other (e.g. `http-interface-clients`
points at `modular-auto-config` when a client won't wire), so they work best installed
as a set:

```bash
cp -R skills/skills/spring/spring-boot-4/* ~/.claude/skills/
```

## Why these exist

Models are trained on a snapshot of the world. Point one at the latest release of a
framework, and it reaches for last year's patterns, confidently and wrong. These
skills close that gap by encoding the **deltas**: what changed, the current idiom, and
the gotchas you only learn by hitting them.

Concretely, here's what that looks like for Spring Boot 4. Models were trained largely
on Boot 3.x, so without help they reach for the old way:

| You ask for… | Without the skill | With it |
| --- | --- | --- |
| A client for another service | `RestTemplate` boilerplate | `@HttpExchange` + `@ImportHttpServices` |
| Versioned endpoints | Manual path routing | Built-in API versioning |
| Retrying a flaky call | `spring-retry` dependency | Built-in `@Retryable` |
| JSON config | `com.fasterxml.jackson` | Jackson 3 (`tools.jackson`) |
| Null handling | Nullable-by-default assumptions | JSpecify non-null defaults |

## What's here

Two kinds of skills, kept deliberately separate:

- **Knowledge skills** are auto-discovered by description match. They teach the agent
  what changed in a framework or language: the deltas, not the basics.
- **Workflow skills** are processes that drive a repeatable task end to end — my
  actual blogging and YouTube workflows.

### spring

Spring skills live under `skills/spring/`, one folder per release or product — today
that's `spring-boot-4`, with room for `spring-ai` and friends as siblings.

**spring-boot-4** is one focused skill per feature. Each encodes the delta (what changed
in 4.x/7.x, the current idiom, and the gotchas) and triggers on the task, not the
feature name.

**APIs & web**
- **[http-interface-clients](./skills/spring/spring-boot-4/http-interface-clients/SKILL.md)**: `@ImportHttpServices` + `@HttpExchange` declarative clients
- **[api-versioning](./skills/spring/spring-boot-4/api-versioning/SKILL.md)**: the `version` attribute + `ApiVersionConfigurer`
- **[jackson-3](./skills/spring/spring-boot-4/jackson-3/SKILL.md)**: `tools.jackson`, auto-configured `JsonMapper`, ISO-8601 defaults, `@JsonView`

**Messaging & resilience**
- **[jms-client](./skills/spring/spring-boot-4/jms-client/SKILL.md)**: the fluent `JmsClient` (send, QoS, request-reply)
- **[resilience](./skills/spring/spring-boot-4/resilience/SKILL.md)**: built-in `@Retryable` + `@ConcurrencyLimit`, no Spring Retry

**Core & data**
- **[null-safety](./skills/spring/spring-boot-4/null-safety/SKILL.md)**: JSpecify `@NullMarked` / `@Nullable`
- **[bean-registration](./skills/spring/spring-boot-4/bean-registration/SKILL.md)**: the `BeanRegistrar` interface
- **[spring-data-aot](./skills/spring/spring-boot-4/spring-data-aot/SKILL.md)**: build-time repositories + the validation gotcha

**Testing**
- **[rest-test-client](./skills/spring/spring-boot-4/rest-test-client/SKILL.md)**: `RestTestClient` across all five bind modes
- **[mock-vs-rest](./skills/spring/spring-boot-4/mock-vs-rest/SKILL.md)**: `MockMvcTester` vs `RestTestClient` decision guide

**Observability, security & migration**
- **[opentelemetry](./skills/spring/spring-boot-4/opentelemetry/SKILL.md)**: the official `spring-boot-starter-opentelemetry`
- **[spring-security-mfa](./skills/spring/spring-boot-4/spring-security-mfa/SKILL.md)**: `@EnableMultiFactorAuthentication` + one-time tokens
- **[modular-auto-config](./skills/spring/spring-boot-4/modular-auto-config/SKILL.md)**: the split-up auto-configuration breaking change

### dev

General development workflow skills, not tied to any framework.

- **[readme](./skills/dev/readme/SKILL.md)**: write a README that fits the project type — what to lead with for a CLI vs library vs service vs monorepo, plus honesty rules (verified commands, no hype, no aspirational features) and plain-language style rules (short sentences, no em dashes)

### blog

The workflow behind [danvega.dev](https://www.danvega.dev) — from "what should I
write?" to a published, optimized post with a cover image. These are tuned to my site
and voice, but the structure is easy to adapt.

- **[seo-opportunities](./skills/blog/seo-opportunities/SKILL.md)**: find what to write or fix next, ranked by Search Console evidence
- **[new-blog-post](./skills/blog/new-blog-post/SKILL.md)**: scaffold and draft a new post with correct frontmatter, in my voice
- **[seo-optimize](./skills/blog/seo-optimize/SKILL.md)**: keyword research + on-page optimization for an existing post
- **[post-cover](./skills/blog/post-cover/SKILL.md)**: render the site's terminal-style cover image to PNG

### newsletter

The newsletter workflow — authored and sent in [Beehiiv](https://www.beehiiv.com), republished on the site.

- **[publish-newsletter](./skills/newsletter/publish-newsletter/SKILL.md)**: republish a Beehiiv edition on the site — fetch via MCP, convert to site markdown (embeds, local images, house footer), light typo pass, validated save

### video

The full pipeline for my [YouTube channel](https://www.youtube.com/@DanVega) — from
"what should I make?" through packaging to the first cut.

- **[video-ideation](./skills/video/video-ideation/SKILL.md)**: research-driven video ideas — fans out across channel data, YouTube outliers, community trends, and search demand, then returns a ranked brief where every idea cites evidence of real demand
- **[develop-idea](./skills/video/develop-idea/SKILL.md)**: pressure-test an idea I already have — validates demand with evidence, maps the existing coverage to find the angle it misses, scopes what's in and out, and ends in an honest go / reframe / park verdict
- **[demo-design](./skills/video/demo-design/SKILL.md)**: design the demo code with me in conversation — start from the final frame and work backwards to the beats, then build a viewer-followable companion repo with every checkpoint verified, plus a shot list to record from
- **[video-project](./skills/video/video-project/SKILL.md)**: scaffold a new project on disk — copies the 2026 template into a PascalCase project folder under `~/youtube/` and renames the Premiere project file to match
- **[video-packaging](./skills/video/video-packaging/SKILL.md)**: turn a chosen idea into a congruent package — title options, a thumbnail creative brief, and a scripted first-30-seconds intro that all tell the same story
- **[thumbnail](./skills/video/thumbnail/SKILL.md)**: render the final thumbnail art — no AI image generation; composes real photo cutouts (Apple Vision subject lift) with HTML/CSS templates in the channel's design language, rendered via headless Chrome, verified with a 120px shrink test
- **[rough-cut](./skills/video/rough-cut/SKILL.md)**: raw recording → safe first pass — trims dead air, cuts fillers, resolves retakes; knows the difference between talking-head silence and screen-share "silence" while a build runs
- **[motion-graphics](./skills/video/motion-graphics/SKILL.md)**: transcript-driven graphics pass — branded terminal-style lower thirds (and a growing template library) rendered via headless Chrome with alpha, placed by actually looking at the frame, composited with ffmpeg; every graphic also ships as a ProRes 4444 overlay for Premiere
- **[shorts](./skills/video/shorts/SKILL.md)**: chop a long-form video into 30–60s 9:16 shorts — finds the moments that stand alone (hook + payoff, quality bar over quota), reframes per segment (face crop vs stacked screen-share layout), and burns in word-by-word "karaoke pop" captions with selectable font styles

## What's a skill?

A skill is a small folder with a `SKILL.md` the agent loads on demand: a description
that tells it *when* to reach for the skill, and a body that tells it *what to do*.
Knowledge skills here route by task to focused reference files, and nothing loads until
it's relevant. See [Anthropic's docs](https://docs.claude.com/en/docs/claude-code/skills)
for the format.

## License

MIT
