#!/usr/bin/env python3
"""Composite full-frame inserts/alpha overlays, or a bounded preview, preserving base narration.

python3 composite.py --plan graphics.json --out preview.mp4 --start 20 --duration 10 --width 960
Omit --start/--duration/--width for native-resolution final delivery.
"""
import argparse
import json
import math
from pathlib import Path
import subprocess
import time


def run(args):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stderr[-4000:])
    return result.stdout


def probe(path):
    result = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]))
    v = next(s for s in result["streams"] if s["codec_type"] == "video")
    return v, float(result["format"].get("duration", 0))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--start", type=float, default=0)
    p.add_argument("--duration", type=float)
    p.add_argument("--width", type=int)
    p.add_argument("--encoder", choices=["hardware", "software"], default="hardware")
    a = p.parse_args()
    began = time.monotonic()
    plan = json.loads(Path(a.plan).read_text())
    video = Path(plan["video"]).resolve()
    stat = video.stat()
    if plan["video_identity"] != {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns}:
        raise ValueError("Base video changed; recheck graphics anchors and update the plan identity")
    if plan.get("edit_manifest"):
        manifest = json.loads(Path(plan["edit_manifest"]).read_text())
        if manifest["id"] != plan["manifest_id"]:
            raise ValueError("Edit changed; re-anchor the graphics before rendering")
    v, total = probe(video)
    duration = a.duration if a.duration is not None else total - a.start
    if not all(math.isfinite(x) for x in (a.start, duration)) or not 0 <= a.start < total or duration <= 0:
        raise ValueError("Invalid preview interval")
    duration = min(duration, total - a.start)
    width = a.width or v["width"]
    if width <= 0 or width % 2 or width > v["width"]:
        raise ValueError("Preview width must be positive, even, and no larger than the source")
    height = round(v["height"] * width / v["width"] / 2) * 2
    out = Path(a.out).resolve()
    if out.suffix.lower() != ".mp4":
        raise ValueError("Output must end in .mp4")
    # Mixed camera/card color metadata can reinitialize the graph and reset setpts.
    # Keep this fixed-raster timeline continuous across those metadata changes.
    inputs = ["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", a.start, "-t", duration, "-reinit_filter", "0", "-i", video]
    graph = [f"[0:v]setpts=PTS-STARTPTS,scale={width}:{height},setsar=1[base0]"]
    count = 0
    asset_paths = set()
    for clip in plan["clips"]:  # Plan order is layer order; later clips paint over earlier ones.
        path = Path(clip["asset"]).resolve()
        asset_paths.add(path)
        start, length = float(clip["start"]), float(clip["duration"])
        if not all(math.isfinite(x) for x in (start, length)) or start < 0 or length <= 0 or start + length > total + .05:
            raise ValueError(f"Invalid asset interval: {path}")
        begin, end = max(a.start, start), min(a.start + duration, start + length)
        if end <= begin:
            continue
        asset, asset_duration = probe(path)
        if (asset["width"], asset["height"]) != (v["width"], v["height"]):
            raise ValueError(f"Asset raster does not match the base video: {path}")
        still = path.suffix.lower() == ".png"
        if not still and asset_duration + .05 < length:
            raise ValueError(f"Asset shorter than scheduled duration: {path}")
        if asset.get("codec_name") == "vp9":
            inputs += ["-c:v", "libvpx-vp9"]
        if still:
            inputs += ["-loop", "1", "-framerate", v["avg_frame_rate"], "-t", end - begin]
        else:
            inputs += ["-ss", begin - start, "-t", end - begin]
        inputs += ["-i", path]
        count += 1
        delay = begin - a.start
        graph.append(f"[{count}:v]scale={width}:{height},setsar=1,setpts=PTS-STARTPTS+{delay:.9f}/TB[g{count}]")
        graph.append(f"[base{count-1}][g{count}]overlay=eof_action=pass:repeatlast=0:enable='between(t,{delay:.9f},{end-a.start:.9f})'[base{count}]")
    if out == video or out in asset_paths:
        raise ValueError("Cannot overwrite a source video or graphic")
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = out.with_name(out.stem + ".partial.mp4")
    codec = (["-c:v", "h264_videotoolbox", "-b:v", "12M" if width < 1920 else "50M"] if a.encoder == "hardware"
             else ["-c:v", "libx264", "-preset", "fast", "-crf", "19"])
    run(inputs + ["-filter_complex", ";".join(graph), "-map", f"[base{count}]", "-map", "0:a?", *codec,
                  "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", duration, "-movflags", "+faststart", temporary])
    rendered, actual = probe(temporary)
    video_duration = float(rendered.get("duration", actual))
    if abs(video_duration - duration) > .1:
        raise ValueError(f"Unexpected video duration: {video_duration} vs {duration}")
    if abs(actual - duration) > .1:
        raise ValueError(f"Unexpected output duration: {actual} vs {duration}")
    temporary.replace(out)
    print(json.dumps({"output": str(out), "start": a.start, "duration": actual, "assets": count,
                      "seconds": round(time.monotonic() - began, 2)}))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration) as error:
        raise SystemExit(str(error))
