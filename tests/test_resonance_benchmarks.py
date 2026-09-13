"""
AcousticShield 2.0 Test Suite
Automated verification for Voice Scam Interceptor, Music Codec Resonance, and Multimodal Bridge.
"""

import os
import sys
import pytest
import numpy as np

PACKAGE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from acousticshield.engine import AcousticResonanceEngine, ForensicReport
from acousticshield.music_engine import MusicResonanceEngine, MusicForensicReport
from acousticshield.multimodal_bridge import MultimodalForensicBridge
from acousticshield.mcp_server import inspect_audio_authenticity, inspect_music_authenticity, inspect_multimodal_identity


@pytest.fixture
def audio_engine():
    return AcousticResonanceEngine()


@pytest.fixture
def music_engine():
    return MusicResonanceEngine()


@pytest.fixture
def multimodal_bridge():
    return MultimodalForensicBridge()


def test_voice_engine_clean_human(audio_engine):
    sig = audio_engine.generate_synthetic_signal(4.0, sample_rate=24000, is_ai=False, channel="clean")
    report = audio_engine.analyze_audio(audio_array=sig, sample_rate=24000, channel="clean")
    assert report.verdict == "AUTHENTIC_HUMAN"
    assert report.resonance_delta_db < 6.0
    assert report.confidence >= 0.90
    assert report.ed25519_signature.startswith("ed25519:")
    assert report.latency_ms < 500.0


def test_voice_engine_ai_clone(audio_engine):
    sig = audio_engine.generate_synthetic_signal(4.0, sample_rate=24000, is_ai=True, model_type="elevenlabs", channel="clean")
    report = audio_engine.analyze_audio(audio_array=sig, sample_rate=24000, channel="clean")
    assert report.verdict == "AI_CLONE"
    assert report.resonance_delta_db >= 6.0
    assert report.comb_spikes_detected is True
    assert report.confidence >= 0.90
    assert report.latency_ms < 500.0


def test_voice_engine_voip_opus(audio_engine):
    sig = audio_engine.generate_synthetic_signal(4.0, sample_rate=24000, is_ai=True, channel="voip_opus")
    report = audio_engine.analyze_audio(audio_array=sig, sample_rate=24000, channel="voip_opus")
    assert report.verdict == "AI_CLONE"
    assert report.channel_detected == "voip_opus"


def test_voice_engine_telephone_g711(audio_engine):
    sig = audio_engine.generate_synthetic_signal(4.0, sample_rate=24000, is_ai=True, channel="telephone_g711")
    report = audio_engine.analyze_audio(audio_array=sig, sample_rate=24000, channel="telephone_g711")
    assert report.verdict == "AI_CLONE"
    assert report.channel_detected == "telephone_g711"


def test_music_engine_authentic(music_engine):
    left, right = music_engine.generate_synthetic_music(4.0, sample_rate=44100, is_ai=False)
    report = music_engine.analyze_music(audio_left=left, audio_right=right, sample_rate=44100)
    assert report.verdict == "AUTHENTIC_STUDIO_RECORDING"
    assert report.resonance_delta_db < 6.2
    assert report.stereo_phase_dispersion_deg > 15.0
    assert report.confidence >= 0.90
    assert report.latency_ms < 500.0


def test_music_engine_ai_suno(music_engine):
    left, right = music_engine.generate_synthetic_music(4.0, sample_rate=44100, is_ai=True, model_type="suno_v4")
    report = music_engine.analyze_music(audio_left=left, audio_right=right, sample_rate=44100)
    assert report.verdict == "AI_GENERATED_MUSIC"
    assert report.resonance_delta_db >= 6.2
    assert report.ultrasonic_cutoff_khz <= 18.5
    assert report.confidence >= 0.90
    assert report.latency_ms < 500.0


def test_multimodal_bridge_scam_scenario(multimodal_bridge):
    report = multimodal_bridge.analyze_multimodal(
        audio_preset="grandparent_scam",
        image_preset="ai_avatar_scammer",
        channel="voip_opus"
    )
    assert report.final_verdict == "CONFIRMED_MULTIMODAL_SCAM"
    assert report.joint_scam_risk_score >= 0.85
    assert report.image_analyzed is True
    assert report.combined_ed25519_signature.startswith("ed25519:")


def test_mcp_tools():
    resp_audio = inspect_audio_authenticity(preset_case="grandparent_scam")
    assert resp_audio["status"] == "success"
    assert resp_audio["verdict"] == "AI_CLONE"

    resp_music = inspect_music_authenticity(preset_track="suno_song")
    assert resp_music["status"] == "success"
    assert resp_music["verdict"] == "AI_GENERATED_MUSIC"

    resp_mm = inspect_multimodal_identity(audio_preset="grandparent_scam", image_preset="ai_avatar_scammer")
    assert resp_mm["status"] == "success"
    assert resp_mm["final_verdict"] == "CONFIRMED_MULTIMODAL_SCAM"


def test_edge_cases(audio_engine, music_engine):
    # Empty array
    empty_sig = np.array([], dtype=np.float32)
    rep_empty = audio_engine.analyze_audio(audio_array=empty_sig, sample_rate=24000)
    assert rep_empty.verdict in ["AUTHENTIC_HUMAN", "AI_CLONE"]

    # Extreme noise
    noise_sig = np.random.normal(0, 0.9, 24000 * 3).astype(np.float32)
    rep_noise = audio_engine.analyze_audio(audio_array=noise_sig, sample_rate=24000)
    assert rep_noise.latency_ms < 500.0
