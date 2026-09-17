---
name: contentos-next
description: >-
  Move a ContentOS project forward to the next point where Dan is actually needed, running
  every stage in between without pausing for sign-off. Reads the project's 18-stage
  checklist, finds the next open stage, runs the stage skills in chain mode (brief,
  packaging, thumbnails, rough cut, graphics, metadata, blog post, shorts, X clips, social
  drafts) and stops only at the stops: Record, Edit, Publish, and Park. Use when Dan says
  "what's next", "next on <project>", "run it", "keep going", "move this forward", or
  "where are we on <project>", and right after contentos-capture when he wants it to keep
  going. With no project named, it shows the open projects and their next step. Do NOT
  use to research an undecided idea (video-develop-idea), to capture a new one
  (contentos-capture), or to run a single stage on its own (invoke that stage skill).
---

# ContentOS Next

The pipeline has 18 stages and only a few places where Dan himself has to act. Everything
else is a skill invocation. Until this skill existed, Dan was the scheduler who started
each one. `contentos-next` reads where a project is, runs every stage up to the next stop,
and hands Dan one thing.

This skill adds no editorial judgment of its own. It sequences. Every rule about briefs,
titles, cuts, and posts lives in the stage skills and still applies in full.

## The stops

| Stop | Dan does | What Next hands him |
|---|---|---|
| Record | films | the shoot brief: working title, thumbnail direction or round-1 sheet, intro script, beats, pre-flight checks |
| Edit | final edit in Premiere, and picks the real title and thumbnail | rough cut, graphics, transcript, title options from the metadata generator, a thumbnail sheet |
| Publish | hits publish on YouTube | a private draft upload with metadata and the final thumbnail |
| Park (conditional) | decides whether to make it at all | only when a develop-idea run returns PARK |

Everything between two stops runs without asking. One stop per run: never run past one.

## Decided or undecided

A project exists because Dan (or `contentos-capture`) promoted it. That is the decision.
Next never asks "is this worth making". It writes a short GO brief from the project's idea,
notes, and repo, ticks `IDEA_DEVELOPED`, and moves on.

Short means the record shape Dan asked for, defined in
`../contentos-capture/references/record-shape.md`: `## At a glance` with at most five
bullets (the verdict and its one-line reason, the promise, the money shot, what is blocked,
what happens next), then `## Scope` (in, deliberately out, demo plan, assumed knowledge,
one line each), then `## Hook`. No demand or competition sections. The whole brief fits on
one screen, about 250 words. Packaging does its own lighter research.

The exception: Dan says "research it first", or the project came from an ideation batch and
carries no notes in his own words. Then run `video-develop-idea` in chain mode and honor
its verdict. GO and REFRAME continue (a reframe continues on the reframed angle, flagged at
the top of the brief). PARK halts the chain and Next reports why.

## Chain mode

Stage skills are invoked through the Skill tool with arguments of the form
`in contentos <slug> (chain mode: <what to do, what to write, what to tick>)`.

Chain mode means: no sign-off pauses, pick the top option yourself as a working version,
write the result to ContentOS, and return. The same skills stay conversational when Dan
invokes them himself. `video-develop-idea`, `video-demo-design`, `video-packaging`, and
`video-thumbnail` each carry a "Chain mode" section that says exactly what changes.

## Stage table

Pipeline order, with the precondition each stage needs before it can run. A missing
precondition is a stop with one line naming what is missing and where it should be.

| Stage | Precondition | Chain-mode action |
|---|---|---|
| `IDEA_DEVELOPED` | project exists | decided: `save_brief` GO from idea, notes, repo in the record shape (At a glance, Scope, Hook); tick. Undecided: `video-develop-idea` chain run |
| `DEMO_CODE_WORKING` | brief | repo attached and Dan said it is done: tick on his word. Otherwise `video-demo-design` chain run (or `course-demo-design` when the project has sections) |
| `TITLE_LOCKED`, `INTRO_WRITTEN`, `THUMBNAIL_READY` | brief | `video-packaging` chain run: working title, hook, and intro locked, all three ticked (the concept counts as the working thumbnail so the gate opens), shoot brief published |
| thumbnails, round 1 | packaging locked, project folder exists | `video-thumbnail` chain run: four options to `06_Thumbnails/`, sheet sent, no lock. Runs here when Dan asks for the thumbnail before recording; otherwise at the Edit stop |
| **Stop: Record** | | |
| `RECORDED` | raw recordings in `/Users/vega/youtube/<Folder>/07_raw/` or `01_Footage/` beyond the template's `endcard.mp4`, or Dan says recorded | tick |
| `ROUGH_CUT` | recorded | `video-rough-cut` |
| `MOTION_GRAPHICS` | edit manifest from the rough cut | `video-motion-graphics` |
| metadata options | transcript | ContentOS generates YouTube metadata from the transcript; read it with `get_youtube_metadata` and present the title options next to the working title |
| thumbnails | transcript, title options | `video-thumbnail` round 1 if not yet run, else round 2 on the winner |
| **Stop: Edit** | | |
| `FINAL_EDIT` | final export in `04_Exports/`, or Dan says done | tick |
| `METADATA_ADDED` | Dan picked the title and thumbnail (else keep the working ones and say so) | `update_video_packaging` final title, `video-thumbnail` lock, metadata on the video |
| `UPLOADED` | YouTube connected in Settings > Social Accounts | private draft upload through ContentOS |
| `TEASER_TRAILER` | rough cut or better, and Dan asked for a teaser | optional, off by default: `video-teaser` only when Dan asks for one. Dan posts it himself before the video goes live; tick on his word |
| **Stop: Publish** | | |
| `VIDEO_PUBLISHED` | Dan publishes (the app raises VideoPublishedEvent), or Dan says published | tick |
| `BLOG_POST` | published | `blog-new-post`, then the ContentOS blog PR flow |
| `SHORTS`, `SHORTS_PUBLISHED` | final export | `video-shorts`, then the batch draft upload from the shorts board |
| X clips | final export | `video-x-clips` onto the shorts board. Dan posts them himself |
| `SOCIAL_CAMPAIGN` | published | `video-social-campaign`: drafts saved to the calendar. Scheduling waits for Dan's yes |
| `NEWSLETTER` | published, blog post in | the next edition draft picks up the video and post automatically; tick when the mention is in the draft |

Distribution runs when Dan says next after publishing. It does not fire on the publish
event by itself.

## Workflow

1. **Resolve the project.** Named: `get_project`. Not named: `list_projects` without
   DONE and ARCHIVED, compute the next stop for each, print that board, and continue only
   if exactly one project is mid-chain. Otherwise stop after the board.
2. **Read the checklist.** The first open required stage in pipeline order is the next
   action. Optional stages (blog post, shorts) run in distribution unless Dan says skip;
   the teaser trailer runs only when Dan asks for it.
3. **Run up to the next stop**, checking each precondition first. Pass shared inputs
   down (slug, project folder, transcript path) so the stage skills do not resolve them
   twice.
4. **At the stop, hand Dan exactly what that stop needs.** One message. No questions,
   unless the stop is Park.
5. **Say what was ticked.** ContentOS is the record; the message is the summary.

## Guardrails

- Never tick `RECORDED`, `FINAL_EDIT`, or `VIDEO_PUBLISHED` from inference. Require the
  file, the event, or Dan's word.
- Never post, schedule, publish, or send anything outward-facing without Dan's explicit
  yes. Drafts are fine.
- Never verify a demo Dan wrote. Only demos the agent built get verified.
- Never install tooling such as a JDK or SDK. If a stage needs a tool that is not there,
  stop and say so.
- Do not re-run a completed stage. Running Next twice at the same stop reports the stop
  again.
- Working versions are labeled as such in ContentOS (title, thumbnail concept) so the
  Edit stop knows what is still open.
