"""Meaningful timeline and synthetic-media checks; no ASR download or real footage required."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import pipeline as p


class TimelineTests(unittest.TestCase):
    def test_source_order_and_ambiguous_endings(self):
        files = p.ordered(['topic_outtro.mp4', 'part10.mp4', 'topic_introTake.mp4', 'part2.mp4', 'part.mp4'])
        self.assertEqual([x.name for x in files], ['topic_introTake.mp4', 'part.mp4', 'part2.mp4', 'part10.mp4', 'topic_outtro.mp4'])
        with self.assertRaises(ValueError):
            p.ordered(['topic_outro.mp4', 'endcard.mp4'])

    def test_union_and_speed(self):
        segments = p.make_segments(10, [{"start": 1, "end": 3}, {"start": 2, "end": 4}],
                                   [{"start": 5, "end": 7, "speed": 2}])
        self.assertEqual(sum((s["source_end"] - s["source_start"]) / s["speed"] for s in segments), 6)
        self.assertFalse(any(s["source_start"] < 4 and s["source_end"] > 1 for s in segments))

    def test_mapping_never_snaps_a_deleted_take(self):
        manifest = {"segments": [{"clip_id": "a", "source_start": 2, "source_end": 4, "speed": 2,
                                   "output_start": 3, "output_end": 4}]}
        self.assertEqual(p.mapped_time(manifest, "a", 3)["time"], 3.5)
        self.assertIsNone(p.mapped_time(manifest, "a", 0, .3))
        self.assertEqual(p.mapped_time(manifest, "a", 1.9, .15)["time"], 3)
        self.assertTrue(p.mapped_time(manifest, "a", 1.9, .15)["snapped"])
        self.assertIsNone(p.mapped_time(manifest, "b", 3))

    def test_invalid_ranges(self):
        with self.assertRaises(ValueError):
            p.make_segments(5, [{"start": -1, "end": 1}], [])
        with self.assertRaises(ValueError):
            p.make_segments(5, [], [{"start": 0, "end": 3, "speed": 2}, {"start": 2, "end": 4, "speed": 2}])
        for fps in ("0", "30000", "nan"):
            with self.assertRaises(ValueError):
                p.rate(fps)


class MediaTests(unittest.TestCase):
    def test_cached_multiclip_render_and_mapped_words(self):
        with tempfile.TemporaryDirectory(prefix="video-pipeline-test-") as temp:
            root = Path(temp)
            script = Path(p.__file__).resolve()
            def cli(*args):
                return p.run(["python3", script, *args])
            sources = []
            for color in ("red", "blue"):
                source = root / f"{color}.mp4"
                p.ffmpeg("-v", "error", "-f", "lavfi", "-i", f"color=c={color}:s=320x180:r=30:d=4",
                         "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=4",
                         "-af", "volume=enable='between(t,1,2.5)':volume=0", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", source)
                sources.append(source)
            work = root / "work"
            cli("analyze", *sources, "--work", work, "--mode", "talking-head", "--skip-transcript")
            analysis = p.load(work / "analysis.json")
            self.assertTrue(all(c["silences"] for c in analysis["clips"]))
            self.assertFalse((work / "proxy.mp4").exists())
            cli("analyze", *sources, "--work", work, "--mode", "talking-head", "--skip-transcript")
            analysis = p.load(work / "analysis.json")
            self.assertTrue(all(t["audio_cache_hit"] and t["analysis_cache_hit"] for t in analysis["timings"]))
            transcript = root / "transcript.json"
            p.save(transcript, {"segments": [{"words": [
                {"word": "keep", "start": .2, "end": .5},
                {"word": "delete", "start": 1.2, "end": 1.5},
                {"word": "boundary", "start": .9, "end": 1.1},
                {"word": "fast", "start": 2.2, "end": 2.6}]}]})
            analysis["clips"][0]["transcript"] = str(transcript)
            p.save(work / "analysis.json", analysis)
            decisions = {"clips": [{"id": c["id"], "cuts": [], "speeds": []} for c in analysis["clips"]]}
            decisions["clips"][0].update(cuts=[{"start": 1, "end": 2}], speeds=[{"start": 2, "end": 3, "speed": 2}])
            p.save(work / "decisions.json", decisions)
            manifest_path = work / "edit.json"
            cli("build", "--analysis", work / "analysis.json", "--decisions", work / "decisions.json", "--fps", "30000/1001", "--out", manifest_path)
            manifest = p.load(manifest_path)
            self.assertAlmostEqual(manifest["duration"], 6.5, delta=.04)
            mapped = p.load(work / "transcript.output.json")
            self.assertEqual([w["word"] for w in mapped["segments"][0]["words"]], ["keep", "fast"])
            self.assertEqual(mapped["removed_words"][0]["word"], "delete")
            self.assertEqual(mapped["boundary_words_for_review"][0]["word"], "boundary")
            self.assertAlmostEqual(mapped["segments"][0]["words"][1]["end"] - mapped["segments"][0]["words"][1]["start"], .2)
            output = root / "cut.mp4"
            cli("render", "--manifest", manifest_path, "--out", output, "--encoder", "software")
            metadata = p.probe(output)
            self.assertAlmostEqual(metadata["duration"], manifest["duration"], delta=.04)
            self.assertEqual((metadata["width"], metadata["height"]), (320, 180))
            # The second source must appear after the mapped first-source duration.
            seam = next(s["output_start"] for s in manifest["segments"] if s["clip_id"] == analysis["clips"][1]["id"])
            raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(seam + .2), "-i", str(output),
                                  "-frames:v", "1", "-vf", "scale=1:1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
            expected = Path(analysis["clips"][1]["source"]).stem
            self.assertGreater(raw[0 if expected == "red" else 2], 200)
            cli("render", "--manifest", manifest_path, "--out", output, "--encoder", "software")
            self.assertTrue(all(r["cache_hit"] for r in p.load(output.with_suffix(".render.json"))["parts"]))
            # Tampering with the manifest cannot silently change rendered timing.
            changed = copy.deepcopy(manifest)
            changed["segments"][0]["speed"] = 3
            p.save(manifest_path, changed)
            with self.assertRaises(RuntimeError):
                cli("render", "--manifest", manifest_path, "--out", output, "--encoder", "software")


if __name__ == "__main__":
    unittest.main()
