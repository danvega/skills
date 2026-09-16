# Camera moves

Apply moves to the base footage before overlays, in the same graph and encode.
Times must be on the current edit manifest clock.

## Step 2.5 — Zooms (pure ffmpeg, no template)

Zooms transform the **base video** and must happen *before* the overlay pass (cards must not
zoom). Split the timeline into contiguous segments — the segments must tile the full duration,
no gaps — apply a zoom (or nothing) per segment, concat. Both recipes are resolution-agnostic
and keep the zoom center x-centered with the upward bias `(ih-oh)*0.3` for natural headroom.

**Hard punch** (constant 110% for the whole segment):

```
[b]trim=start=A:end=B,setpts=PTS-STARTPTS,scale=iw*1.10:ih*1.10,crop=iw/1.10:ih/1.10:(iw-ow)/2:(ih-oh)*0.3[v1];
```

**Slow push** (100→106% over the segment, D seconds at FPS):

```
[c]trim=start=B:end=C,setpts=PTS-STARTPTS,zoompan=z='min(1+0.06*on/(D*FPS),1.06)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*0.3':d=1:s=${W}x${H}:fps=${FPS}[v2];
```

`${W}x${H}` is the video's **native** size from ffprobe — zoompan's `s` defaults to 1280×720 and
will silently downscale if omitted (see pitfalls). Concat the segments (`[v0][v1][v2]concat=n=3`)
into `[base]`, then run the Step 3 overlay chain on `[base]` — one filter graph, one encode.
Audio needs no work: zooms don't change the timeline, so `-map 0:a -c:a copy` still holds.

**Code zoom-to-region** (screen-share) — the punch-in rule says never *blindly* zoom screen-share,
but a *targeted* zoom into the exact code being discussed is one of the best moves for code (makes
small text readable on mobile). It's the same segment/concat mechanism, but the crop is aimed at a
rectangle center `(CX,CY)` given as **fractions of the frame**, not center-with-headroom. Get the
region by extracting the frame (`ffmpeg -ss <t> -frames:v 1`) and reading the box off it — the same
fractional coords the `spotlight` template uses, so a zoom and a spotlight can share one measurement.

```
# hard zoom to region: zoom Z centered on (CX,CY), clamped so the crop stays on-frame
[seg]trim=start=A:end=B,setpts=PTS-STARTPTS,scale=iw*Z:ih*Z,crop=${W}:${H}:'min(max(CX*iw-${W}/2,0),iw-${W})':'min(max(CY*ih-${H}/2,0),ih-${H})',setsar=1[vN];
# smooth push to region (1→Z over D seconds)
[seg]trim=start=A:end=B,setpts=PTS-STARTPTS,zoompan=z='min(1+(Z-1)*on/(D*${FPS}),Z)':x='min(max(CX*iw-(iw/zoom)/2,0),iw-iw/zoom)':y='min(max(CY*ih-(ih/zoom)/2,0),ih-ih/zoom)':d=1:s=${W}x${H}:fps=${FPS},setsar=1[vN];
```

Z≈1/regionWidthFraction gets the region to roughly fill the width (e.g. a box ~45% wide → Z≈2.2).
`setsar=1` on every segment keeps concat happy. **For readability, often a `spotlight` overlay
(dim + highlight, no zoom) beats a zoom** — it keeps the surrounding code visible and never
softens the pixels. Reach for the zoom only when the code is genuinely too small to read.


## Speed changes

Speed changes belong in the rough-cut decisions file, before graphics are placed.
Use the pipeline build command to regenerate edit.json and transcript.output.json.
Then re-anchor graphics. Do not hand-maintain a second timestamp shift formula.
