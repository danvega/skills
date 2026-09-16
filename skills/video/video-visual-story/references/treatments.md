# Explainer treatments

The bundled template is a self-contained 1920×1080 light canvas with dark ink and a green
accent. It complements the existing dark overlay cards. Use the installed sibling
`video-motion-graphics/scripts/render.mjs`; install that skill's Node dependencies once if needed.
For separately installed skills, resolve them by their installed locations, not assumed repo paths.
No image-generation or external animation service is needed for these treatments.

## Flow

Use two to four nodes, short labels, and one visible journey. For loops with return messages,
author a separate custom path rather than misrepresenting the diagram as a one-way journey.
The example below is an illustrative generic flow, not a claim about a particular framework.

```json
{
  "mode": "flow",
  "eyebrow": "Request lifecycle",
  "title": "Validate before execution",
  "subtitle": "The request reaches the handler only after validation succeeds.",
  "nodes": [
    {"label": "Request", "detail": "Input arrives"},
    {"label": "Validation", "detail": "Check the required fields"},
    {"label": "Handler", "detail": "Execute the operation"}
  ],
  "reveals": [0.6, 2.4, 4.2],
  "takeaway": "Invalid input stops before the handler.",
  "takeawayAt": 5.5,
  "source": "Illustrative flow"
}
```

`reveals` specifies when each node highlights, not transcript times. Derive these local offsets
from the narration, keep them increasing, and leave a reading hold after the final highlight.
Use roughly 20-character node labels and brief details; verify actual layout rather than treating
character count as proof. This straight-path treatment illustrates the successful route; to show
rejection explicitly, author a branch instead of relying on text alone.

## Comparison

```json
{
  "mode": "compare",
  "eyebrow": "Before / after",
  "title": "Make the change easy to see",
  "subtitle": "Replace these example labels with the actual demonstrated contrast.",
  "before": {"label": "Before", "title": "Manual setup", "lines": ["Several explicit steps", "Repeated configuration"]},
  "after": {"label": "After", "title": "A focused default", "lines": ["One supported setting", "Same verified outcome"]},
  "reveals": [0.6, 2.4],
  "takeaway": "State the specific, demonstrated improvement.",
  "source": "Illustrative comparison"
}
```

Keep each panel to one short headline and two or three short lines. Use real code animation
instead if the audience needs to inspect exact syntax. Do not invent a measured improvement.

## Evidence

```json
{
  "mode": "evidence",
  "eyebrow": "From the documentation",
  "title": "The detail that matters",
  "subtitle": "Use the exact feature name and scope from the source.",
  "image": "file:///absolute/path/to/real-screenshot.png",
  "focus": {"x": 0.1, "y": 0.2, "w": 0.8, "h": 0.25},
  "reveals": [0.6],
  "takeaway": "Summarize only what the highlighted passage supports.",
  "source": "Source name · capture date"
}
```

The focus rectangle uses fractions of the ORIGINAL screenshot dimensions. It follows the
contained image, accounting for letterboxing. Crop a long page to the useful passage before
using it so text remains readable. Keep the original capture and source URL in the visual plan.

## Render and inspect

```bash
node <graphics-skill>/scripts/render.mjs --template <this-skill>/assets/templates/explainer.html \
  --params-file /absolute/flow.json --duration 8 --fps 30000/1001 \
  --poster /absolute/flow-poster.png --at 6

node <graphics-skill>/scripts/render.mjs --template <this-skill>/assets/templates/explainer.html \
  --params-file /absolute/flow.json --duration 8 --fps 30000/1001 --scale 2 \
  --out /absolute/cache/flow
```

For screenshots, add `--dependency /absolute/path/to/real-screenshot.png` to the render command.
Inspect the poster, then encode the full-frame insert once:

```bash
ffmpeg -nostdin -y -framerate 30000/1001 -i /absolute/cache/flow/f_%04d.png \
  -c:v h264_videotoolbox -b:v 50M -pix_fmt yuv420p /absolute/flow.mp4
```

Use the frame rate recorded in `render.json`. These full-frame explainers normally need only
MP4; alpha is not useful for an opaque background. Match the base video resolution for final
compositing. Watch the short composite with narration at normal speed, including the transition
back to the recording. Verify entry, staged reveals, final hold, and mobile readability.
