#!/usr/bin/env python3
"""Cut a vedit words.json down to one clip, with times relative to the clip start.

Writes the [{word, start, end}] list that assets/captions-wide.html reads.

  clip_words.py --words <work>/transcript/<id>.words.json --start 61.2 --end 118.9 --out clip1.words.json
"""

import argparse
import json


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--words", required=True, help="vedit words.json of the export")
    ap.add_argument("--start", type=float, required=True, help="clip start in seconds")
    ap.add_argument("--end", type=float, required=True, help="clip end in seconds")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    doc = json.load(open(a.words))
    words = doc["words"] if isinstance(doc, dict) else doc
    length = a.end - a.start
    clip = []
    for w in words:
        if a.start <= (w["s"] + w["e"]) / 2 < a.end:
            clip.append({"word": w["w"],
                         "start": round(max(w["s"] - a.start, 0.0), 3),
                         "end": round(min(w["e"] - a.start, length), 3)})
    if not clip:
        raise SystemExit(f"no words between {a.start} and {a.end}")
    json.dump(clip, open(a.out, "w"))
    print(f"{len(clip)} words, first: {clip[0]['word']!r} at {clip[0]['start']}s, "
          f"last: {clip[-1]['word']!r} ends {clip[-1]['end']}s of {length:.2f}s")


if __name__ == "__main__":
    main()
