#!/usr/bin/env python3
"""Build a feed-style contact sheet from rendered thumbnails.

Each option is shown twice, the way YouTube shows it: at desktop feed size
(360px wide) with the candidate title under it, and at 120px (sidebar /
phone size) beside it. One image to verify, one image to send Dan.

    contact_sheet.py -o sheet.png [-t "Title 1" -t "Title 2" ...] a.png b.png ...

Titles pair with images in order; a missing title falls back to the filename.
Pass the same title for every option when only the thumbnails differ.
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FEED_W, SMALL_W = 360, 120
COLS = 2
BG, FG, MUTED = "#0f0f0f", "#f1f1f1", "#aaaaaa"
PAD = 28


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w, max_lines=2):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while draw.textlength(lines[-1] + "…", font=fnt) > max_w and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "…"
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("-t", "--title", action="append", default=[])
    ap.add_argument("images", nargs="+")
    args = ap.parse_args()

    feed_h, small_h = FEED_W * 9 // 16, SMALL_W * 9 // 16
    cell_w = FEED_W + 24 + SMALL_W + PAD * 2
    cell_h = 22 + feed_h + 96 + PAD
    rows = (len(args.images) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * cell_w, rows * cell_h), BG)
    draw = ImageDraw.Draw(sheet)
    f_label, f_title, f_small, f_meta = font(13), font(17, bold=True), font(9, bold=True), font(13)

    for i, path in enumerate(args.images):
        title = args.title[i] if i < len(args.title) else os.path.basename(path)
        x0 = (i % COLS) * cell_w + PAD
        y0 = (i // COLS) * cell_h + PAD
        im = Image.open(path).convert("RGB")

        draw.text((x0, y0), os.path.basename(path), fill=MUTED, font=f_label)
        y = y0 + 22
        sheet.paste(im.resize((FEED_W, feed_h), Image.LANCZOS), (x0, y))
        ty = y + feed_h + 10
        for line in wrap(draw, title, f_title, FEED_W):
            draw.text((x0, ty), line, fill=FG, font=f_title)
            ty += 22
        draw.text((x0, ty + 2), "Dan Vega · 1.2K views · 1 hour ago", fill=MUTED, font=f_meta)

        sx = x0 + FEED_W + 24
        sheet.paste(im.resize((SMALL_W, small_h), Image.LANCZOS), (sx, y))
        sy = y + small_h + 6
        for line in wrap(draw, title, f_small, SMALL_W, max_lines=3):
            draw.text((sx, sy), line, fill=FG, font=f_small)
            sy += 12

    sheet.save(args.out)
    print(args.out, sheet.size, len(args.images))


if __name__ == "__main__":
    sys.exit(main())
