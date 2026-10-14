---
name: readme
description: >-
  Write, update, or review a project README. Most of Dan's repos are small Spring Boot
  demos, so treat a repo as a demo unless it is clearly a library, CLI, or product. Use
  when the task includes creating, cleaning up, or reviewing a README. Do not use for API
  reference docs, contributing guides, changelogs, or blog posts.
---

# README

A README helps a stranger understand the project and run it. Most of Dan's repos are
demos that show one idea. Some go with a video, talk, workshop, or post. Many do not.

## Ground rules

- Read the build file, `application.yml` or `.properties`, `compose.yaml`, any `.http`
  files, and the controllers first. Take versions, ports, endpoints, env vars, and
  commands from them. Do not guess.
- Describe only what the code does. Every endpoint, property, class, and output you
  mention must exist in the code.
- Never invent a link. Link a video, talk, or post only when one exists. If a README says
  "coming soon" and Dan gives you the link, replace it.
- Write for a stranger, not for Dan on stage. Talking points, speaker notes, and workshop
  answers do not belong in the README.
- When updating, keep useful setup notes and gotchas. Change only what is stale.
- Keep it short. The code explains itself. Link out for long walkthroughs.

## Writing style

- Plain words. Short sentences, one idea each.
- No em dashes. Use a period, a comma, or parentheses.
- Open with an elevator pitch: what it does, in words a listener would understand.
- No marketing words, emoji headings, or badges.

## Demo (the default)

Use these sections in this order. Skip any that do not apply.

1. **Title and pitch.** One or two sentences on what the demo shows and why it matters.
2. **Related content.** Only if it exists: the video, post, or course link, or the event
   and date for a talk or workshop.
3. **Tested with.** Java, Spring Boot, and Spring AI versions from the build file.
   Example: "Java 25, Spring Boot 4.0.8, Spring AI 2.0.1."
4. **What you need.** JDK, Docker if Compose is used, and each API key as an env var with
   a placeholder value.
5. **Run it.** `./mvnw spring-boot:run` or the Gradle equivalent. Say what Docker Compose
   starts and on which port.
6. **Try it.** curl calls or the `.http` file, with the expected result. Put prompts meant
   to be pasted in their own code block.
7. **Where to look.** The one to three files to read first, as relative links.
8. **Branches.** When branches exist, a table of each branch and what it adds. Say which
   branch to start on and that `main` holds the finished code.
9. **Good to know.** Real gotchas and version quirks. Add "demo code, not production" when
   it matters, such as security, payments, or secrets.

Leave out Contributing, a License section (the LICENSE file is enough), roadmaps, feature
lists, project trees, and a table of contents.

When the output is visual (a UI, traces, reports), add screenshots to `images/` and link
them with relative paths. Confirm each file exists.

If the README teaches step by step, put Run it and Try it before the steps. Move long
walkthroughs to branch READMEs or a blog post.

## Library, CLI, or product

- **Library or starter.** Dependency coordinates, minimum config, and one small example
  with its result. State supported Java and Spring Boot versions.
- **CLI or tool.** Install, one useful command, common commands, and a pointer to `--help`.
- **Product or template.** What it is and who it is for, local setup, required settings
  with safe example values, and where to customize.

## Review pass

- Check each endpoint, property, class name, command, and version against the code. Fix
  or remove anything the code does not back.
- Run the build and the quickstart when it is cheap. Tell Dan what you could not verify.
- Check that links and image paths resolve.
- Read it as a first-time visitor. Remove filler and anything meant only for Dan.
