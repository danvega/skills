#!/usr/bin/env python3
"""Cached rough-cut mechanics. Python standard library + ffmpeg/ffprobe + optional mlx_whisper.

analyze: audio, transcript, silence/activity candidates (never silently applies cuts)
build: reviewed decisions -> edit manifest + output-clock transcript
render: native-size CFR video from original sources, cached per source clip
map: source timestamp -> output timestamp, with optional bounded edge snapping
"""
import argparse
import array
import hashlib
import json
import math
import platform
from pathlib import Path
import re
import subprocess
import sys
import time
import wave
from fractions import Fraction

VERSION = 1
MODEL = "mlx-community/whisper-small.en-mlx"


def load(path):
    return json.loads(Path(path).read_text())


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def identity(path):
    path = Path(path).resolve()
    stat = path.stat()
    return {"path": str(path), "size": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def run(command):
    result = subprocess.run([str(x) for x in command], text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{command[0]} failed:\n{result.stderr[-6000:]}")
    return result


def ffmpeg(*args):
    return run(["ffmpeg", "-nostdin", "-hide_banner", "-y", *args])


def probe(path):
    data = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]).stdout)
    video = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    if not video:
        raise ValueError(f"No video stream: {path}")
    duration = float(video.get("duration", data["format"]["duration"]))
    if audio and abs(float(video.get("start_time", 0)) - float(audio.get("start_time", 0))) > .05:
        raise ValueError(f"Audio/video start offset exceeds 50 ms: {path}. Normalize the streams together before analysis.")
    # Rotated and anamorphic sources need an explicit common sequence setup, not silent scaling.
    if video.get("sample_aspect_ratio", "1:1") not in ("1:1", "N/A") or any(s.get("rotation", 0) for s in video.get("side_data_list", [])):
        raise ValueError(f"Normalize rotation/sample aspect ratio before analysis: {path}")
    return {"duration": duration, "width": video["width"], "height": video["height"],
            "fps": video.get("avg_frame_rate") or video["r_frame_rate"], "has_audio": audio is not None}


def rate(value):
    number = float(Fraction(str(value)))
    if not math.isfinite(number) or not 0 < number <= 240:
        raise ValueError("FPS must be greater than 0 and at most 240")
    return number


def ordered(paths):
    paths = [Path(p).resolve() for p in paths]
    if len(paths) != len(set(paths)):
        raise ValueError("Duplicate source paths")
    def slot(path):
        name = path.stem.lower()
        if "_intro" in name:
            return 0
        if "_outro" in name or "_outtro" in name or name == "endcard":
            return 2
        return 1
    for n in (0, 2):
        if sum(slot(p) == n for p in paths) > 1:
            raise ValueError("Multiple intro/outro candidates; pass the intended clips only")
    return sorted(paths, key=lambda p: (slot(p), [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", p.stem.lower())]))


def rms_windows(path):
    values = []
    with wave.open(str(path), "rb") as wav:
        if wav.getsampwidth() != 2 or wav.getnchannels() != 1:
            raise ValueError("Expected mono PCM16 audio")
        count = round(wav.getframerate() * .05)
        while data := wav.readframes(count):
            samples = array.array("h", data)
            if sys.byteorder != "little":
                samples.byteswap()
            rms = math.sqrt(sum(x * x for x in samples) / len(samples)) / 32768
            values.append(20 * math.log10(max(rms, 1e-6)))
    return values


def percentile(values, p):
    return sorted(values)[min(len(values) - 1, round((len(values) - 1) * p))]


def silences_from_log(log, duration):
    silences, start = [], None
    for event, value in re.findall(r"silence_(start|end):\s*([\d.]+)", log):
        if event == "start":
            start = max(0., float(value))
        elif start is not None:
            silences.append([start, min(duration, float(value))])
            start = None
    if start is not None:
        silences.append([start, duration])
    return silences


def activity(path, start, end):
    # Keep original sample rate: the calibrated rate threshold is not portable to a downsampled proxy.
    if not math.isfinite(start) or not math.isfinite(end) or not 0 <= start < end:
        raise ValueError("Activity window must have increasing nonnegative times")
    decode = ["-hwaccel", "videotoolbox"] if platform.system() == "Darwin" else []
    result = ffmpeg("-v", "info", "-ss", start, "-t", end - start, *decode, "-i", path, "-an",
                    "-vf", "select='gt(scene,0.003)',metadata=print", "-f", "null", "-")
    hits = len(re.findall(r"lavfi.scene_score=", result.stderr))
    return {"hits": hits, "seconds": end - start, "changes_per_second": hits / (end - start)}


def words_in(transcript):
    return [w for s in transcript.get("segments", []) for w in s.get("words", [])]


def silence_candidates(silent, words, mode, measure):
    """Turn detected silences into candidates; measure(start, end) reports screen activity."""
    candidates = []
    for start, end in silent:
        length = end - start
        if mode == "screen-share" and length <= 2:
            continue
        check = measure(start, end) if mode == "screen-share" else None
        pause = (.7 if check else .4 if length <= 2 else .5)
        previous = next((w for w in reversed(words) if w["end"] <= start + .3), None)
        if previous and str(previous["word"]).rstrip().endswith(("?", "…")):
            pause = max(pause, .5)
        # Retain an extra 0.8 seconds at a clip head to protect a quiet first word.
        a, b = (0., end - .8) if start < .05 else (start + pause / 2, end - pause / 2)
        if b <= a:
            continue
        if check and check["changes_per_second"] >= .5:
            # Wordless and active: silent code entry gets cut, a result the viewer must watch stays.
            # Scene changes cannot tell those apart, so propose the range and leave the call to review.
            candidates.append({"start": start, "end": end, "reason": "screen activity", "suggest_cut": False,
                               "activity": check, "proposed_cut": {"start": a, "end": b}})
        else:
            candidates.append({"start": a, "end": b, "reason": "silence", "suggest_cut": True, "activity": check})
    return candidates


def prepare_media(args):
    """Extract only audio, then transcribe all uncached clips in one MLX process."""
    work = Path(args.work).resolve()
    prepared, pending = [], []
    asr_folder = work / "cache" / "transcripts" / digest({"model": args.model, "language": "en", "words": True, "version": VERSION})[:12]
    asr_folder.mkdir(parents=True, exist_ok=True)
    for source in ordered(args.sources):
        began = time.monotonic()
        fingerprint = identity(source)
        clip_id = digest(fingerprint)[:16]
        folder = work / "cache" / clip_id
        folder.mkdir(parents=True, exist_ok=True)
        meta_path = folder / "probe.json"
        if not meta_path.exists():
            save(meta_path, probe(source))
        meta = load(meta_path)
        passthrough = source.stem.lower() == "endcard" or str(source) in [str(Path(p).resolve()) for p in args.passthrough]
        clip = {"id": clip_id, "source": str(source), "fingerprint": fingerprint, **meta,
                "mode": getattr(args, "mode", "talking-head"), "passthrough": passthrough}
        audio = folder / f"{clip_id}.wav"
        hit_audio = audio.exists()
        transcript = None
        asr_hit = False
        if not passthrough and meta["has_audio"]:
            if not hit_audio:
                temp = folder / "audio.partial.wav"
                ffmpeg("-v", "error", "-i", source, "-map", "0:a:0", "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", temp)
                temp.replace(audio)
            if not args.skip_transcript:
                transcript = asr_folder / f"{clip_id}.json"
                asr_hit = transcript.exists()
                if not asr_hit:
                    pending.append(audio)
        clip["transcript"] = str(transcript) if transcript else None
        prepared.append({"clip": clip, "folder": folder, "audio": audio, "audio_cache_hit": hit_audio,
                         "asr_cache_hit": asr_hit, "prepare_seconds": time.monotonic() - began})
    asr_started = time.monotonic()
    if pending:
        # Unique audio basenames prevent collisions in the shared output directory.
        # Write to a scratch directory and promote only valid complete JSON after successful ASR.
        import tempfile
        with tempfile.TemporaryDirectory(prefix="asr-", dir=asr_folder) as temporary:
            run(["mlx_whisper", *pending, "--model", args.model, "--language", "en", "--word-timestamps", "True",
                 "--output-format", "json", "--output-dir", temporary, "--verbose", "False"])
            for audio in pending:
                result = Path(temporary) / (audio.stem + ".json")
                load(result)
                result.replace(asr_folder / result.name)
    return prepared, round(time.monotonic() - asr_started, 3)


def transcribe(args):
    prepared, asr_seconds = prepare_media(args)
    save(Path(args.work) / "transcripts.json", {"clips": [x["clip"] for x in prepared], "asr_seconds": asr_seconds,
        "timings": [{k: x[k] for k in ("audio_cache_hit", "asr_cache_hit", "prepare_seconds")} for x in prepared]})
    print(Path(args.work).resolve() / "transcripts.json")


def analyze(args):
    work = Path(args.work).resolve()
    clips, timings = [], []
    prepared, asr_seconds = prepare_media(args)
    for item in prepared:
        began = time.monotonic()
        clip = item["clip"]
        source, meta, folder, audio = Path(clip["source"]), clip, item["folder"], item["audio"]
        transcript = Path(clip["transcript"]) if clip["transcript"] else None
        if clip["passthrough"] or not clip["has_audio"]:
            clip.update(candidates=[], silences=[], notes=["Preserved without audio analysis"])
            clips.append(clip)
            continue
        # "candidates" versions the candidate shape without invalidating cached transcripts.
        analysis_path = folder / (digest({"version": VERSION, "candidates": 2, "mode": args.mode, "threshold": args.threshold,
                                           "transcript": identity(transcript) if transcript else None})[:16] + ".analysis.json")
        hit_analysis = analysis_path.exists()
        if hit_analysis:
            analysis = load(analysis_path)
        else:
            levels = rms_windows(audio)
            floor, speech = percentile(levels, .1), percentile(levels, .8)
            threshold = float(args.threshold) if args.threshold is not None else max(floor + 6, speech - 15)
            threshold = min(-18., max(-65., threshold)) if args.threshold is None else threshold
            if not math.isfinite(threshold) or not -120 <= threshold <= 0:
                raise ValueError("Silence threshold must be between -120 and 0 dB")
            silent = silences_from_log(ffmpeg("-v", "info", "-i", audio, "-af", f"silencedetect=noise={threshold}dB:d=0.6", "-f", "null", "-").stderr, meta["duration"])
            notes = ["Fillers not analyzed: the default ASR normalizes disfluencies"]
            words = words_in(load(transcript)) if transcript else []
            if transcript and not words:
                notes.append("No word timestamps returned; inspect the audio before speech-based cuts")
            candidates = silence_candidates(silent, words, args.mode, lambda a, b: activity(source, a, b))
            if len(silent) < 2 and meta["duration"] > 120:
                notes.append("Few silences detected; inspect the threshold and a known quiet interval")
            if args.mode == "screen-share":
                notes.append("Before accepting static candidates, check a known typing interval with the activity command")
                if any(c.get("proposed_cut") for c in candidates):
                    notes.append("Classify each wordless active window: cut silent code entry, keep a result the viewer must watch")
            analysis = {"threshold_db": threshold, "noise_floor_db": floor, "speech_proxy_db": speech,
                        "silences": silent, "candidates": candidates, "notes": notes}
            save(analysis_path, analysis)
        clip.update(analysis)
        clip["transcript"] = str(transcript) if transcript else None
        clips.append(clip)
        timings.append({"source": str(source), "seconds": round(time.monotonic() - began, 3),
                        "prepare_seconds": round(item["prepare_seconds"], 3), "audio_cache_hit": item["audio_cache_hit"],
                        "asr_cache_hit": item["asr_cache_hit"], "analysis_cache_hit": hit_analysis})
        unclassified = sum(1 for c in clip["candidates"] if c.get("proposed_cut"))
        print(f"Analyzed {source.name}: {len(clip['candidates'])} candidates, {unclassified} to classify", flush=True)
    save(work / "analysis.json", {"version": VERSION, "clips": clips, "timings": timings, "batch_asr_seconds": asr_seconds})
    # Never overwrite the human/agent's reviewed decisions on a rerun.
    save(work / "suggested-decisions.json", {"clips": [{"id": c["id"], "cuts": [
        {k: x[k] for k in ("start", "end", "reason")} for x in c["candidates"] if x["suggest_cut"]], "speeds": [],
        "classify": [{**x["proposed_cut"], "reason": f"wordless screen activity, {x['activity']['changes_per_second']:.1f} changes/s"}
                     for x in c["candidates"] if x.get("proposed_cut")]} for c in clips]})
    print(work / "analysis.json")


def intervals(items, duration):
    result = []
    for item in items:
        a, b = float(item["start"]), float(item["end"])
        if not all(math.isfinite(t) for t in (a, b)) or not 0 <= a < b <= duration:
            raise ValueError(f"Invalid interval {a}..{b}; source duration {duration}")
        result.append((a, b))
    merged = []
    for a, b in sorted(result):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


def make_segments(duration, cuts, speeds):
    cuts = intervals(cuts, duration)
    intervals(speeds, duration)  # validates numeric bounds
    speeds = sorted(speeds, key=lambda x: x["start"])
    for i, s in enumerate(speeds):
        if not math.isfinite(s["speed"]) or not .25 <= s["speed"] <= 16:
            raise ValueError("Speed must be between 0.25 and 16")
        if i and s["start"] < speeds[i - 1]["end"]:
            raise ValueError("Speed intervals must not overlap")
    points = sorted({0., duration, *(x for c in cuts for x in c), *(s[k] for s in speeds for k in ("start", "end"))})
    result = []
    for a, b in zip(points, points[1:]):
        mid = (a + b) / 2
        if any(c <= mid < d for c, d in cuts):
            continue
        speed = next((s["speed"] for s in speeds if s["start"] <= mid < s["end"]), 1.)
        result.append({"source_start": a, "source_end": b, "speed": speed})
    return result


def mapped_time(manifest, clip_id, t, snap=0.):
    segments = [s for s in manifest["segments"] if s["clip_id"] == clip_id]
    for s in segments:
        if s["source_start"] <= t < s["source_end"]:
            return {"time": min(s["output_end"], s["output_start"] + (t - s["source_start"]) / s["speed"]), "snapped": False}
    # Exact keep ends are valid for end boundaries, even without snapping.
    for s in segments:
        if abs(t - s["source_end"]) < 1e-9:
            return {"time": s["output_end"], "snapped": False}
    edges = [(abs(t - s[k]), s[o]) for s in segments for k, o in (("source_start", "output_start"), ("source_end", "output_end"))]
    if edges:
        delta, out = min(edges)
        if 0 < snap <= .3 and delta <= snap:
            return {"time": out, "snapped": True, "distance": delta}
    return None


def map_words(manifest):
    output, dropped, review = [], [], []
    for clip in manifest["clips"]:
        if not clip.get("transcript"):
            continue
        for word in words_in(load(clip["transcript"])):
            a, b = float(word["start"]), float(word["end"])
            # Only map a word contained by one kept interval. Never resurrect a deleted take.
            segment = next((s for s in manifest["segments"] if s["clip_id"] == clip["id"] and s["source_start"] <= a < b <= s["source_end"]), None)
            if segment:
                output.append({**word, "start": min(segment["output_end"], segment["output_start"] + (a - segment["source_start"]) / segment["speed"]),
                               "end": min(segment["output_end"], segment["output_start"] + (b - segment["source_start"]) / segment["speed"]),
                               "source_clip": clip["id"], "source_start": a, "source_end": b})
            else:
                item = {**word, "source_clip": clip["id"]}
                if any(s["clip_id"] == clip["id"] and a < s["source_end"] and b > s["source_start"] for s in manifest["segments"]):
                    review.append(item)
                else:
                    dropped.append(item)
    output.sort(key=lambda w: w["start"])
    return {"clock": "output", "manifest_id": manifest["id"], "segments": [{"words": output}],
            "boundary_words_for_review": review, "removed_words": dropped}


def build(args):
    analysis = load(args.analysis)
    decisions = load(args.decisions)
    choices = {c["id"]: c for c in decisions["clips"]}
    if len(choices) != len(decisions["clips"]) or set(choices) != {c["id"] for c in analysis["clips"]}:
        raise ValueError("Decisions must contain each analyzed clip exactly once")
    if any(c.get("classify") for c in decisions["clips"]):
        raise ValueError("Unresolved classify entries: move silent code entry to cuts, delete what the viewer must watch")
    fps = args.fps or analysis["clips"][0]["fps"]
    hz = rate(fps)
    dimensions = {(c["width"], c["height"]) for c in analysis["clips"]}
    if len(dimensions) != 1:
        raise ValueError("Mixed source dimensions: normalize to the intended sequence size first")
    segments, frame = [], 0
    for clip in analysis["clips"]:
        if identity(clip["source"]) != clip["fingerprint"]:
            raise ValueError("Source changed; rerun analysis")
        choice = choices[clip["id"]]
        if clip["passthrough"] and (choice["cuts"] or choice.get("speeds")):
            raise ValueError("Passthrough clips must not be cut or retimed")
        for s in make_segments(clip["duration"], choice["cuts"], choice.get("speeds", [])):
            frames = max(1, math.floor((s["source_end"] - s["source_start"]) / s["speed"] * hz + .5))
            segments.append({**s, "clip_id": clip["id"], "output_start": frame / hz, "output_end": (frame + frames) / hz,
                             "start_frame": frame, "frames": frames})
            frame += frames
    if not segments:
        raise ValueError("The edit removes all footage")
    width, height = next(iter(dimensions))
    if width % 2 or height % 2:
        raise ValueError("H.264 delivery requires even dimensions")
    manifest = {"version": VERSION, "fps": str(fps), "width": width, "height": height,
                "duration": frame / hz, "frames": frame, "clips": analysis["clips"], "segments": segments,
                "decisions": decisions}
    manifest["id"] = digest(manifest)
    save(args.out, manifest)
    save(Path(args.out).with_name("transcript.output.json"), map_words(manifest))
    print(f"{args.out}: {manifest['duration']:.3f}s, {len(segments)} kept intervals")


def tempo(speed):
    parts = []
    while speed > 2:
        parts.append("atempo=2")
        speed /= 2
    while speed < .5:
        parts.append("atempo=0.5")
        speed /= .5
    return ",".join(parts + [f"atempo={speed:.12g}"])


def filter_graph(segments, fps, has_audio):
    lines = []
    for i, s in enumerate(segments):
        a, b, speed = (s[k] for k in ("source_start", "source_end", "speed"))
        duration = s["frames"] / rate(fps)
        lines.append(f"[0:v:0]trim=start={a:.9f}:end={b:.9f},setpts=(PTS-STARTPTS)/{speed:.12g},fps={fps},tpad=stop_mode=clone:stop_duration={duration:.9f},trim=end_frame={s['frames']},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v{i}]")
        if has_audio:
            lines.append(f"[0:a:0]atrim=start={a:.9f}:end={b:.9f},asetpts=PTS-STARTPTS,{tempo(speed)},aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo,apad,atrim=duration={duration:.9f}[a{i}]")
        else:
            lines.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={duration:.9f}[a{i}]")
    inputs = "".join(f"[v{i}][a{i}]" for i in range(len(segments)))
    lines.append(f"{inputs}concat=n={len(segments)}:v=1:a=1[outv][outa]")
    return ";\n".join(lines)


def render(args):
    began = time.monotonic()
    manifest = load(args.manifest)
    expected_id = manifest.pop("id")
    if digest(manifest) != expected_id:
        raise ValueError("Manifest was edited directly; rebuild it from decisions")
    manifest["id"] = expected_id
    destination = Path(args.out).resolve()
    if destination.suffix.lower() != ".mp4":
        raise ValueError("Delivery path must end in .mp4")
    if str(destination) in {c["source"] for c in manifest["clips"]}:
        raise ValueError("Cannot overwrite source footage")
    cache = Path(args.manifest).resolve().parent / "cache" / "renders"
    cache.mkdir(parents=True, exist_ok=True)
    parts, records = [], []
    ffversion = run(["ffmpeg", "-version"]).stdout.splitlines()[0]
    for clip in manifest["clips"]:
        if identity(clip["source"]) != clip["fingerprint"]:
            raise ValueError(f"Source changed: {clip['source']}; rerun analysis")
        segments = [s for s in manifest["segments"] if s["clip_id"] == clip["id"]]
        if not segments:
            continue
        # Later clips retain cache hits when an earlier clip's edit moves their output offset.
        local = [{k: s[k] for k in ("source_start", "source_end", "speed", "frames")} for s in segments]
        key = digest({"version": VERSION, "source": clip["fingerprint"], "segments": local,
                      "fps": manifest["fps"], "encoder": args.encoder, "ffmpeg": ffversion})
        part = cache / f"{key}.mkv"
        cached = part.exists()
        start = time.monotonic()
        if not cached:
            graph = cache / f"{key}.filter.txt"
            graph.write_text(filter_graph(local, manifest["fps"], clip["has_audio"]))
            temporary = cache / f"{key}.partial.mkv"
            codec = (["-c:v", "h264_videotoolbox", "-b:v", "50M", "-maxrate", "60M", "-bufsize", "80M"]
                     if args.encoder == "hardware" else ["-c:v", "libx264", "-preset", "fast", "-crf", "18"])
            decode = ["-hwaccel", "videotoolbox"] if args.encoder == "hardware" else []
            ffmpeg("-v", "error", *decode, "-i", clip["source"], "-filter_complex_script", graph,
                   "-map", "[outv]", "-map", "[outa]", *codec, "-pix_fmt", "yuv420p", "-r", manifest["fps"],
                   "-c:a", "pcm_s16le", temporary)
            temporary.replace(part)
        parts.append(part)
        records.append({"source": clip["source"], "cache_hit": cached, "seconds": round(time.monotonic() - start, 3)})
        print(f"{'Cached' if cached else 'Rendered'} {Path(clip['source']).name}", flush=True)
    listing = cache / f"{expected_id}.concat.txt"
    listing.write_text("".join("file '" + str(p).replace("'", "'\\''") + "'\n" for p in parts))
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.stem + ".partial.mp4")
    ffmpeg("-v", "error", "-f", "concat", "-safe", "0", "-i", listing, "-map", "0:v:0", "-map", "0:a:0",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-video_track_timescale", "90000", "-movflags", "+faststart", temporary)
    actual = probe(temporary)
    if abs(actual["duration"] - manifest["duration"]) > max(.1, 2 / rate(manifest["fps"])):
        raise ValueError(f"Rendered duration {actual['duration']} differs from manifest {manifest['duration']}")
    temporary.replace(destination)
    save(destination.with_suffix(".render.json"), {"manifest_id": expected_id, "output": str(destination),
        "seconds": round(time.monotonic() - began, 3), "parts": records, "probe": actual})
    print(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("analyze")
    p.add_argument("sources", nargs="+")
    p.add_argument("--work", required=True)
    p.add_argument("--mode", choices=["talking-head", "screen-share"], required=True)
    p.add_argument("--passthrough", action="append", default=[])
    p.add_argument("--skip-transcript", action="store_true")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--threshold", type=float)
    p.set_defaults(action=analyze)
    p = sub.add_parser("transcribe")
    p.add_argument("sources", nargs="+")
    p.add_argument("--work", required=True)
    p.add_argument("--model", default=MODEL)
    p.set_defaults(action=transcribe, skip_transcript=False, passthrough=[])
    p = sub.add_parser("build")
    p.add_argument("--analysis", required=True)
    p.add_argument("--decisions", required=True)
    p.add_argument("--fps")
    p.add_argument("--out", required=True)
    p.set_defaults(action=build)
    p = sub.add_parser("render")
    p.add_argument("--manifest", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--encoder", choices=["hardware", "software"], default="hardware")
    p.set_defaults(action=render)
    p = sub.add_parser("map")
    p.add_argument("--manifest", required=True)
    p.add_argument("--clip", required=True)
    p.add_argument("--time", type=float, required=True)
    p.add_argument("--snap", type=float, default=0.)
    p.set_defaults(action=lambda a: print(json.dumps(mapped_time(load(a.manifest), a.clip, a.time, a.snap))))
    p = sub.add_parser("activity")
    p.add_argument("source")
    p.add_argument("--start", type=float, required=True)
    p.add_argument("--end", type=float, required=True)
    p.set_defaults(action=lambda a: print(json.dumps(activity(a.source, a.start, a.end))))
    args = parser.parse_args()
    try:
        args.action(args)
    except (ValueError, RuntimeError, OSError, KeyError, ZeroDivisionError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
