#!/usr/bin/env python3
"""Render a trailer timeline with independent visual shots, dialogue, music and SFX.

No downloads. Input paths must name local media. See references/trailer-edit.md for the schema.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time


def run(cmd):
    r = subprocess.run([str(x) for x in cmd], text=True, capture_output=True)
    if r.returncode:
        raise ValueError(r.stderr[-5000:])
    return r.stdout


def signature(path):
    path = Path(path).resolve()
    s = path.stat()
    return {"path": str(path), "size": s.st_size, "mtime_ns": s.st_mtime_ns}


def number(value, lo, hi, name):
    value = float(value)
    if not math.isfinite(value) or not lo <= value <= hi:
        raise ValueError(f"Invalid {name}: {value}")
    return value


def duck_expression(intervals, gain_db=-12, attack=.18, release=.65):
    """Sample-continuous raised-cosine ramps; overlapping lines share the deepest duck."""
    floor = 10 ** (gain_db / 20)
    envelopes = []
    for start, end in intervals:
        onset = max(0, start - .08)
        rise = f'(0.5-0.5*cos(PI*clip((t-({onset-attack}))/{attack},0,1)))'
        fall = f'(0.5+0.5*cos(PI*clip((t-({end+.12}))/{release},0,1)))'
        envelopes.append(f'min({rise},{fall})')
    if not envelopes:
        return '1'
    active = envelopes[0]
    for envelope in envelopes[1:]:
        active = f'max({active},{envelope})'
    return f'(1-{1-floor}*({active}))'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--encoder', choices=['hardware', 'software'], default='hardware')
    a = p.parse_args()
    started = time.monotonic()
    plan = json.loads(Path(a.plan).read_text())
    from fractions import Fraction
    fps_text = str(plan.get('fps', '30000/1001'))
    fps = number(float(Fraction(fps_text)), 1, 120, 'fps')
    width, height = plan.get('width', 1920), plan.get('height', 1080)
    if any(not isinstance(n, int) or n <= 0 or n % 2 or n > 7680 for n in (width, height)):
        raise ValueError('Dimensions must be positive even integers, no larger than 7680')
    out = Path(a.out).resolve()
    if out.suffix.lower() != '.mp4':
        raise ValueError('Output must be .mp4')
    if not plan.get('shots'):
        raise ValueError('At least one visual shot is required')
    shot_frames = [max(1, math.floor(number(s['duration'], .05, 60, 'shot duration') * fps + .5)) for s in plan['shots']]
    total = sum(shot_frames) / fps
    if total >= 60:
        raise ValueError('Teaser must be shorter than 60 seconds')
    sources = {Path(x['asset']).resolve() for x in plan['shots'] + plan.get('audio', [])}
    if out in sources:
        raise ValueError('Cannot overwrite source media')
    cache = Path(a.plan).resolve().parent / 'cache'
    cache.mkdir(parents=True, exist_ok=True)
    parts, shot_records = [], []
    version = run(['ffmpeg', '-version']).splitlines()[0]
    clock = 0
    for i, (shot, frames) in enumerate(zip(plan['shots'], shot_frames)):
        asset = Path(shot['asset']).resolve()
        start = number(shot.get('source_start', 0), 0, 86400, 'source start')
        duration = frames / fps
        still = asset.suffix.lower() == '.png'
        if not still:
            source_duration = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', asset]))
            if start + duration > source_duration + 1 / fps:
                raise ValueError(f'Shot extends past source end: {asset}')
        key = hashlib.sha256(json.dumps({'version': 1, 'source': signature(asset), 'start': start, 'frames': frames,
                                        'fps': fps_text, 'width': width, 'height': height, 'encoder': a.encoder, 'ffmpeg': version}, sort_keys=True).encode()).hexdigest()
        part = cache / (key + '.mp4')
        cached = part.exists()
        if not cached:
            temporary = cache / (key + '.partial.mp4')
            inputs = (['-loop', '1', '-framerate', fps_text, '-t', duration] if still else ['-ss', start, '-t', duration])
            codec = (['-c:v', 'h264_videotoolbox', '-b:v', '12M' if width <= 1920 else '50M'] if a.encoder == 'hardware'
                     else ['-c:v', 'libx264', '-preset', 'fast', '-crf', '18'])
            filters = (f'scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2,'
                       f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps_text},'
                       f'tpad=stop_mode=clone:stop_duration={duration},trim=end_frame={frames},setpts=PTS-STARTPTS')
            decode = ['-hwaccel', 'videotoolbox'] if a.encoder == 'hardware' and not still else []
            run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *inputs, *decode, '-i', asset, '-an', '-vf', filters,
                 *codec, '-pix_fmt', 'yuv420p', '-frames:v', frames, '-video_track_timescale', '90000', temporary])
            temporary.replace(part)
        parts.append(part)
        shot_records.append({'index': i, 'asset': str(asset), 'start': clock, 'duration': duration,
                             'source_start': start, 'cache_hit': cached, 'purpose': shot.get('purpose', '')})
        clock += duration
    listing = cache / 'shots.concat.txt'
    listing.write_text(''.join("file '" + str(path).replace("'", "'\\''") + "'\n" for path in parts))
    inputs = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', listing]
    filters, labels, words, uncertain = [], [], [], []
    # Silent base guarantees an audio stream and bounds the final mix through intentional gaps.
    filters.append(f'anullsrc=r=48000:cl=stereo,atrim=duration={total}[silence]')
    dialogue = [(float(x['start']), float(x['start']) + float(x['duration'])) for x in plan.get('audio', []) if x['role'] == 'dialogue']
    for i, audio in enumerate(plan.get('audio', []), 1):
        if audio['role'] not in ('dialogue', 'music', 'sfx'):
            raise ValueError('Audio role must be dialogue, music or sfx')
        asset = Path(audio['asset']).resolve()
        start = number(audio['start'], 0, total, 'audio placement')
        source_start = number(audio.get('source_start', 0), 0, 86400, 'audio source start')
        duration = number(audio['duration'], .01, total, 'audio duration')
        gain = number(audio.get('gain_db', 0 if audio['role'] == 'dialogue' else -18), -60, 12, 'gain')
        if start + duration > total + 1 / fps:
            raise ValueError('Audio extends past the teaser')
        source_duration = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', asset]))
        if source_start + duration > source_duration + .03:
            raise ValueError(f'Audio extends past source end: {asset}')
        inputs += ['-ss', source_start, '-t', duration, '-i', asset]
        chain = f'[{i}:a:0]asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB'
        speech = audio['role'] == 'dialogue'
        fade_in = number(audio.get('fade_in', min(.008 if speech else .05, duration / 2)), 0, duration / 2, 'fade in')
        fade_out = number(audio.get('fade_out', min(.035 if speech else .5, duration / 2)), 0, duration / 2, 'fade out')
        if fade_in:
            chain += f',afade=t=in:d={fade_in}:curve=qsin'
        if fade_out:
            chain += f',afade=t=out:st={duration-fade_out}:d={fade_out}:curve=qsin'
        chain += f',adelay={round(start*1000)}:all=1'
        if audio['role'] == 'music' and dialogue:
            duck = duck_expression(dialogue,
                number(audio.get('duck_db', -12), -60, 0, 'duck gain'),
                number(audio.get('duck_attack', .18), .01, 3, 'duck attack'),
                number(audio.get('duck_release', .65), .01, 3, 'duck release'))
            chain += f",aeval=exprs='val(0)*{duck}|val(1)*{duck}'"
        chain += f'[a{i}]'
        filters.append(chain)
        labels.append(f'[a{i}]')
        if audio['role'] == 'dialogue' and audio.get('transcript'):
            transcript = json.loads(Path(audio['transcript']).read_text())
            for segment in transcript.get('segments', []):
                for word in segment.get('words', []):
                    ws, we = word['start'], word['end']
                    if source_start <= ws < we <= source_start + duration:
                        words.append({**word, 'start': start + ws - source_start, 'end': start + we - source_start})
                    elif ws < source_start + duration and we > source_start:
                        uncertain.append(word)
    filters.append('[silence]' + ''.join(labels) + f'amix=inputs={len(labels)+1}:normalize=0:dropout_transition=0,atrim=duration={total},loudnorm=I=-14:TP=-1.5:LRA=11[aout]')
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = out.with_name(out.stem + '.partial.mp4')
    run(inputs + ['-filter_complex', ';'.join(filters), '-map', '0:v:0', '-map', '[aout]', '-c:v', 'copy',
                  '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-t', total, '-movflags', '+faststart', temporary])
    actual = float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', temporary]))
    if abs(actual - total) > .1:
        raise ValueError(f'Rendered duration mismatch: {actual} vs {total}')
    temporary.replace(out)
    receipt = {'duration': total, 'fps': fps_text, 'shots': shot_records, 'source_identities': [signature(x) for x in sorted(sources)],
               'seconds': round(time.monotonic() - started, 3)}
    out.with_suffix('.render.json').write_text(json.dumps(receipt, indent=2))
    out.with_suffix('.transcript.json').write_text(json.dumps({'clock':'teaser', 'segments':[{'words':sorted(words,key=lambda w:w['start'])}],
                                                            'boundary_words_for_review':uncertain}, indent=2))
    print(json.dumps({'output':str(out), **receipt}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, ZeroDivisionError) as error:
        raise SystemExit(str(error))
