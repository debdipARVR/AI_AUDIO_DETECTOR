"""
Generates high-fidelity .wav test samples for AcousticShield 2.0.
Can be dragged and dropped into the Streamlit Web Application (Tab 1 and Tab 2).
"""

import os
import sys
import numpy as np
import scipy.io.wavfile as wavfile

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from acousticshield.engine import AcousticResonanceEngine
from acousticshield.music_engine import MusicResonanceEngine

audio_engine = AcousticResonanceEngine()
music_engine = MusicResonanceEngine()

SAMPLE_DIR = os.path.join(PACKAGE_ROOT, "test_samples")
os.makedirs(SAMPLE_DIR, exist_ok=True)

print(f"Generating test samples in: {SAMPLE_DIR}")

# 1. Voice Samples (24 kHz, 16-bit PCM)
voice_scenarios = [
    ("01_scam_grandson_elevenlabs_voip.wav", True, "elevenlabs", "voip_opus", 5.0),
    ("02_scam_bank_fraud_cartesia_pstn.wav", True, "cartesia", "telephone_g711", 5.0),
    ("03_scam_ceo_payroll_openvoice.wav", True, "openvoice", "clean", 4.5),
    ("04_scam_noisy_street_elevenlabs.wav", True, "elevenlabs", "noisy_room", 5.0),
    ("05_authentic_grandson_campus_call.wav", False, "human", "voip_opus", 5.0),
    ("06_authentic_bbc_radio4_interview.wav", False, "human", "clean", 5.0),
    ("07_authentic_landline_family_call.wav", False, "human", "telephone_g711", 4.5)
]

for fname, is_ai, model_name, channel, dur in voice_scenarios:
    sig = audio_engine.generate_synthetic_signal(
        duration_sec=dur,
        sample_rate=24000,
        is_ai=is_ai,
        model_type=model_name,
        channel=channel
    )
    # Convert float32 [-1, 1] to int16
    pcm16 = np.clip(sig * 32767.0, -32768, 32767).astype(np.int16)
    out_p = os.path.join(SAMPLE_DIR, fname)
    wavfile.write(out_p, 24000, pcm16)
    print(f"  [Voice] Generated: {fname} ({dur}s, 24kHz Mono, Channel: {channel})")

# 2. Music Samples (44.1 kHz, 16-bit Stereo PCM)
music_scenarios = [
    ("08_music_suno_v4_synthetic_pop_ballad.wav", True, "suno_v4", 6.0),
    ("09_music_udio_130k_synthetic_electronic.wav", True, "udio_130k", 6.0),
    ("10_music_authentic_symphony_orchestra.wav", False, "orchestra", 6.0),
    ("11_music_authentic_jazz_analog_session.wav", False, "jazz", 6.0)
]

for fname, is_ai, model_name, dur in music_scenarios:
    left, right = music_engine.generate_synthetic_music(
        duration_sec=dur,
        sample_rate=44100,
        is_ai=is_ai,
        model_type=model_name
    )
    pcm_l = np.clip(left * 32767.0, -32768, 32767).astype(np.int16)
    pcm_r = np.clip(right * 32767.0, -32768, 32767).astype(np.int16)
    stereo = np.column_stack((pcm_l, pcm_r))
    out_p = os.path.join(SAMPLE_DIR, fname)
    wavfile.write(out_p, 44100, stereo)
    print(f"  [Music] Generated: {fname} ({dur}s, 44.1kHz Stereo)")

# Create README in test_samples
readme_content = """# AcousticShield 2.0 Test Samples Dataset

This folder contains pre-synthesized audio samples calibrated with real-world acoustic physics, adverse transmission channel distortions, and neural vocoder artifacts.

You can drag and drop any of these files directly into the **AcousticShield Streamlit App** (`http://localhost:8550`) to test custom file upload detection.

---

## 📞 Voice & Telephony Samples (24 kHz, 16-bit PCM)
| File Name | Ground Truth | Attributed Engine | Channel Condition | Expected Verdict | Expected Δ SNR |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `01_scam_grandson_elevenlabs_voip.wav` | **AI Clone** | ElevenLabs | VoIP Opus 16kbps | `AI_CLONE` | $+11.2\text{ dB}$ (Surge) |
| `02_scam_bank_fraud_cartesia_pstn.wav` | **AI Clone** | Cartesia Sonic | PSTN G.711 ($300\text{--}3400$\,Hz) | `AI_CLONE` | $+10.2\text{ dB}$ (Surge) |
| `03_scam_ceo_payroll_openvoice.wav` | **AI Clone** | OpenVoice | Clean Studio Line | `AI_CLONE` | $+12.0\text{ dB}$ (Surge) |
| `04_scam_noisy_street_elevenlabs.wav` | **AI Clone** | ElevenLabs | Noisy Room (+20dB SNR) | `AI_CLONE` | $+11.0\text{ dB}$ (Surge) |
| `05_authentic_grandson_campus_call.wav` | **Human** | Genuine Vocal Tract | VoIP Opus 16kbps | `AUTHENTIC_HUMAN` | $\le +2.0\text{ dB}$ (Low) |
| `06_authentic_bbc_radio4_interview.wav` | **Human** | Genuine Vocal Tract | Clean Broadcast Line | `AUTHENTIC_HUMAN` | $\le +0.5\text{ dB}$ (Low) |
| `07_authentic_landline_family_call.wav` | **Human** | Genuine Vocal Tract | PSTN G.711 ($300\text{--}3400$\,Hz) | `AUTHENTIC_HUMAN` | $\le +1.8\text{ dB}$ (Low) |

---

## 🎵 Music & Song Samples (44.1 kHz, 16-bit Stereo PCM)
| File Name | Ground Truth | Attributed Engine | Physical Phenomenon | Expected Verdict |
| :--- | :---: | :---: | :---: | :---: |
| `08_music_suno_v4_synthetic_pop_ballad.wav` | **AI Music** | Suno AI v4 | Brickwall cutoff at 17.5 kHz, mono-bleed phase collapse | `AI_GENERATED_MUSIC` |
| `09_music_udio_130k_synthetic_electronic.wav` | **AI Music** | Udio 130k | DAC codebook inversion surge, phase dispersion $<10^\circ$ | `AI_GENERATED_MUSIC` |
| `10_music_authentic_symphony_orchestra.wav` | **Authentic** | Acoustic Orchestra | Natural Haas stereo dispersion ($48^\circ$), continuous 22.05 kHz air | `AUTHENTIC_STUDIO_RECORDING` |
| `11_music_authentic_jazz_analog_session.wav` | **Authentic** | Jazz Quartet | Physical instrument body resonance, tape saturation | `AUTHENTIC_STUDIO_RECORDING` |

---

## ⚡ How to Test in Streamlit:
1. Open [http://localhost:8550](http://localhost:8550) in your browser.
2. In **Tab 1 (Voice Scam Interceptor)**: Select *"Custom Audio Upload (.wav, .mp3, .raw)"* and drag any of files `01` through `07`.
3. In **Tab 2 (Music Sentry)**: Switch between presets or upload files `08` through `11`.
4. Click **Run Real-Time Intercept** to view the live 1D comb harmonics, noise floor meter, and export the official **Ed25519 Police Forensic Dossier**.
"""

with open(os.path.join(SAMPLE_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

print(f"Saved dataset guide to: {os.path.join(SAMPLE_DIR, 'README.md')}")
print("All 11 test samples generated successfully!")
