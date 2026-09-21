#!/usr/bin/env python3
"""Make paginated inspection sheets and a source index, without changing originals.

Requires Pillow. Usage: python3 photo_sheet.py PHOTO_DIR -o OUTPUT_DIR
Also works on transparent cutouts; the gray background makes their edges visible.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("-o", "--out", required=True, type=Path)
    args = parser.parse_args()
    files = sorted(
        (p for p in args.source.iterdir()
         if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
         and p.name != "cutouts-sheet.png"),
        key=lambda p: p.name.lower(),
    )
    if not files:
        parser.error(f"No photos in {args.source}")
    if args.source.resolve() == args.out.resolve():
        parser.error("Output must be a separate directory so picker pages are not indexed")
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    index = []
    page_size, cols, cell_w, cell_h = 24, 4, 320, 240
    for start in range(0, len(files), page_size):
        subset = files[start:start + page_size]
        page = start // page_size + 1
        sheet = Image.new("RGB", (cols * cell_w, ((len(subset) + cols - 1) // cols) * cell_h), "#383838")
        draw = ImageDraw.Draw(sheet)
        for offset, path in enumerate(subset):
            number = start + offset + 1
            x, y = offset % cols * cell_w, offset // cols * cell_h
            with Image.open(path) as original:
                photo = ImageOps.exif_transpose(original).convert("RGBA")
                dimensions = photo.size
                photo.thumbnail((cell_w - 16, cell_h - 56), Image.Resampling.LANCZOS)
                sheet.paste(photo, (x + (cell_w - photo.width) // 2, y + 8), photo)
            label = f"{number:03d} {path.stem}"
            while draw.textlength(label, font=font) > cell_w - 16:
                label = label[:-2]
            draw.text((x + 8, y + cell_h - 40), label, fill="white", font=font)
            draw.text((x + 8, y + cell_h - 20), f"{dimensions[0]} x {dimensions[1]}", fill="#bbbbbb", font=font)
            index.append({"number": number, "page": page, "source": str(path.resolve()), "width": dimensions[0], "height": dimensions[1]})
        output = args.out / f"photos-{page:02d}.jpg"
        sheet.save(output, quality=90)
        print(output)
    (args.out / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    # Remove only surplus pages owned by this script after a library shrinks.
    for stale in args.out.glob("photos-*.jpg"):
        if stale.stem[7:].isdigit() and int(stale.stem[7:]) > page:
            stale.unlink()
    print(f"{len(files)} photos indexed in {args.out / 'index.json'}")


if __name__ == "__main__":
    main()
