#!/usr/bin/env python3
"""Extract clip-relative word timings for a short, handling the rough-cut trim map.

The whisper transcript (audio.json) is timestamped on the ORIGINAL recording, but
clips are usually cut from the rough cut, which has had dead air and retakes
trimmed out. Given a clip window on the ORIGINAL clock (i.e. the clock you read
in the transcript), this script:

  1. maps the clip boundaries through the rough cut's trim map (filter.txt) and
     prints them — use these as ffmpeg -ss/-to on the rough cut
  2. writes words.json with every spoken word inside the window, timed relative
     to the clip start — feed it to assets/captions.html as the `words` param

Without --filter (cutting from an untrimmed source) the mapping is identity.

Usage:
  extract_words.py --json /tmp/rough-cut/NAME/audio.json \
      --start 42.3 --end 78.1 \
      [--filter /tmp/rough-cut/NAME/filter.txt] \
      --out /tmp/shorts/NAME/clip1_words.json
"""

import argparse
import json
import re
import sys


def build_map(filter_path):
    keeps = []
    for a, b in re.findall(r"trim=start=([\d.]+):end=([\d.]+)", open(filter_path).read()):
        k = (float(a), float(b))
        if k not in keeps:  # video + audio emit duplicate trim lines
            keeps.append(k)
    cum, maps = 0.0, []
    for a, b in keeps:
        maps.append((a, b, cum - a))
        cum += b - a
    def to_out(t):
        for a, b, sh in maps:
            if a <= t <= b:
                return t + sh
        return None  # inside a trimmed-out region
    return to_out


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", required=True, help="whisper JSON with word timestamps")
    p.add_argument("--start", type=float, required=True, help="clip start, ORIGINAL clock (s)")
    p.add_argument("--end", type=float, required=True, help="clip end, ORIGINAL clock (s)")
    p.add_argument("--filter", help="rough-cut filter.txt (omit when cutting the original)")
    p.add_argument("--out", required=True, help="output words.json (clip-relative)")
    args = p.parse_args()

    to_out = build_map(args.filter) if args.filter else (lambda t: t)

    out_a, out_b = to_out(args.start), to_out(args.end)
    if out_a is None or out_b is None:
        sys.exit(f"clip boundary falls inside a trimmed-out region "
                 f"(start->{out_a}, end->{out_b}) — nudge the boundary to kept material")

    tr = json.load(open(args.json))
    words = [w for seg in tr["segments"] for w in seg.get("words", [])]
    if not words:
        sys.exit("no word timestamps in JSON — transcribe with --word-timestamps True")

    kept, dropped = [], 0
    for w in words:
        if not (args.start <= w["start"] < args.end):
            continue
        ws, we = to_out(w["start"]), to_out(w["end"])
        if ws is None or we is None:
            dropped += 1  # spoken inside a cut — that audio isn't in the video
            continue
        kept.append({"word": w["word"].strip(),
                     "start": round(ws - out_a, 3), "end": round(we - out_a, 3)})
    if not kept:
        sys.exit("no words in the clip window")

    with open(args.out, "w") as f:
        json.dump(kept, f, indent=1)

    print(f"OUT_A={out_a:.2f} OUT_B={out_b:.2f}   # ffmpeg -ss/-to on the trimmed video")
    print(f"{args.out}: {len(kept)} words, clip duration {out_b - out_a:.1f}s"
          + (f", {dropped} words dropped (inside trims)" if dropped else ""))


if __name__ == "__main__":
    main()
