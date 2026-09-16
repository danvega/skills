# Record shape

Dan is the first reader of every record in ContentOS: capture notes, project
descriptions, and briefs. On 2026-09-16 he said the detailed briefs were so long he did
not get through them. This file is the one shape all three writers follow:
`contentos-capture`, `contentos-next` (the short GO brief), and `video-develop-idea`.

## Two layers

**Top layer: what Dan decides with.** It opens with `## At a glance` and fits on one
screen, about 250 to 300 words in total. He can stop reading at the first reference
heading and miss nothing he needs.

**Bottom layer: what later skills need.** Packaging, demo design, the blog post, and
social drafts read the file map, the stack, and the evidence. That detail goes at the end,
under a heading that says it is reference, one line per item, with no prose restating a
README.

## At a glance

At most five bullets, one line each:

1. What the video is, in one sentence. For a brief, the verdict and its one-line reason.
2. The money shot: the moment the demo proves the promise.
3. What is blocked, or "nothing blocked".
4. What happens next.
5. The angle in Dan's words, when he gave one.

## Sections by record

| Record | Top layer, in order | Reference layer |
|---|---|---|
| Capture notes (`save_idea`, becomes the project description) | At a glance, Dan's notes (verbatim), For contentos-next, Status at capture | Demo reference: stack, file map, demo story, sibling projects |
| GO brief written by `contentos-next` for a decided idea | At a glance, Scope, Hook | none |
| Develop-idea brief (`save_brief`) | At a glance, Scope, Hook | Evidence: demand (three bullets), competition (three bullets), angles considered |

Scope means: in, deliberately out, demo plan, assumed knowledge, rough shape. One line
per item.

## Field limits

`hook` and `whyNow` on an idea each stay under 500 characters. Longer values make
`promote_idea` roll back with "value too long for type character varying(500)", and the
idea has to be saved again.

## Example

The At a glance block from the first record written this way (2026-09-16):

```markdown
## At a glance

- Spring MVC follow-up to the plain-Java structured concurrency video. Same API, inside a real request.
- Demo is done: `/Users/vega/dev/spring-boot/federated-search`. One endpoint, three stub sources, chaos controls, tests.
- Four moments: sequential 1.5s, concurrent 700ms, a failure cancels the sibling call (503 plus "cancelled: youtube"), group timeout (504 after 2s).
- Blocked on: no git repo and no GitHub remote. Everything else is ready.
- Angle in Dan's words: fan-out in Spring used to mean WebFlux. Virtual threads plus a scope means you keep your blocking code.
```

The project `structured-concurrency-in-spring-boot-no-webflux-required` in ContentOS
holds the whole record in this shape.
