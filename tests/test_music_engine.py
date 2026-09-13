import unittest
import numpy as np
import sys
import os

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from acousticshield.music_engine import MusicResonanceEngine, MusicForensicReport


class TestMusicEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MusicResonanceEngine()

    def test_ai_instrumental_preset_detection(self):
        # Test Suno AI Jazz Duo preset
        report = self.engine.analyze_music(preset_type="suno_jazz_duo")
        self.assertIsInstance(report, MusicForensicReport)
        self.assertEqual(report.verdict, "AI_GENERATED_MUSIC")
        self.assertGreaterEqual(report.confidence, 0.90)
        self.assertLessEqual(report.ultrasonic_cutoff_khz, 18.5)
        self.assertEqual(report.action_recommended, "FLAG_AI_SONG_COPYRIGHT_INFRINGEMENT")

    def test_authentic_classical_preset_detection(self):
        # Test Mozart Piano K176 preset
        report = self.engine.analyze_music(preset_type="mozart_piano")
        self.assertIsInstance(report, MusicForensicReport)
        self.assertEqual(report.verdict, "AUTHENTIC_STUDIO_RECORDING")
        self.assertGreaterEqual(report.confidence, 0.90)
        self.assertGreaterEqual(report.ultrasonic_cutoff_khz, 20.0)
        self.assertEqual(report.action_recommended, "VERIFY_ORGANIC_ROYALTY_ELIGIBLE")

    def test_calibrated_decision_boundaries(self):
        # Synthesize audio with steep cutoff at 16kHz
        sr = 44100
        n_samples = sr * 3
        t = np.linspace(0, 3, n_samples)
        # 16kHz brickwall
        sig = np.sin(2 * np.pi * 440 * t)
        fft_sig = np.fft.rfft(sig)
        freqs = np.fft.rfftfreq(n_samples, 1.0 / sr)
        fft_sig[freqs > 16000] = 0.0
        filtered = np.fft.irfft(fft_sig, n=n_samples)

        rep = self.engine.analyze_music(audio_left=filtered, audio_right=filtered, sample_rate=sr)
        self.assertEqual(rep.verdict, "AI_GENERATED_MUSIC")


if __name__ == "__main__":
    unittest.main()
