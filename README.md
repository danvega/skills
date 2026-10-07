# Dan Vega's Skills

My agent skills for everyday development, Spring, and the workflows behind
[danvega.dev](https://www.danvega.dev), my YouTube channel, and Spring Office Hours.

These capture choices, conventions, and lessons I want an agent to carry into the next
task. Start with `dev` for everyday work or `shipit` for building a demo or product.
The content workflows are tailored to my setup and can serve as examples to adapt.

## Use a skill

Clone the repo and enter it:

```bash
git clone https://github.com/danvega/skills.git
cd skills
```

For Claude Code, link the skill folders you want into your personal skills directory:

```bash
mkdir -p "$HOME/.claude/skills"
ln -s "$PWD/skills/dev/readme" "$HOME/.claude/skills/readme"
```

The link points to this checkout, so edits and pulled updates are available through it.
Keep the checkout at the same path. If `readme` is already installed, check its location
before replacing it.

To copy instead of linking, use this command in place of `ln -s`:

```bash
cp -R skills/dev/readme "$HOME/.claude/skills/"
```

Replace `skills/dev/readme` with another skill folder to install it. Copy the entire
folder so its scripts, references, and assets come with it.
For a project-only skill, use that project's `.claude/skills/` directory instead.

Once installed, invoke it by name, such as `/readme`, or describe a task that matches
its description. See the [Claude Code skills documentation](https://code.claude.com/docs/en/skills)
for discovery and configuration. Other agents may use a different skill directory.

## What's here

### dev

General development skills with plain language and short instructions.

- **[readme](./skills/dev/readme/SKILL.md)**: write a README that fits the project and its readers
- **[pr-description](./skills/dev/pr-description/SKILL.md)**: turn a diff into a PR title and description with actual test results
- **[bug-repro](./skills/dev/bug-repro/SKILL.md)**: reproduce a bug, capture it in a regression test, and verify a focused fix when requested
- **[code-review](./skills/dev/code-review/SKILL.md)**: find actionable bugs and regressions, with evidence and file references
- **[release-notes](./skills/dev/release-notes/SKILL.md)**: turn changes between versions into useful release notes
- **[code-tour](./skills/dev/code-tour/SKILL.md)**: trace a real request or command through the code

### shipit

A process for new demos, small tools, and products: decide enough to start, build
something you can verify, then review and update. `PRODUCT.md` holds current scope
and decisions. Supporting files hold work and history, and are created only when useful.

The skills are not seven required stages. See the [shipit guide](./skills/shipit/README.md)
for the flow and examples of where to start.

- **[shipit-shape](./skills/shipit/shipit-shape/SKILL.md)**: clarify an idea and find the smallest useful version
- **[shipit-mvp](./skills/shipit/shipit-mvp/SKILL.md)**: create a short initial PRODUCT.md and refine it as the project takes shape
- **[shipit-stack](./skills/shipit/shipit-stack/SKILL.md)**: resolve material technical choices and record their reasons
- **[shipit-prototype](./skills/shipit/shipit-prototype/SKILL.md)**: explore an uncertain screen or interaction when a prototype would help
- **[shipit-verify](./skills/shipit/shipit-verify/SKILL.md)**: reuse or add checks, separating verified behavior from evidence awaiting review
- **[shipit-feature](./skills/shipit/shipit-feature/SKILL.md)**: build within scope, check the result, and batch review
- **[shipit-retro](./skills/shipit/shipit-retro/SKILL.md)**: use evidence from a run to propose a focused process improvement

### spring

Focused guidance for Spring Boot 4 migrations, under `skills/spring/spring-boot-4/`.

- **[jackson-3](./skills/spring/spring-boot-4/jackson-3/SKILL.md)**: Jackson 3 migration, JSON configuration, and changed defaults
- **[modular-auto-config](./skills/spring/spring-boot-4/modular-auto-config/SKILL.md)**: modular auto-configuration and missing starter dependencies

### blog

The workflow behind danvega.dev, from choosing a topic to preparing a post and cover.

- **[blog-seo-opportunities](./skills/blog/blog-seo-opportunities/SKILL.md)**: rank topics and improvements using Search Console evidence
- **[blog-new-post](./skills/blog/blog-new-post/SKILL.md)**: scaffold and draft a post with the site's frontmatter and writing style
- **[blog-seo-optimize](./skills/blog/blog-seo-optimize/SKILL.md)**: research keywords and improve an existing post
- **[blog-cover](./skills/blog/blog-cover/SKILL.md)**: render the site's terminal-style cover image

### newsletter

- **[newsletter-publish](./skills/newsletter/newsletter-publish/SKILL.md)**: republish a Beehiiv edition on the site with its links, images, and formatting

### podcast

Guest appearances and the Spring Office Hours episode workflow.

- **[podcast-appearance](./skills/podcast/podcast-appearance/SKILL.md)**: record a guest appearance in ContentOS and on danvega.dev
- **[spring-office-hours-prep](./skills/podcast/spring-office-hours-prep/SKILL.md)**: run the audio edit and show-notes steps for one episode
- **[spring-office-hours-edit](./skills/podcast/spring-office-hours-edit/SKILL.md)**: edit a recording into a podcast MP3 and transcript
- **[spring-office-hours-show-notes](./skills/podcast/spring-office-hours-show-notes/SKILL.md)**: assemble the episode title, description, and resource links
- **[spring-office-hours-spring-io-pr](./skills/podcast/spring-office-hours-spring-io-pr/SKILL.md)**: prepare the spring.io post and PR after the episode is published on Transistor

### contentos

The glue that moves a video through [ContentOS](https://github.com/danvega/contentos):
capture an idea in one pass, then run it forward to the next point where I am needed.

- **[contentos-capture](./skills/contentos/contentos-capture/SKILL.md)**: turn dictated notes, a repo, or a link into a saved idea and project
- **[contentos-next](./skills/contentos/contentos-next/SKILL.md)**: run a project through every stage up to the next stop: record, edit, or publish

## Adapt these to your setup

The `dev` and `shipit` skills can work with the conventions and tools in your project.
The Spring skills provide guidance for their stated framework versions.

The blog, newsletter, podcast, and video workflows include my paths, branding, and
publishing conventions. Some rely on ContentOS, Search Console, Figma, local site repos,
or media tools such as Node.js, ffmpeg, and transcription software. Read the selected
skill's prerequisites and replace personal paths and account details before using it.
Copying a skill does not install its tools or connect its accounts.

## Maintain the collection

Keep `name` and `description` valid in each skill's YAML frontmatter, and keep this
catalog aligned with the folders in `skills/`. See [CLAUDE.md](./CLAUDE.md) for
authoring conventions.

## License

Original material is licensed under [MIT](./LICENSE).
