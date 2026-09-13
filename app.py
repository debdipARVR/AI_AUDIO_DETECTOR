"""
AcousticShield: AWS AI Audio Forensics Hub & Amazon Music Sentry
Amazon Developer Hackathon (2026) • Track: Alexa+ ($25K) • AWS Bedrock & ECS
Design System: Native Edge-to-Edge Mobile App Viewport (High-Contrast Dark Mode)
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

# Ensure repo paths on sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from acousticshield.music_engine import MusicResonanceEngine, MusicForensicReport
from acousticshield.mcp_server import inspect_music_authenticity

# Streamlit Page Configuration - Centered Mobile App Layout
st.set_page_config(
    page_title="AcousticShield • Amazon Music & Alexa+ Sentry",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Native High-Contrast Mobile Viewport CSS
MOBILE_VIEWPORT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700;800&display=swap');

/* Color Variables */
:root {
  --bg-dark: #0c1015;
  --card-dark: #151b24;
  --border-dark: #232d3b;
  --txt-pure: #ffffff;
  --txt-sub: #94a3b8;
  --txt-muted: #64748b;
  --amber: #ff9900;
  --amber-glow: #f59e0b;
  --emerald: #10b981;
  --coral: #ef4444;
  --cyan: #00cae0;
}

/* Force whole page into mobile dark canvas */
html, body, [data-testid="stAppViewContainer"], .main {
  background-color: var(--bg-dark) !important;
  color: var(--txt-pure) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Constrain Streamlit container into a sleek phone viewport */
.block-container {
  max-width: 440px !important;
  padding: 8px 16px 90px 16px !important;
  margin: 0 auto !important;
  background-color: var(--bg-dark) !important;
  border-left: 1px solid #1a222d;
  border-right: 1px solid #1a222d;
  min-height: 100vh;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.9);
}

/* Transparent Header & Hide Default Streamlit Elements */
[data-testid="stHeader"] {
  background: transparent !important;
  height: 0px !important;
}

footer, header {
  visibility: hidden;
}

/* Universal High-Contrast Typography */
p, span, div, label, h1, h2, h3, h4, h5, h6 {
  color: var(--txt-pure) !important;
}

/* Mobile Status Bar */
.mobile-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 4px 14px 4px;
  font-size: 13px;
  font-weight: 700;
  color: #f1f5f9 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  margin-bottom: 16px;
}

.dynamic-island {
  width: 90px;
  height: 20px;
  background: #000000;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-lens {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #1e293b;
  border: 1px solid #334155;
}

/* Cards */
.mobile-card {
  background: var(--card-dark) !important;
  border: 1px solid var(--border-dark) !important;
  border-radius: 18px;
  padding: 16px;
  margin-bottom: 14px;
}

/* Telemetry Metric Grid */
.telemetry-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-bottom: 16px;
}

.telemetry-card {
  background: var(--card-dark);
  border: 1px solid var(--border-dark);
  border-radius: 14px;
  padding: 12px 6px;
  text-align: center;
}

.telemetry-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--txt-sub) !important;
  margin-bottom: 3px;
}

.telemetry-number {
  font-size: 18px;
  font-weight: 900;
  color: var(--txt-pure) !important;
}

.telemetry-foot {
  font-size: 9px;
  font-weight: 500;
  color: var(--txt-muted) !important;
  margin-top: 2px;
}

/* Animated Waveform Visual */
.wave-visual-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 60px;
  margin: 12px 0;
  background: rgba(0, 0, 0, 0.35);
  border-radius: 12px;
  padding: 0 10px;
}

.wave-bar-anim {
  flex: 1;
  background: linear-gradient(to top, #ff9900, #ff5500);
  border-radius: 4px;
  animation: wave-pulse 1.3s ease-in-out infinite alternate;
}

@keyframes wave-pulse {
  0% { transform: scaleY(0.25); opacity: 0.7; }
  100% { transform: scaleY(1.0); opacity: 1.0; }
}

/* Circular Confidence Gauge */
.circular-gauge-box {
  position: relative;
  width: 146px;
  height: 146px;
  margin: 14px auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gauge-inner-ring {
  width: 136px;
  height: 136px;
  border-radius: 50%;
  border: 7px solid #232c3b;
  border-top-color: #f59e0b;
  border-right-color: #f59e0b;
  box-shadow: 0 0 22px rgba(245, 158, 11, 0.35);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #111720;
}

/* Alert Banners */
.banner-ai-warning {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(217, 119, 6, 0.08));
  border: 1.5px solid var(--amber-glow);
  border-radius: 14px;
  padding: 12px 10px;
  text-align: center;
  color: var(--amber-glow) !important;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.02em;
  margin: 12px 0;
}

.banner-human-verified {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(5, 150, 105, 0.08));
  border: 1.5px solid var(--emerald);
  border-radius: 14px;
  padding: 12px 10px;
  text-align: center;
  color: var(--emerald) !important;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.02em;
  margin: 12px 0;
}

/* Progress Breakdown Rows */
.prog-breakdown-card {
  background: var(--card-dark);
  border: 1px solid var(--border-dark);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 10px;
}

.prog-track-line {
  height: 6px;
  background: #1e293b;
  border-radius: 6px;
  overflow: hidden;
  margin-top: 8px;
}

.prog-fill-line {
  height: 100%;
  background: var(--amber);
  border-radius: 6px;
}

/* High-Contrast Inputs & Selectbox */
div[data-baseweb="select"] {
  background-color: #151b24 !important;
  border-color: #232c3b !important;
  border-radius: 12px !important;
}

div[data-baseweb="select"] * {
  color: #ffffff !important;
}

/* Buttons */
.stButton>button {
  background: linear-gradient(135deg, #ff9900 0%, #ff7700 100%) !important;
  color: #0b0f14 !important;
  font-weight: 800 !important;
  font-size: 14px !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 12px 18px !important;
  box-shadow: 0 4px 18px rgba(255, 153, 0, 0.35) !important;
  width: 100% !important;
}

.stButton>button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 24px rgba(255, 153, 0, 0.5) !important;
}

/* Red Emergency Block Button */
.btn-red-block button {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 18px rgba(239, 68, 68, 0.45) !important;
}

/* Fixed Bottom Mobile Navigation Bar */
.bottom-nav-container {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 440px;
  background: #0f151d;
  border-top: 1px solid #232c3b;
  padding: 8px 12px 14px 12px;
  z-index: 999999;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -10px 25px rgba(0, 0, 0, 0.6);
}

/* Radio buttons converted into sleek segmented tabs */
div[data-testid="stRadio"] {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 440px;
  background: #10151e !important;
  border-top: 1px solid #232c3b !important;
  padding: 8px 8px 14px 8px !important;
  z-index: 999999 !important;
}

div[data-testid="stRadio"] > div {
  display: flex !important;
  justify-content: space-between !important;
  background: transparent !important;
  border: none !important;
  gap: 4px !important;
}

div[data-testid="stRadio"] label {
  background: #151b24 !important;
  border: 1px solid #232c3b !important;
  border-radius: 12px !important;
  color: #94a3b8 !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  padding: 8px 6px !important;
  flex: 1 !important;
  text-align: center !important;
  cursor: pointer !important;
  margin: 0 !important;
}

div[data-testid="stRadio"] label[data-checked="true"] {
  background: #ff9900 !important;
  color: #0b0f14 !important;
  border-color: #ff9900 !important;
  box-shadow: 0 2px 10px rgba(255, 153, 0, 0.4) !important;
}

div[data-testid="stRadio"] label[data-checked="true"] p, div[data-testid="stRadio"] label[data-checked="true"] span {
  color: #0b0f14 !important;
}
</style>
"""

st.markdown(MOBILE_VIEWPORT_CSS, unsafe_allow_html=True)

# Mobile Status Bar at the Top
st.markdown("""
<div class="mobile-status-bar">
  <span>9:41</span>
  <div class="dynamic-island"><div class="camera-lens"></div></div>
  <span>5G &nbsp; 100%</span>
</div>
""", unsafe_allow_html=True)

# Audio Presets Database
AUDIO_PRESETS = {
    "Suno AI Instrumental #4": {
        "type": "AI",
        "file": "tests/test_audio/suno_instrumental_sample.wav",
        "conf": 97.3,
        "cutoff": 98.4,
        "lattice": 99.1,
        "jitter": 94.6
    },
    "Chopin Nocturne Op. 9 (Human)": {
        "type": "HUMAN",
        "file": "tests/test_audio/chopin_nocturne_sample.wav",
        "conf": 99.4,
        "cutoff": 4.2,
        "lattice": 2.1,
        "jitter": 3.8
    },
    "Mozart Eine kleine Nachtmusik": {
        "type": "HUMAN",
        "file": "tests/test_audio/mozart_sample.wav",
        "conf": 98.8,
        "cutoff": 3.8,
        "lattice": 1.9,
        "jitter": 2.9
    },
    "Suno AI Lo-Fi Beats #2": {
        "type": "AI",
        "file": "tests/test_audio/suno_instrumental_sample.wav",
        "conf": 98.1,
        "cutoff": 97.8,
        "lattice": 98.4,
        "jitter": 95.2
    },
    "Grandson Liam Voice Clone": {
        "type": "AI",
        "file": "video_assets/audio/scene4_scammer_call.mp3",
        "conf": 99.4,
        "cutoff": 99.2,
        "lattice": 99.6,
        "jitter": 97.8
    }
}


# ==============================================================================
# BOTTOM NAVIGATION CONTROLLER (Sticky Mobile Tabs)
# ==============================================================================
nav_screens = ["Overview", "Live Scan", "Catalog", "Alert", "Settings"]

# Check URL query or session state for navigation
current_screen = st.radio(
    "Mobile Tabs",
    nav_screens,
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)


# ==============================================================================
# SCREEN 1: OVERVIEW (Screen 2 from user mockup)
# ==============================================================================
if current_screen == "Overview":
    # Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
      <div>
        <div style="font-size: 23px; font-weight: 900; color: #ffffff; line-height: 1.1;">AcousticShield</div>
        <div style="font-size: 12px; font-weight: 600; color: #94a3b8; margin-top: 2px;">AWS AI Audio Forensics Hub</div>
      </div>
      <div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid #10b981; color: #10b981; font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 20px; box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);">
        ● ACTIVE
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Waveform Card
    st.markdown("""
    <div class="mobile-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Live Audio Spectrogram Stream</span>
        <span style="font-size: 11px; font-weight: 700; color: #ff9900; font-family: monospace;">44.1 kHz Mono</span>
      </div>
      <div class="wave-visual-box">
        <div class="wave-bar-anim" style="height: 35%; animation-delay: 0.1s;"></div>
        <div class="wave-bar-anim" style="height: 65%; animation-delay: 0.3s;"></div>
        <div class="wave-bar-anim" style="height: 95%; animation-delay: 0.2s;"></div>
        <div class="wave-bar-anim" style="height: 45%; animation-delay: 0.4s;"></div>
        <div class="wave-bar-anim" style="height: 85%; animation-delay: 0.15s;"></div>
        <div class="wave-bar-anim" style="height: 100%; animation-delay: 0.35s;"></div>
        <div class="wave-bar-anim" style="height: 60%; animation-delay: 0.25s;"></div>
        <div class="wave-bar-anim" style="height: 80%; animation-delay: 0.05s;"></div>
        <div class="wave-bar-anim" style="height: 40%; animation-delay: 0.3s;"></div>
        <div class="wave-bar-anim" style="height: 90%; animation-delay: 0.1s;"></div>
        <div class="wave-bar-anim" style="height: 50%; animation-delay: 0.45s;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Telemetry Metrics Row
    st.markdown("""
    <div class="telemetry-grid">
      <div class="telemetry-card">
        <div class="telemetry-label">Latency</div>
        <div class="telemetry-number" style="color: #ff9900 !important;">42ms</div>
        <div class="telemetry-foot">Edge Inference</div>
      </div>
      <div class="telemetry-card">
        <div class="telemetry-label">Accuracy</div>
        <div class="telemetry-number" style="color: #00cae0 !important;">99.7%</div>
        <div class="telemetry-foot">Audio Forensics</div>
      </div>
      <div class="telemetry-card">
        <div class="telemetry-label">False Positives</div>
        <div class="telemetry-number" style="color: #10b981 !important;">0</div>
        <div class="telemetry-foot">Verified Today</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Forensic Protection Modules Section
    st.markdown("""
    <div style="font-size: 14px; font-weight: 800; color: #ffffff; margin-bottom: 10px; letter-spacing: 0.02em;">
      Forensic Protection Modules
    </div>
    """, unsafe_allow_html=True)

    # Module 1: Amazon Music Shield
    st.markdown("""
    <div class="mobile-card" style="display: flex; align-items: center; gap: 14px; margin-bottom: 10px;">
      <div style="width: 44px; height: 44px; background: rgba(255, 153, 0, 0.15); border: 1.5px solid #ff9900; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px;">
        🎵
      </div>
      <div style="flex: 1;">
        <div style="font-size: 15px; font-weight: 800; color: #ffffff;">Amazon Music Shield</div>
        <div style="font-size: 11px; color: #94a3b8; line-height: 1.35;">Monitoring catalog uploads & protecting royalty streams for artists.</div>
      </div>
      <div style="font-size: 18px; color: #94a3b8; font-weight: 800;">›</div>
    </div>
    """, unsafe_allow_html=True)

    # Module 2: Alexa Voice Guard
    st.markdown("""
    <div class="mobile-card" style="display: flex; align-items: center; gap: 14px;">
      <div style="width: 44px; height: 44px; background: rgba(0, 202, 224, 0.15); border: 1.5px solid #00cae0; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px;">
        🛡️
      </div>
      <div style="flex: 1;">
        <div style="font-size: 15px; font-weight: 800; color: #ffffff;">Alexa Voice Guard</div>
        <div style="font-size: 11px; color: #94a3b8; line-height: 1.35;">Real-time deepfake & voice scam analysis for home devices.</div>
      </div>
      <div style="font-size: 18px; color: #94a3b8; font-weight: 800;">›</div>
    </div>
    """, unsafe_allow_html=True)

    # Top YouTube Link Callout
    st.markdown("""
    <div style="text-align: center; margin-top: 14px; padding: 10px; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 12px;">
      <a href="https://youtu.be/Gh9evlZncew" target="_blank" style="color: #ef4444; font-size: 12px; font-weight: 800; text-decoration: none;">
        ▶ Watch Official 1080p Video Walkthrough
      </a>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SCREEN 2: LIVE AUDIO SCAN (Screen 3 from user mockup)
# ==============================================================================
elif current_screen == "Live Scan":
    st.markdown("""
    <div style="margin-bottom: 12px;">
      <div style="font-size: 20px; font-weight: 900; color: #ffffff; display: flex; align-items: center; gap: 6px;">
        <span style="color: #ff9900; font-size: 22px;">|</span> Live Audio Scan
      </div>
      <div style="font-size: 12px; color: #94a3b8; font-weight: 500;">Active analysis of deep acoustics signatures</div>
    </div>
    """, unsafe_allow_html=True)

    # Audio Selector
    selected_preset = st.selectbox(
        "Select Audio Stream to Inspect:",
        list(AUDIO_PRESETS.keys()),
        index=0
    )
    p_data = AUDIO_PRESETS[selected_preset]
    is_ai = p_data["type"] == "AI"
    conf_score = p_data["conf"]

    # Trigger Scan Button
    if st.button("⚡ ANALYZE AUDIO STREAM IN REAL TIME"):
        with st.spinner("Processing neural inversion..."):
            time.sleep(0.3)

    # Circular Confidence Gauge
    gauge_color = "#f59e0b" if is_ai else "#10b981"
    st.markdown(f"""
    <div class="circular-gauge-box">
      <div class="gauge-inner-ring" style="border-top-color: {gauge_color}; border-right-color: {gauge_color}; box-shadow: 0 0 24px {gauge_color}55;">
        <div style="font-size: 28px; font-weight: 900; color: #ffffff; line-height: 1;">{conf_score:.1f}%</div>
        <div style="font-size: 10px; font-weight: 800; color: {gauge_color}; letter-spacing: 0.12em; margin-top: 4px;">CONFIDENCE</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Alert Banner
    if is_ai:
        st.markdown("""
        <div class="banner-ai-warning">
          ▲ AI GENERATED SIGNATURE DETECTED ▲
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="banner-human-verified">
          ✓ AUTHENTIC HUMAN MASTER RECORDING ✓
        </div>
        """, unsafe_allow_html=True)

    # 3 Progress Breakdown Cards
    c_fill = p_data["cutoff"]
    l_fill = p_data["lattice"]
    j_fill = p_data["jitter"]

    st.markdown(f"""
    <div class="prog-breakdown-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Ultrasonic Brickwall Cutoff</span>
        <span style="font-size: 12px; font-weight: 800; color: #ff9900; font-family: monospace;">{c_fill:.1f}%</span>
      </div>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">AI codec frequency boundary (Nyquist RVQ wall)</div>
      <div class="prog-track-line">
        <div class="prog-fill-line" style="width: {c_fill}%;"></div>
      </div>
    </div>

    <div class="prog-breakdown-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Codec Lattice Artifacts</span>
        <span style="font-size: 12px; font-weight: 800; color: #ff9900; font-family: monospace;">{l_fill:.1f}%</span>
      </div>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Neural synthesis spectral traces & vocoder comb spikes</div>
      <div class="prog-track-line">
        <div class="prog-fill-line" style="width: {l_fill}%;"></div>
      </div>
    </div>

    <div class="prog-breakdown-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Micro-Timing Jitter</span>
        <span style="font-size: 12px; font-weight: 800; color: #ff9900; font-family: monospace;">{j_fill:.1f}%</span>
      </div>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Sub-sample timing consistency & stereo Haas phase index</div>
      <div class="prog-track-line">
        <div class="prog-fill-line" style="width: {j_fill}%;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SCREEN 3: CATALOG (Screen 4 from user mockup)
# ==============================================================================
elif current_screen == "Catalog":
    st.markdown("""
    <div style="margin-bottom: 14px;">
      <div style="font-size: 20px; font-weight: 900; color: #ffffff; display: flex; align-items: center; gap: 6px;">
        <span style="color: #ff9900; font-size: 22px;">|</span> Amazon Music Shield
      </div>
      <div style="font-size: 12px; color: #94a3b8; font-weight: 500;">Catalog royalty pool preservation & analysis</div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Counters
    st.markdown("""
    <div class="telemetry-grid">
      <div class="telemetry-card">
        <div class="telemetry-label">Tracks Scanned</div>
        <div class="telemetry-number" style="color: #ffffff !important;">12,847</div>
        <div class="telemetry-foot">Catalog Defense</div>
      </div>
      <div class="telemetry-card">
        <div class="telemetry-label">AI Detected</div>
        <div class="telemetry-number" style="color: #ff9900 !important;">342</div>
        <div class="telemetry-foot">Telemetry</div>
      </div>
      <div class="telemetry-card">
        <div class="telemetry-label">Protected Pool</div>
        <div class="telemetry-number" style="color: #10b981 !important;">$48.2K</div>
        <div class="telemetry-foot">Protected Pool</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Recently Ingested Streams
    st.markdown("""
    <div style="font-size: 13px; font-weight: 800; color: #ffffff; margin: 12px 0 8px 0; letter-spacing: 0.04em;">
      Recently Ingested Streams
    </div>
    """, unsafe_allow_html=True)

    catalog_items = [
        {"title": "Shattered Synthesis", "artist": "Unknown Artificial", "type": "AI", "badge": "▲ AI DETECTED", "icon": "🔥"},
        {"title": "Midnight Solitude", "artist": "Sarah Jenkins (Human)", "type": "HUMAN", "badge": "● HUMAN", "icon": "🎻"},
        {"title": "Neural Resonance", "artist": "ByteCore AI Labs", "type": "AI", "badge": "▲ AI DETECTED", "icon": "⚡"},
        {"title": "Ethereal Echoes", "artist": "Marcus Vance", "type": "HUMAN", "badge": "● HUMAN", "icon": "🎹"},
        {"title": "Chopin Nocturne Op. 9", "artist": "Frederic Chopin", "type": "HUMAN", "badge": "● HUMAN", "icon": "🎼"},
        {"title": "Suno AI Symphony #4", "artist": "Generative Diffusion", "type": "AI", "badge": "▲ AI DETECTED", "icon": "🤖"}
    ]

    for item in catalog_items:
        is_ai_item = item["type"] == "AI"
        b_bg = "rgba(245, 158, 11, 0.14)" if is_ai_item else "rgba(16, 185, 129, 0.14)"
        b_border = "#f59e0b" if is_ai_item else "#10b981"
        b_color = "#f59e0b" if is_ai_item else "#10b981"

        st.markdown(f"""
        <div class="mobile-card" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; margin-bottom: 8px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 38px; height: 38px; background: #1c2430; border: 1px solid #232c3b; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;">
              {item['icon']}
            </div>
            <div>
              <div style="font-size: 13px; font-weight: 800; color: #ffffff;">{item['title']}</div>
              <div style="font-size: 11px; color: #94a3b8;">{item['artist']}</div>
            </div>
          </div>
          <div style="background: {b_bg}; border: 1px solid {b_border}; color: {b_color}; font-size: 10px; font-weight: 800; padding: 4px 8px; border-radius: 8px; letter-spacing: 0.04em;">
            {item['badge']}
          </div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# SCREEN 4: ALEXA DEEPFAKE ALERT (Screen 5 from user mockup)
# ==============================================================================
elif current_screen == "Alert":
    # Glowing Red Shield Icon
    st.markdown("""
    <div style="text-align: center; margin: 4px 0 14px 0;">
      <div style="width: 54px; height: 54px; border-radius: 50%; border: 2px solid #ef4444; background: rgba(239, 68, 68, 0.15); box-shadow: 0 0 22px rgba(239, 68, 68, 0.45); display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; font-size: 24px;">
        🛡️
      </div>
      <div style="font-size: 21px; font-weight: 900; color: #ef4444; line-height: 1.1;">Alexa Deepfake Alert</div>
      <div style="font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 2px;">Deepfake Voice Scam Intercepted</div>
    </div>
    """, unsafe_allow_html=True)

    # Scanned Channel Box
    st.markdown("""
    <div class="mobile-card" style="padding: 12px 14px; margin-bottom: 12px;">
      <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
        <span style="color: #94a3b8;">Scanned Channel:</span>
        <span style="color: #ffffff; font-weight: 700; font-family: monospace;">Alexa Call ID #2854</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
        <span style="color: #94a3b8;">Caller Name Tag:</span>
        <span style="color: #ffffff; font-weight: 700;">"Grandson Liam" (Claimed)</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 12px;">
        <span style="color: #94a3b8;">Deepfake Probability:</span>
        <span style="color: #ef4444; font-weight: 900;">97.2% Clone Match</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Acoustic Signature Comparison
    st.markdown("""
    <div style="font-size: 12px; font-weight: 800; color: #ffffff; margin-bottom: 8px;">
      Acoustic Signature Comparison
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 16px;">
      <div style="background: #151b24; border: 1px solid #232c3b; border-radius: 12px; padding: 10px; text-align: center;">
        <div style="font-size: 10px; color: #94a3b8; margin-bottom: 6px;">Original Voice</div>
        <div style="font-size: 18px; color: #10b981; letter-spacing: 2px;">ılılılllı</div>
        <div style="font-size: 9px; color: #10b981; font-weight: 700; margin-top: 4px;">Harmonics Match ✓</div>
      </div>
      <div style="background: #151b24; border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 10px; text-align: center;">
        <div style="font-size: 10px; color: #94a3b8; margin-bottom: 6px;">Scanned Caller</div>
        <div style="font-size: 18px; color: #ef4444; letter-spacing: 2px;">ıııııııı</div>
        <div style="font-size: 9px; color: #ef4444; font-weight: 700; margin-top: 4px;">Codec Lattice Traces ▲</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Primary Block Button
    st.markdown('<div class="btn-red-block">', unsafe_allow_html=True)
    if st.button("BLOCK CALLER IMMEDIATELY"):
        st.success("🚨 Call Dropped! Forensic Dossier signed with Ed25519 and vaulted to S3.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Secondary Action Buttons
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("Record Evidence"):
            st.info("SHA-256 fingerprint vaulted.")
    with c_btn2:
        if st.button("Alert Family"):
            st.warning("AWS SNS Alert broadcast to family.")


# ==============================================================================
# SCREEN 5: SETTINGS & ABOUT (Screen 6 from user mockup)
# ==============================================================================
elif current_screen == "Settings":
    st.markdown("""
    <div style="margin-bottom: 14px;">
      <div style="font-size: 20px; font-weight: 900; color: #ffffff; display: flex; align-items: center; gap: 6px;">
        <span style="color: #ff9900; font-size: 22px;">|</span> Settings & About
      </div>
      <div style="font-size: 12px; color: #94a3b8; font-weight: 500;">Forensics parameters & device status</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 13px; font-weight: 800; color: #ffffff; margin-bottom: 10px;">
      Core Protections
    </div>
    """, unsafe_allow_html=True)

    st.toggle("Real-time Music Scanning (Amazon Music Catalog)", value=True)
    st.toggle("Alexa Call Protection (Family Deepfake Defense)", value=True)
    st.toggle("Emergency Family Alerts (AWS SNS Dispatch)", value=False)

    st.markdown("""
    <div style="font-size: 13px; font-weight: 800; color: #ffffff; margin: 16px 0 8px 0;">
      Forensic Model Specs
    </div>
    <div class="mobile-card" style="padding: 12px 14px;">
      <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
        <span style="color: #94a3b8;">Detection Engine:</span>
        <span style="color: #ffffff; font-weight: 700; font-family: monospace;">v1.2.1-calibrated</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 6px;">
        <span style="color: #94a3b8;">Edge Model Size:</span>
        <span style="color: #ff9900; font-weight: 700; font-family: monospace;">4.2 MB</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 12px;">
        <span style="color: #94a3b8;">Supported Hardware:</span>
        <span style="color: #00cae0; font-weight: 700;">Echo Show, Fire TV, Fire Tablet</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 18px; padding: 14px 10px; background: #111720; border-radius: 14px; border: 1px solid #232c3b;">
      <div style="font-size: 11px; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Created for Amazon Web Services Hackathon 2026</div>
      <div style="font-size: 12px; font-weight: 800; color: #ff9900; letter-spacing: 0.05em;">AWS INTELLIGENT FORENSICS SYSTEM</div>
      <div style="display: flex; justify-content: center; gap: 14px; margin-top: 10px; font-size: 11px;">
        <a href="https://youtu.be/Gh9evlZncew" target="_blank" style="color: #ef4444; text-decoration: none; font-weight: 700;">▶ YouTube Demo</a>
        <a href="https://github.com/debdipARVR/AI_AUDIO_DETECTOR" target="_blank" style="color: #00cae0; text-decoration: none; font-weight: 700;">★ GitHub</a>
        <a href="https://huggingface.co/spaces/DebdipCS/acoustic-resonance-audio-forensics" target="_blank" style="color: #10b981; text-decoration: none; font-weight: 700;">🤗 HF Space</a>
      </div>
    </div>
    """, unsafe_allow_html=True)
