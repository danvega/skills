"""Small real render/composite regression tests; no actual user footage."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


def run(*args):
    result = subprocess.run([str(a) for a in args], text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout


def pixel(path, time):
    return subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(time), '-i', str(path), '-frames:v', '1',
                           '-vf', 'crop=2:2:160:90,scale=1:1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                          capture_output=True, check=True).stdout


class RenderMediaTests(unittest.TestCase):
    def test_mixed_color_metadata_preserves_picture_clock(self):
        # Camera footage and generated cards may carry different color metadata.
        with tempfile.TemporaryDirectory(prefix='graphics-clock-') as tmp:
            root = Path(tmp)
            parts = []
            for i, color in enumerate(['blue', 'red']):
                part = root / f'{i}.mp4'
                metadata = [] if i == 0 else ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']
                run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                    f'color={color}:s=320x180:r=30000/1001:d=1.001',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', *metadata, part)
                parts.append(part)
            listing = root / 'parts.txt'
            listing.write_text(''.join(f"file '{p}'\n" for p in parts))
            base = root / 'base.mp4'
            run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'concat', '-safe', '0',
                '-i', listing, '-c', 'copy', base)
            stat = base.stat()
            plan = root / 'plan.json'
            plan.write_text(json.dumps({'video': str(base), 'video_identity': {
                'size': stat.st_size, 'mtime_ns': stat.st_mtime_ns}, 'clips': []}))
            out = root / 'result.mp4'
            run('python3', HERE / 'composite.py', '--plan', plan, '--out', out, '--encoder', 'software')
            duration = float(run('ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                 '-show_entries', 'stream=duration', '-of', 'csv=p=0', out))
            self.assertAlmostEqual(duration, 2.002, delta=.04)
            self.assertGreater(pixel(out, .7)[2], 200)
            self.assertGreater(pixel(out, 1.7)[0], 200)

    def test_fractional_cache_shortening_and_preview_phase(self):
        with tempfile.TemporaryDirectory(prefix='graphics-test-') as tmp:
            root = Path(tmp)
            html = root / 'tiny.html'
            html.write_text('''<!doctype html><html><body style="margin:0;background:transparent"><div id="box"
              style="position:absolute;left:100px;top:50px;width:120px;height:80px"></div><script>
              window.setParams=()=>{};window.seek=t=>document.getElementById('box').style.background=t<.3?'red':'lime';
              </script></body></html>''')
            frames, mov = root / 'frames', root / 'overlay.mov'
            def render(duration):
                return json.loads(run('node', HERE / 'render.mjs', '--template', html, '--duration', duration,
                                      '--fps', '30000/1001', '--width', 320, '--height', 180,
                                      '--out', frames, '--mov', mov))
            first = render(.6)
            self.assertEqual(first['frames'], 18)
            self.assertFalse(first['cacheHit'])
            self.assertTrue(render(.6)['cacheHit'])
            self.assertTrue((frames / 'f_0017.png').exists())
            render(.2)
            self.assertFalse((frames / 'f_0017.png').exists())
            self.assertEqual(len(list(frames.glob('f_*.png'))), 6)
            duration = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mov))
            self.assertAlmostEqual(duration, 6 * 1001 / 30000, delta=.01)
            render(.6)
            base = root / 'base.mp4'
            run('ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=blue:s=320x180:r=30000/1001:d=3',
                '-f', 'lavfi', '-i', 'sine=frequency=440:duration=3', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', base)
            stat = base.stat()
            plan = root / 'graphics.json'
            plan.write_text(json.dumps({'video':str(base),'video_identity':{'size':stat.st_size,'mtime_ns':stat.st_mtime_ns},
                                        'clips':[{'asset':str(mov),'start':1,'duration':.6}]}))
            preview = root / 'preview.mp4'
            run('python3', HERE / 'composite.py', '--plan', plan, '--out', preview, '--start', .8, '--duration', 1.2, '--encoder', 'software')
            self.assertGreater(pixel(preview, .05)[2], 200)  # base before overlay
            self.assertGreater(pixel(preview, .3)[0], 200)   # red phase
            self.assertGreater(pixel(preview, .65)[1], 200)  # green phase
            self.assertGreater(pixel(preview, 1)[2], 200)    # no frozen overlay after its end
            mid = root / 'mid.mp4'
            run('python3', HERE / 'composite.py', '--plan', plan, '--out', mid, '--start', 1.4, '--duration', .4, '--encoder', 'software')
            self.assertGreater(pixel(mid, .02)[1], 200)  # mid-preview seeks asset, does not restart red


if __name__ == '__main__':
    unittest.main()
