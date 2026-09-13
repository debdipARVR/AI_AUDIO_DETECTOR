# AcousticShield 2.0 Test Samples Dataset

This folder contains pre-synthesized audio samples calibrated with real-world acoustic physics, adverse transmission channel distortions, and neural vocoder artifacts.

You can drag and drop any of these files directly into the **AcousticShield Streamlit App** (`http://localhost:8550`) to test custom file upload detection.

---

## 📞 Voice & Telephony Samples (24 kHz, 16-bit PCM)
| File Name | Ground Truth | Attributed Engine | Channel Condition | Expected Verdict | Expected Δ SNR |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `01_scam_grandson_elevenlabs_voip.wav` | **AI Clone** | ElevenLabs | VoIP Opus 16kbps | `AI_CLONE` | $+11.2	ext{ dB}$ (Surge) |
| `02_scam_bank_fraud_cartesia_pstn.wav` | **AI Clone** | Cartesia Sonic | PSTN G.711 ($300	ext{--}3400$\,Hz) | `AI_CLONE` | $+10.2	ext{ dB}$ (Surge) |
| `03_scam_ceo_payroll_openvoice.wav` | **AI Clone** | OpenVoice | Clean Studio Line | `AI_CLONE` | $+12.0	ext{ dB}$ (Surge) |
| `04_scam_noisy_street_elevenlabs.wav` | **AI Clone** | ElevenLabs | Noisy Room (+20dB SNR) | `AI_CLONE` | $+11.0	ext{ dB}$ (Surge) |
| `05_authentic_grandson_campus_call.wav` | **Human** | Genuine Vocal Tract | VoIP Opus 16kbps | `AUTHENTIC_HUMAN` | $\le +2.0	ext{ dB}$ (Low) |
| `06_authentic_bbc_radio4_interview.wav` | **Human** | Genuine Vocal Tract | Clean Broadcast Line | `AUTHENTIC_HUMAN` | $\le +0.5	ext{ dB}$ (Low) |
| `07_authentic_landline_family_call.wav` | **Human** | Genuine Vocal Tract | PSTN G.711 ($300	ext{--}3400$\,Hz) | `AUTHENTIC_HUMAN` | $\le +1.8	ext{ dB}$ (Low) |

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
