import array
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import montage


class MontageTests(unittest.TestCase):
    def test_duck_has_smooth_edges_and_no_double_duck(self):
        expression = montage.duck_expression([(1, 2), (1.5, 2.4)])
        result = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
            'aevalsrc=0.5:s=48000:d=4', '-af', f"aeval=exprs='val(0)*{expression}'",
            '-f', 'f32le', '-'], capture_output=True, check=True)
        samples = array.array('f', result.stdout)
        self.assertLess(max(abs(b-a) for a,b in zip(samples,samples[1:])), .0001)
        self.assertAlmostEqual(samples[int(1.7*48000)], .5*10**(-12/20), places=5)
        self.assertAlmostEqual(samples[int(3.5*48000)], .5, places=5)
        self.assertGreater(samples[int(2.7*48000)], samples[int(2.5*48000)])

    def test_picture_order_dialogue_mapping_and_music_revision(self):
        with tempfile.TemporaryDirectory(prefix='teaser-test-') as temp:
            root = Path(temp)
            for color in ('red', 'blue'):
                montage.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color={color}:s=320x180:r=30:d=3',
                             '-f', 'lavfi', '-i', 'sine=frequency=440:duration=3', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', root / f'{color}.mp4'])
            montage.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=green:s=320x180', '-frames:v', '1', root / 'card.png'])
            transcript = root / 'speech.json'
            transcript.write_text(json.dumps({'segments':[{'words':[{'word':'hello','start':.2,'end':.4},{'word':'boundary','start':.9,'end':1.2}]}]}))
            plan = {'fps':'30','width':320,'height':180,'shots':[
                {'asset':str(root/'red.mp4'),'source_start':0,'duration':1},
                {'asset':str(root/'blue.mp4'),'source_start':0,'duration':1},
                {'asset':str(root/'card.png'),'duration':1}],
                'audio':[{'role':'dialogue','asset':str(root/'red.mp4'),'source_start':0,'start':.5,'duration':1,'transcript':str(transcript)}]}
            path, output = root/'plan.json', root/'teaser.mp4'
            path.write_text(json.dumps(plan))
            def render():
                return json.loads(montage.run(['python3', Path(montage.__file__).resolve(), '--plan', path, '--out', output, '--encoder', 'software']))
            first = render()
            self.assertEqual(first['duration'], 3)
            self.assertFalse(any(s['cache_hit'] for s in first['shots']))
            mapped = json.loads(output.with_suffix('.transcript.json').read_text())
            self.assertAlmostEqual(mapped['segments'][0]['words'][0]['start'], .7)
            self.assertEqual(len(mapped['boundary_words_for_review']), 1)
            for t, channel in ((.5,0),(1.5,2),(2.5,1)):
                rgb = subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(output),'-frames:v','1','-vf','scale=1:1','-f','rawvideo','-pix_fmt','rgb24','-'], capture_output=True,check=True).stdout
                self.assertEqual(rgb.index(max(rgb)), channel)
            def energy(t):
                data=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-t','0.1','-i',str(output),'-vn','-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True).stdout
                return sum(abs(x) for x in array.array('h',data))
            self.assertLess(energy(.1), energy(.8)*.01)
            plan['audio'].append({'role':'music','asset':str(root/'blue.mp4'),'source_start':0,'start':0,'duration':3,'gain_db':-24})
            path.write_text(json.dumps(plan))
            second=render()
            self.assertTrue(all(s['cache_hit'] for s in second['shots']))
            self.assertGreater(energy(.1), 0)


if __name__ == '__main__':
    unittest.main()
