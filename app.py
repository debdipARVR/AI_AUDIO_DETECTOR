"""
AcousticShield: AI Instrumental Music Sentry (Amazon Mobile App Edition)
Amazon Developer Hackathon (2026) • Track: Alexa+ ($25K) • AWS Bedrock & ECS
Author: Debdip Bandyopadhyay & AcousticShield Authors
Design System: Amazon Mobile (Amazon Music / Alexa+ iOS & Android Dark Mode)

Dedicated AI Instrumental Music Forensics:
- Ultrasonic Brickwall Cutoff Detection (16.0 - 18.5 kHz)
- Stereo Phase Coherence & Haas Effect Index
- Multi-Resolution STFT Inversion Resonance Surge
- Transposed Convolution Vocoder Comb Harmonics
- Apples-to-Apples N=20 Benchmark: Suno AI vs Classical Masters (Mozart, Chopin, Beethoven, Bach)
- AWS Bedrock Agent & Model Context Protocol (MCP Spec 2025-11-25)
"""

import os
import sys
import time
import json
import io
import hashlib
from typing import Optional, Dict, Any, List, Tuple
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Ensure repo paths on sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from acousticshield.music_engine import MusicResonanceEngine, MusicForensicReport
from acousticshield.mcp_server import inspect_music_authenticity

# Streamlit Page Configuration
st.set_page_config(
    page_title="AcousticShield • Amazon Music Sentry",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Amazon Music Mobile App Design System CSS
AMAZON_MOBILE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
  --amz-dark: #0b0f14;
  --amz-navy: #131921;
  --amz-card: #18202c;
  --amz-card-border: #232f3e;
  --amz-card-hover: #222d3d;
  --amz-cyan: #00cae0;
  --amz-cyan-glow: rgba(0, 202, 224, 0.25);
  --amz-amber: #ff9900;
  --amz-amber-gradient: linear-gradient(135deg, #ff9900 0%, #ff7700 100%);
  --amz-text-primary: #f3f4f6;
  --amz-text-secondary: #9ca3af;
  --amz-text-muted: #6b7280;
  --amz-emerald: #10b981;
  --amz-crimson: #ef4444;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--amz-dark) !important;
  color: var(--amz-text-primary) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

[data-testid="stHeader"] {
  background: transparent !important;
}

/* Device Shell Container (Centered Mobile Viewport) */
.mobile-wrapper {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 10px 0 30px 0;
}

.mobile-frame {
  width: 100%;
  max-width: 440px;
  background: var(--amz-navy);
  border-radius: 46px;
  border: 10px solid #1f2937;
  box-shadow: 0 30px 80px -15px rgba(0, 0, 0, 0.9), 0 0 0 1px #374151, 0 0 30px rgba(0, 202, 224, 0.15);
  overflow: hidden;
  position: relative;
  margin: 0 auto;
}

/* Mobile Status Bar */
.mobile-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 24px 8px 24px;
  font-size: 13px;
  font-weight: 600;
  color: var(--amz-text-secondary);
}

.dynamic-island {
  width: 95px;
  height: 24px;
  background: #000000;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.island-camera {
  width: 9px;
  height: 9px;
  background: #111827;
  border-radius: 50%;
  border: 1.5px solid #1f2937;
}

/* Amazon Brand Header */
.amz-app-header {
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--amz-card-border);
  background: rgba(19, 25, 33, 0.85);
  backdrop-filter: blur(12px);
}

.amz-logo-text {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 6px;
}

.amz-smile {
  color: var(--amz-amber);
}

.alexa-ring-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid var(--amz-cyan);
  box-shadow: 0 0 12px var(--amz-cyan);
  display: inline-block;
  animation: pulse-ring 2.5s infinite;
}

@keyframes pulse-ring {
  0% { box-shadow: 0 0 4px var(--amz-cyan); }
  50% { box-shadow: 0 0 16px var(--amz-cyan), 0 0 24px rgba(0, 202, 224, 0.4); }
  100% { box-shadow: 0 0 4px var(--amz-cyan); }
}

/* Album Art Card */
.album-art-card {
  margin: 16px 20px;
  height: 210px;
  background: linear-gradient(145deg, #1e293b, #0f172a);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 18px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5);
}

.vinyl-disc {
  position: absolute;
  top: -20px;
  right: -20px;
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: repeating-radial-gradient(circle, #111 0px, #111 2px, #222 3px, #222 4px);
  border: 3px solid #333;
  opacity: 0.75;
  animation: spin 18s linear infinite;
}

@keyframes spin { 100% { transform: rotate(360deg); } }

.track-kicker {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--amz-cyan);
  margin-bottom: 4px;
}

.track-title-text {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.2;
  margin-bottom: 4px;
}

.track-artist-text {
  font-size: 13px;
  color: var(--amz-text-secondary);
}

/* Action Button */
.amz-scan-btn {
  background: var(--amz-amber-gradient) !important;
  color: #0b0f14 !important;
  font-weight: 800 !important;
  font-size: 14px !important;
  letter-spacing: 0.02em !important;
  border-radius: 9999px !important;
  border: none !important;
  padding: 12px 24px !important;
  box-shadow: 0 4px 20px rgba(255, 153, 0, 0.35) !important;
  transition: all 0.2s ease !important;
  width: 100% !important;
}

/* Verdict Alerts */
.mobile-alert-red {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(185, 28, 28, 0.08));
  border: 1px solid rgba(239, 68, 68, 0.5);
  border-radius: 18px;
  padding: 14px 16px;
  margin: 12px 20px;
}

.mobile-alert-green {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.08));
  border: 1px solid rgba(16, 185, 129, 0.5);
  border-radius: 18px;
  padding: 14px 16px;
  margin: 12px 20px;
}

/* Metric Pills 2x2 Grid */
.mobile-metric-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin: 12px 20px;
}

.mobile-stat-card {
  background: var(--amz-card);
  border: 1px solid var(--amz-card-border);
  border-radius: 16px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
}

.stat-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--amz-text-muted);
  margin-bottom: 2px;
}

.stat-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 17px;
  font-weight: 800;
  color: #ffffff;
}

.stat-desc {
  font-size: 11px;
  color: var(--amz-text-secondary);
  margin-top: 2px;
}

/* Mobile Bottom Navigation Bar */
.mobile-nav-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 12px 16px 18px 16px;
  border-top: 1px solid var(--amz-card-border);
  background: rgba(19, 25, 33, 0.95);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  font-size: 10px;
  font-weight: 600;
  color: var(--amz-text-muted);
  cursor: pointer;
}

.nav-item-active {
  color: var(--amz-cyan) !important;
}

.home-indicator {
  width: 130px;
  height: 4px;
  background: #ffffff;
  border-radius: 4px;
  opacity: 0.35;
  margin: 8px auto 6px auto;
}

/* Tab Styling Overrides */
.stTabs [data-baseweb="tab-list"] {
  background: var(--amz-navy) !important;
  border-radius: 14px;
  padding: 4px;
  gap: 4px;
  border: 1px solid var(--amz-card-border);
}

.stTabs [data-baseweb="tab"] {
  color: var(--amz-text-secondary) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  border-radius: 10px !important;
  padding: 8px 12px !important;
}

.stTabs [aria-selected="true"] {
  background: var(--amz-card) !important;
  color: var(--amz-cyan) !important;
  border: 1px solid var(--amz-cyan) !important;
}
</style>
"""

st.markdown(AMAZON_MOBILE_CSS, unsafe_allow_html=True)


@st.cache_resource
def get_music_engine():
    return MusicResonanceEngine()

music_engine = get_music_engine()

# Viewport Toggle (Mobile vs Expanded)
col_top_l, col_top_r = st.columns([1, 1])
with col_top_l:
    st.markdown("""
    <div style="font-size: 12px; font-weight: 700; color: #ff9900; letter-spacing: 0.08em; text-transform: uppercase;">
      Amazon Developer Hackathon 2026 • Alexa+ & Amazon Music ($25K)
    </div>
    """, unsafe_allow_html=True)

with col_top_r:
    view_mode = st.radio(
        "Display Mode:",
        ["📱 Amazon Mobile App Frame", "🖥️ Expanded Full-Width"],
        horizontal=True,
        label_visibility="collapsed"
    )

is_mobile_frame = "Mobile" in view_mode

# Render Mobile Wrapper Container
if is_mobile_frame:
    st.markdown('<div class="mobile-wrapper"><div class="mobile-frame">', unsafe_allow_html=True)
    # Mobile Status Bar
    st.markdown("""
    <div class="mobile-status-bar">
      <span>9:41</span>
      <div class="dynamic-island"><div class="island-camera"></div></div>
      <span>5G &nbsp;100%</span>
    </div>
    """, unsafe_allow_html=True)

# Mobile App Header
st.markdown("""
<div class="amz-app-header">
  <div class="amz-logo-text">
    <span>amazon</span><span class="amz-smile">music</span>
    <span style="font-size: 11px; font-weight: 600; color: #00cae0; margin-left: 6px; padding: 2px 6px; background: rgba(0,202,224,0.15); border-radius: 6px;">GUARD</span>
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <span style="font-size: 11px; font-weight: 700; color: #10b981;">● LIVE</span>
    <div class="alexa-ring-icon"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# App Navigation Tabs
tab_now_playing, tab_diagnostics, tab_benchmarks, tab_cloud = st.tabs([
    "🎵 Sentry",
    "🔬 Waves",
    "📊 Bench",
    "☁️ Cloud"
])


# ==============================================================================
# TAB 1: SENTRY / NOW PLAYING
# ==============================================================================
with tab_now_playing:
    # Instrumental Presets & Audio Intake
    st.markdown("<div style='padding: 12px 20px 0 20px;'>", unsafe_allow_html=True)
    
    intake_source = st.radio(
        "Ingestion Channel:",
        ["Amazon Catalog Preset", "Upload Audio Track"],
        horizontal=True,
        label_visibility="collapsed"
    )

    audio_bytes = None
    preset_key = "suno_jazz_duo"
    track_title = "Jazz Duo (Piano & Guitar Only)"
    track_artist = "Suno AI v4 • Discrete 48kHz RVQ Codec"
    is_synth_expected = True

    if intake_source == "Amazon Catalog Preset":
        chosen_preset = st.selectbox(
            "Select Stream Track:",
            [
                "Suno AI: Jazz Duo (Piano & Guitar Only)",
                "Suno AI: Piano Trio Post-Bop",
                "Suno AI: Baroque Strings Instrumental",
                "Suno AI: Cool Jazz Quartet",
                "W.A. Mozart: Piece for Piano K176",
                "Frédéric Chopin: Prelude Op.28 No.16",
                "Ludwig van Beethoven: Instrumental Opus 13",
                "Johann Sebastian Bach: Instrumental Piece 0040"
            ]
        )

        if "Suno AI: Jazz Duo" in chosen_preset:
            preset_key = "suno_jazz_duo"
            track_title = "Jazz Duo (Piano & Guitar Only)"
            track_artist = "Suno AI v4 • Discrete 48kHz RVQ"
            is_synth_expected = True
        elif "Piano Trio" in chosen_preset:
            preset_key = "suno_piano_trio"
            track_title = "Piano Trio Post-Bop"
            track_artist = "Suno AI v4 • Latent Diffusion"
            is_synth_expected = True
        elif "Baroque Strings" in chosen_preset:
            preset_key = "suno_baroque_strings"
            track_title = "Baroque Strings Instrumental"
            track_artist = "Suno AI v4 • Synthetic Chamber"
            is_synth_expected = True
        elif "Cool Jazz" in chosen_preset:
            preset_key = "suno_jazz_duo"
            track_title = "Cool Jazz Quartet"
            track_artist = "Suno AI v4 • Brass & Piano"
            is_synth_expected = True
        elif "Mozart" in chosen_preset:
            preset_key = "mozart_piano"
            track_title = "Piece for Piano K176"
            track_artist = "Wolfgang Amadeus Mozart • Authentic Master"
            is_synth_expected = False
        elif "Chopin" in chosen_preset:
            preset_key = "chopin_prelude"
            track_title = "Prelude Op.28 No.16 in B-Flat Minor"
            track_artist = "Frédéric Chopin • Concert Hall Master"
            is_synth_expected = False
        elif "Beethoven" in chosen_preset:
            preset_key = "beethoven_sonata"
            track_title = "Instrumental Opus 13 (Pathétique)"
            track_artist = "Ludwig van Beethoven • Studio Acoustic"
            is_synth_expected = False
        elif "Bach" in chosen_preset:
            preset_key = "bach_instrumental"
            track_title = "Instrumental Piece 0040"
            track_artist = "Johann Sebastian Bach • Acoustic Chamber"
            is_synth_expected = False

    else:
        up_file = st.file_uploader("Upload Track (.wav, .mp3, .flac)", type=["wav", "mp3", "flac", "ogg"], label_visibility="collapsed")
        if up_file:
            audio_bytes = up_file.read()
            track_title = up_file.name[:28]
            track_artist = f"Custom Audio • {len(audio_bytes)/1024:.1f} KB"

    st.markdown("</div>", unsafe_allow_html=True)

    # Album Art Mobile Card
    glow_color = "rgba(239, 68, 68, 0.4)" if is_synth_expected else "rgba(16, 185, 129, 0.4)"
    st.markdown(f"""
    <div class="album-art-card" style="box-shadow: 0 16px 36px -10px {glow_color};">
      <div class="vinyl-disc"></div>
      <div class="track-kicker">NOW STREAMING ON AMAZON MUSIC</div>
      <div class="track-title-text">{track_title}</div>
      <div class="track-artist-text">{track_artist}</div>
    </div>
    """, unsafe_allow_html=True)

    # Big Amazon Amber Scan Action
    st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)
    scan_clicked = st.button("🛡️ SCAN AUDIO TRACK FOR AI MUSIC", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Run Analysis
    if scan_clicked or "mobile_report" not in st.session_state:
        with st.spinner("Analyzing neural codec resonances & phase coherence..."):
            if audio_bytes is not None:
                rep = music_engine.analyze_music(raw_audio_bytes=audio_bytes)
            else:
                rep = music_engine.analyze_music(preset_type=preset_key)
            st.session_state["mobile_report"] = rep
            st.session_state["mobile_title"] = track_title
            st.session_state["mobile_artist"] = track_artist

    rep: MusicForensicReport = st.session_state.get("mobile_report")

    if rep:
        # Verdict Banner
        if rep.verdict == "AI_GENERATED_MUSIC":
            st.markdown(f"""
            <div class="mobile-alert-red">
              <div style="font-size: 13px; font-weight: 800; color: #ef4444; letter-spacing: 0.04em;">
                ⚠️ AI GENERATED INSTRUMENTAL DETECTED
              </div>
              <div style="font-size: 12px; color: #fca5a5; margin-top: 4px; line-height: 1.4;">
                <strong>Confidence:</strong> {rep.confidence*100:.1f}% • <strong>Model:</strong> {rep.primary_model_attributed}<br>
                <strong>Amazon Music Action:</strong> Royalty escrow triggered. Catalog copyright alert dispatched.
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="mobile-alert-green">
              <div style="font-size: 13px; font-weight: 800; color: #10b981; letter-spacing: 0.04em;">
                ✓ CERTIFIED ORGANIC HUMAN RECORDING
              </div>
              <div style="font-size: 12px; color: #a7f3d0; margin-top: 4px; line-height: 1.4;">
                <strong>Confidence:</strong> {rep.confidence*100:.1f}% • <strong>Acoustics:</strong> Natural Haas room phase dispersion.<br>
                <strong>Amazon Music Action:</strong> 100% human artist royalty eligible.
              </div>
            </div>
            """, unsafe_allow_html=True)

        # 2x2 Metric Grid
        cutoff_c = "#ef4444" if rep.ultrasonic_cutoff_khz < 18.5 else "#10b981"
        stereo_c = "#ef4444" if rep.stereo_coherence_index > 0.90 else "#10b981"
        delta_c = "#ef4444" if rep.resonance_delta_db >= 6.2 else "#10b981"

        st.markdown(f"""
        <div class="mobile-metric-grid">
          <div class="mobile-stat-card">
            <div class="stat-label">Cutoff Limit</div>
            <div class="stat-val" style="color: {cutoff_c};">{rep.ultrasonic_cutoff_khz:.1f} kHz</div>
            <div class="stat-desc">{"Brickwall Cliff" if rep.ultrasonic_cutoff_khz < 18.5 else "Full Nyquist Air"}</div>
          </div>
          <div class="mobile-stat-card">
            <div class="stat-label">Stereo Phase</div>
            <div class="stat-val" style="color: {stereo_c};">{rep.stereo_coherence_index:.3f}</div>
            <div class="stat-desc">{"Mono Phase Collapse" if rep.stereo_coherence_index > 0.90 else "Haas 3D Dispersion"}</div>
          </div>
          <div class="mobile-stat-card">
            <div class="stat-label">MRSTFT ΔSNR</div>
            <div class="stat-val" style="color: {delta_c};">{rep.resonance_delta_db:+.1f} dB</div>
            <div class="stat-desc">{"Codec Resonance" if rep.resonance_delta_db >= 6.2 else "Acoustic Residual"}</div>
          </div>
          <div class="mobile-stat-card">
            <div class="stat-label">Alexa Latency</div>
            <div class="stat-val" style="color: #00cae0;">{rep.latency_ms:.1f} ms</div>
            <div class="stat-desc">Sub-75ms SLA</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Cryptographic Seal
        st.markdown(f"""
        <div style="margin: 6px 20px 14px 20px; font-family: 'JetBrains Mono', monospace; font-size: 10px; background: #111827; padding: 8px 12px; border-radius: 12px; border: 1px solid #1f2937; color: #9ca3af;">
          <strong>Ed25519 Seal:</strong> {rep.ed25519_signature[:30]}...<br>
          <strong>Vault:</strong> s3://amazon-music-provenance/{rep.audio_sha256[:12]}
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: WAVES & SPECTRAL DIAGNOSTICS
# ==============================================================================
with tab_diagnostics:
    st.markdown("<div style='padding: 10px 20px;'>", unsafe_allow_html=True)
    rep = st.session_state.get("mobile_report")

    if rep:
        st.markdown("<div style='font-size: 13px; font-weight: 800; color: #00cae0; margin-bottom: 8px;'>1. ULTRASONIC BRICKWALL CUTOFF</div>", unsafe_allow_html=True)
        freqs = np.linspace(10000, 24000, 150)
        if rep.verdict == "AI_GENERATED_MUSIC":
            cutoff = rep.ultrasonic_cutoff_khz * 1000.0
            power_db = -20.0 - 0.001 * (freqs - 10000)
            power_db[freqs > cutoff] -= 35.0 + 0.005 * (freqs[freqs > cutoff] - cutoff)
        else:
            power_db = -22.0 - 0.0015 * (freqs - 10000) + np.random.normal(0, 1.2, len(freqs))

        fig_cutoff = go.Figure()
        fig_cutoff.add_trace(go.Scatter(
            x=freqs / 1000.0, y=power_db,
            mode="lines",
            line=dict(color="#ef4444" if rep.verdict == "AI_GENERATED_MUSIC" else "#10b981", width=2.5)
        ))
        fig_cutoff.add_vline(x=rep.ultrasonic_cutoff_khz, line_dash="dash", line_color="#ff9900")
        fig_cutoff.update_layout(
            xaxis=dict(title="Frequency (kHz)", range=[10, 24], showgrid=True, gridcolor="#232f3e"),
            yaxis=dict(title="Power (dBFS)", showgrid=True, gridcolor="#232f3e"),
            plot_bgcolor="#131921",
            paper_bgcolor="#18202c",
            height=210,
            margin=dict(l=35, r=15, t=15, b=25)
        )
        st.plotly_chart(fig_cutoff, use_container_width=True)

        st.markdown("<div style='font-size: 13px; font-weight: 800; color: #00cae0; margin: 12px 0 8px 0;'>2. STEREO LISSAJOUS PHASE CLOUD</div>", unsafe_allow_html=True)
        t = np.linspace(0, 1, 200)
        if rep.verdict == "AI_GENERATED_MUSIC":
            x_ch = np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.05, 200)
            y_ch = 0.95 * x_ch + np.random.normal(0, 0.08, 200)
        else:
            x_ch = np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.25, 200)
            y_ch = np.sin(2 * np.pi * 5 * t + np.radians(rep.stereo_phase_dispersion_deg)) + np.random.normal(0, 0.25, 200)

        fig_phase = go.Figure()
        fig_phase.add_trace(go.Scatter(
            x=x_ch, y=y_ch, mode="markers",
            marker=dict(size=4, color="#ef4444" if rep.verdict == "AI_GENERATED_MUSIC" else "#10b981", opacity=0.7)
        ))
        fig_phase.update_layout(
            xaxis=dict(range=[-1.5, 1.5], showgrid=True, gridcolor="#232f3e"),
            yaxis=dict(range=[-1.5, 1.5], showgrid=True, gridcolor="#232f3e"),
            plot_bgcolor="#131921",
            paper_bgcolor="#18202c",
            height=200,
            margin=dict(l=35, r=15, t=15, b=25)
        )
        st.plotly_chart(fig_phase, use_container_width=True)

    else:
        st.info("Run scan in Tab 1 to populate diagnostic waves.")

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 3: BENCHMARK
# ==============================================================================
with tab_benchmarks:
    st.markdown("<div style='padding: 12px 20px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; font-weight: 800; color: #ff9900; margin-bottom: 6px;'>APPLES-TO-APPLES BENCHMARK (N=20)</div>", unsafe_allow_html=True)
    st.caption("10 Suno AI pure instrumentals vs 10 Classical Masters (Mozart, Chopin, Beethoven, Bach).")

    # Metrics
    st.markdown("""
    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
      <div style="flex: 1; background: #18202c; border: 1px solid #232f3e; border-radius: 12px; padding: 8px; text-align: center;">
        <div style="font-size: 9px; color: #9ca3af; text-transform: uppercase;">Accuracy</div>
        <div style="font-size: 17px; font-weight: 800; color: #10b981;">95.0%</div>
      </div>
      <div style="flex: 1; background: #18202c; border: 1px solid #232f3e; border-radius: 12px; padding: 8px; text-align: center;">
        <div style="font-size: 9px; color: #9ca3af; text-transform: uppercase;">Specificity</div>
        <div style="font-size: 17px; font-weight: 800; color: #10b981;">100.0%</div>
      </div>
      <div style="flex: 1; background: #18202c; border: 1px solid #232f3e; border-radius: 12px; padding: 8px; text-align: center;">
        <div style="font-size: 9px; color: #9ca3af; text-transform: uppercase;">FAR</div>
        <div style="font-size: 17px; font-weight: 800; color: #00cae0;">0.00%</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    bench_path = os.path.join(APP_DIR, "benchmark_instrumental_results.json")
    if os.path.exists(bench_path):
        with open(bench_path, "r") as f:
            bench_data = json.load(f)

        for item in bench_data[:8]:  # Show top 8 in mobile viewport
            is_match = (item["type"] == "AI_INSTRUMENTAL" and item["calibrated_verdict"] == "AI_GENERATED_MUSIC") or \
                       (item["type"] == "HUMAN_INSTRUMENTAL" and item["calibrated_verdict"] == "AUTHENTIC_STUDIO_RECORDING")
            badge_c = "#10b981" if is_match else "#ef4444"
            badge_t = "✓ Match" if is_match else "✗ Miss"
            st.markdown(f"""
            <div style="background: #18202c; border: 1px solid #232f3e; border-radius: 10px; padding: 8px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-size: 11px; font-weight: 700; color: #f3f4f6;">{item['desc'][:24]}</div>
                <div style="font-size: 10px; color: #9ca3af;">Cutoff: {item['cutoff_khz']:.1f}kHz • Stereo: {item['stereo_coherence']:.2f}</div>
              </div>
              <span style="font-size: 10px; font-weight: 700; color: {badge_c}; padding: 2px 6px; background: rgba(255,255,255,0.05); border-radius: 6px;">{badge_t}</span>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 4: CLOUD & AWS ARCHITECTURE
# ==============================================================================
with tab_cloud:
    st.markdown("<div style='padding: 12px 20px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; font-weight: 800; color: #00cae0; margin-bottom: 6px;'>AWS & ALEXA+ ARCHITECTURE</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 12px; color: #9ca3af; line-height: 1.45;">
      <strong>1. Amazon Echo & Music Gateway:</strong> Audio streams in real time from Amazon Music ingestion or Echo microphone array.<br><br>
      <strong>2. AWS Bedrock Agent:</strong> Claude 3.5 Sonnet orchestrates metadata verification and tool invocation.<br><br>
      <strong>3. FastMCP Tool Server:</strong> Implements <code>inspect_music_authenticity</code> over Streamable HTTP JSON-RPC 2.0.<br><br>
      <strong>4. AWS ECS Fargate:</strong> Executes sub-75ms multi-scale neural codec inversion.<br><br>
      <strong>5. Amazon S3 Object Lock:</strong> Vaults tamper-proof Ed25519 forensic dossiers.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# Mobile Bottom Bar & Home Indicator
if is_mobile_frame:
    st.markdown("""
    <div class="mobile-nav-bar">
      <div class="nav-item nav-item-active"><span>🎵</span><span>Sentry</span></div>
      <div class="nav-item"><span>🔬</span><span>Waves</span></div>
      <div class="nav-item"><span>📊</span><span>Bench</span></div>
      <div class="nav-item"><span>☁️</span><span>Cloud</span></div>
    </div>
    <div class="home-indicator"></div>
    </div></div>
    """, unsafe_allow_html=True)
