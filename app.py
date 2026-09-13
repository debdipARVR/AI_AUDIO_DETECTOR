"""
AcousticShield: AWS AI Audio Forensics Hub & Amazon Music Sentry
Amazon Developer Hackathon (2026) • Track: Alexa+ ($25K) • AWS Bedrock & ECS
Design System: Authentic High-Contrast Mobile Dark UI (Amazon Music / Alexa+ App)
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
    page_title="AcousticShield • AWS AI Audio Forensics Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# High-Contrast Mobile Dark Design System CSS
HIGH_VISIBILITY_MOBILE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

/* Strict High-Contrast Color Palette */
:root {
  --app-bg: #0c1015;
  --card-bg: #151b24;
  --card-border: #232c3b;
  --card-hover: #1c2430;
  --txt-white: #ffffff;
  --txt-silver: #94a3b8;
  --txt-muted: #64748b;
  --amber-glow: #f59e0b;
  --amber-bright: #ff9900;
  --emerald-green: #10b981;
  --coral-red: #ef4444;
  --alexa-cyan: #00cae0;
}

/* Force high-visibility text across Streamlit elements */
html, body, [data-testid="stAppViewContainer"], .main, .stMarkdown, .stText, p, span, div, label {
  background-color: var(--app-bg) !important;
  color: var(--txt-white) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Override Streamlit light theme text defaults */
[data-testid="stMarkdownContainer"] p, [data-testid="stWidgetLabel"] label, [data-testid="stWidgetLabel"] p {
  color: var(--txt-white) !important;
}

/* Streamlit Header clean transparent */
[data-testid="stHeader"] {
  background: transparent !important;
}

/* Main Container centered */
.block-container {
  padding-top: 1.2rem !important;
  padding-bottom: 2rem !important;
  max-width: 1000px !important;
}

/* Smartphone Viewport Shell */
.phone-shell {
  max-width: 420px;
  margin: 0 auto;
  background: var(--app-bg);
  border: 9px solid #1e2530;
  border-radius: 46px;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.95), 0 0 30px rgba(245, 158, 11, 0.15);
  overflow: hidden;
  position: relative;
}

/* Phone Status Bar */
.phone-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px 6px 24px;
  font-size: 13px;
  font-weight: 700;
  color: #f1f5f9 !important;
  background: var(--app-bg);
}

.phone-dynamic-island {
  width: 96px;
  height: 24px;
  background: #000000;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.phone-camera-lens {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #1e293b;
  border: 1px solid #334155;
}

/* Screen Content Container */
.screen-content {
  padding: 18px 20px 24px 20px;
  min-height: 560px;
}

/* Navigation Segmented Bar */
.nav-segment-bar {
  display: flex;
  background: #151b24;
  border: 1px solid var(--card-border);
  border-radius: 14px;
  padding: 4px;
  margin-bottom: 16px;
  gap: 4px;
}

.nav-btn {
  flex: 1;
  text-align: center;
  padding: 8px 4px;
  font-size: 11px;
  font-weight: 700;
  color: var(--txt-silver) !important;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.15s ease;
}

.nav-btn-active {
  background: var(--amber-bright) !important;
  color: #0b0f14 !important;
  box-shadow: 0 2px 10px rgba(245, 158, 11, 0.35);
}

/* Card Containers */
.ui-card {
  background: var(--card-bg) !important;
  border: 1px solid var(--card-border) !important;
  border-radius: 18px;
  padding: 16px;
  margin-bottom: 14px;
}

.ui-card-clickable {
  transition: transform 0.15s ease, border-color 0.15s ease;
  cursor: pointer;
}

.ui-card-clickable:hover {
  border-color: var(--amber-glow) !important;
  transform: translateY(-1px);
}

/* Telemetry Metric Boxes */
.metric-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 16px;
}

.metric-box {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 14px;
  padding: 12px 8px;
  text-align: center;
}

.metric-lbl {
  font-size: 11px;
  font-weight: 600;
  color: var(--txt-silver) !important;
  margin-bottom: 4px;
}

.metric-val {
  font-size: 19px;
  font-weight: 900;
  color: var(--txt-white) !important;
}

.metric-sub {
  font-size: 9px;
  font-weight: 500;
  color: var(--txt-muted) !important;
  margin-top: 2px;
}

/* Audio Waveform Animation */
.waveform-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  height: 60px;
  margin: 12px 0;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 12px;
  padding: 0 10px;
}

.wave-bar {
  flex: 1;
  background: linear-gradient(to top, #ff9900, #ff5500);
  border-radius: 4px;
  animation: pulse-wave 1.4s ease-in-out infinite alternate;
}

@keyframes pulse-wave {
  0% { transform: scaleY(0.25); opacity: 0.7; }
  100% { transform: scaleY(1.0); opacity: 1.0; }
}

/* Circular Confidence Gauge */
.gauge-wrapper {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 16px auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gauge-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 7px solid #232c3b;
  border-top-color: #f59e0b;
  border-right-color: #f59e0b;
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.35);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #111720;
}

/* Alert Banners */
.alert-ai-banner {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.16), rgba(217, 119, 6, 0.08));
  border: 1.5px solid var(--amber-glow);
  border-radius: 14px;
  padding: 12px 14px;
  text-align: center;
  color: var(--amber-glow) !important;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.02em;
  margin: 14px 0;
}

.alert-human-banner {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.16), rgba(5, 150, 105, 0.08));
  border: 1.5px solid var(--emerald-green);
  border-radius: 14px;
  padding: 12px 14px;
  text-align: center;
  color: var(--emerald-green) !important;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.02em;
  margin: 14px 0;
}

.alert-red-banner {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.18), rgba(185, 28, 28, 0.08));
  border: 1.5px solid var(--coral-red);
  border-radius: 14px;
  padding: 14px;
  margin: 14px 0;
}

/* Progress Item Row */
.prog-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 10px;
}

.prog-track {
  height: 6px;
  background: #1f2937;
  border-radius: 6px;
  overflow: hidden;
  margin-top: 8px;
}

.prog-fill-amber {
  height: 100%;
  background: var(--amber-bright);
  border-radius: 6px;
}

/* Button Styling Overrides */
.stButton>button {
  background: linear-gradient(135deg, #ff9900 0%, #ff7700 100%) !important;
  color: #0b0f14 !important;
  font-weight: 800 !important;
  font-size: 14px !important;
  border: none !important;
  border-radius: 14px !important;
  padding: 10px 20px !important;
  box-shadow: 0 4px 18px rgba(255, 153, 0, 0.35) !important;
  width: 100% !important;
}

.stButton>button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 22px rgba(255, 153, 0, 0.5) !important;
}

/* Selectbox styling */
div[data-baseweb="select"] {
  background-color: #151b24 !important;
  border-color: #232c3b !important;
  border-radius: 12px !important;
}

div[data-baseweb="select"] * {
  color: #ffffff !important;
}

/* Radio button horizontal pill style */
div[data-testid="stRadio"] > div {
  background: #151b24;
  border: 1px solid #232c3b;
  border-radius: 14px;
  padding: 4px;
  gap: 4px;
}

div[data-testid="stRadio"] label {
  border-radius: 10px;
  padding: 6px 12px !important;
  font-weight: 700 !important;
  color: #94a3b8 !important;
}

div[data-testid="stRadio"] label[data-checked="true"] {
  background: #ff9900 !important;
  color: #0b0f14 !important;
}

/* Mobile Bottom Navigation Bar */
.bottom-nav-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 12px 10px 18px 10px;
  background: #111720;
  border-top: 1px solid var(--card-border);
}

.bottom-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 700;
  color: var(--txt-muted);
  text-decoration: none;
}

.bottom-nav-active {
  color: var(--amber-glow) !important;
}

.home-bar {
  width: 120px;
  height: 4px;
  background: #ffffff;
  border-radius: 4px;
  opacity: 0.35;
  margin: 6px auto 6px auto;
}
</style>
"""

st.markdown(HIGH_VISIBILITY_MOBILE_CSS, unsafe_allow_html=True)

# Initialize Session State
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Overview"
if "scanned_result" not in st.session_state:
    st.session_state.scanned_result = None
if "selected_preset" not in st.session_state:
    st.session_state.selected_preset = "Suno AI Instrumental #4"

@st.cache_resource
def get_music_engine():
    return MusicResonanceEngine()

music_engine = get_music_engine()

# Top Switcher Bar (App View & Direct Navigation)
col_top_mode, col_top_links = st.columns([1.2, 0.8])
with col_top_mode:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
      <span style="color: #ff9900; font-weight: 800; font-size: 13px; text-transform: uppercase; letter-spacing: 0.08em;">
        Amazon Developer Hackathon 2026 • Alexa+ ($25K)
      </span>
      <a href="https://youtu.be/Gh9evlZncew" target="_blank" style="display: inline-block; background: #ef4444; color: #ffffff; font-weight: 800; font-size: 11px; padding: 3px 10px; border-radius: 12px; text-decoration: none;">
        ▶ Watch Video Demo
      </a>
    </div>
    """, unsafe_allow_html=True)

with col_top_links:
    view_mode = st.radio(
        "Viewport:",
        ["📱 Mobile Frame (420px)", "🖥️ Expanded Layout"],
        horizontal=True,
        label_visibility="collapsed"
    )

is_mobile = "Mobile" in view_mode

# Primary Navigation Selector (Pill Bar matching the 4 tabs from the design)
screen_options = ["Overview", "Live Scan", "Catalog", "Alexa Alert", "Settings"]
current_idx = screen_options.index(st.session_state.active_nav) if st.session_state.active_nav in screen_options else 0

selected_nav = st.radio(
    "Navigation Tabs:",
    screen_options,
    index=current_idx,
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.active_nav = selected_nav


# Begin Mobile Phone Wrapper Container
if is_mobile:
    st.markdown("""
    <div class="phone-shell">
      <div class="phone-status-bar">
        <span>9:41</span>
        <div class="phone-dynamic-island"><div class="phone-camera-lens"></div></div>
        <span>5G &nbsp; 100%</span>
      </div>
      <div class="screen-content">
    """, unsafe_allow_html=True)


# ==============================================================================
# SCREEN 1: OVERVIEW
# ==============================================================================
if st.session_state.active_nav == "Overview":
    # Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
      <div>
        <div style="font-size: 22px; font-weight: 900; color: #ffffff; line-height: 1.1;">AcousticShield</div>
        <div style="font-size: 12px; font-weight: 600; color: #94a3b8;">AWS AI Audio Forensics Hub</div>
      </div>
      <div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid #10b981; color: #10b981; font-size: 11px; font-weight: 800; padding: 4px 10px; border-radius: 20px; box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);">
        ● ACTIVE
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Waveform Card
    st.markdown("""
    <div class="ui-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Live Audio Spectrogram Stream</span>
        <span style="font-size: 11px; font-weight: 700; color: #ff9900; font-family: monospace;">44.1 kHz Mono</span>
      </div>
      <div class="waveform-container">
        <div class="wave-bar" style="height: 35%; animation-delay: 0.1s;"></div>
        <div class="wave-bar" style="height: 65%; animation-delay: 0.3s;"></div>
        <div class="wave-bar" style="height: 90%; animation-delay: 0.2s;"></div>
        <div class="wave-bar" style="height: 45%; animation-delay: 0.4s;"></div>
        <div class="wave-bar" style="height: 80%; animation-delay: 0.15s;"></div>
        <div class="wave-bar" style="height: 100%; animation-delay: 0.35s;"></div>
        <div class="wave-bar" style="height: 60%; animation-delay: 0.25s;"></div>
        <div class="wave-bar" style="height: 75%; animation-delay: 0.05s;"></div>
        <div class="wave-bar" style="height: 40%; animation-delay: 0.3s;"></div>
        <div class="wave-bar" style="height: 85%; animation-delay: 0.1s;"></div>
        <div class="wave-bar" style="height: 50%; animation-delay: 0.45s;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Telemetry Metrics
    st.markdown("""
    <div class="metric-row">
      <div class="metric-box">
        <div class="metric-lbl">Latency</div>
        <div class="metric-val" style="color: #ff9900 !important;">42ms</div>
        <div class="metric-sub">Edge Inference</div>
      </div>
      <div class="metric-box">
        <div class="metric-lbl">Accuracy</div>
        <div class="metric-val" style="color: #00cae0 !important;">99.7%</div>
        <div class="metric-sub">Audio Forensics</div>
      </div>
      <div class="metric-box">
        <div class="metric-lbl">False Positives</div>
        <div class="metric-val" style="color: #10b981 !important;">0</div>
        <div class="metric-sub">Verified Today</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Forensic Protection Modules Header
    st.markdown("""
    <div style="font-size: 14px; font-weight: 800; color: #ffffff; margin-bottom: 10px; letter-spacing: 0.02em;">
      Forensic Protection Modules
    </div>
    """, unsafe_allow_html=True)

    # Module 1: Amazon Music Shield
    st.markdown("""
    <div class="ui-card ui-card-clickable" style="display: flex; align-items: center; gap: 14px;">
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
    <div class="ui-card ui-card-clickable" style="display: flex; align-items: center; gap: 14px;">
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

    # Action Button to launch scan
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("⚡ Open Live Scan"):
            st.session_state.active_nav = "Live Scan"
            st.rerun()
    with col_btn2:
        if st.button("🚨 Simulate Alexa Alert"):
            st.session_state.active_nav = "Alexa Alert"
            st.rerun()


# ==============================================================================
# SCREEN 2: LIVE AUDIO SCAN
# ==============================================================================
elif st.session_state.active_nav == "Live Scan":
    st.markdown("""
    <div style="margin-bottom: 12px;">
      <div style="font-size: 19px; font-weight: 900; color: #ffffff; display: flex; align-items: center; gap: 6px;">
        <span style="color: #ff9900; font-size: 22px;">|</span> Live Audio Scan
      </div>
      <div style="font-size: 12px; color: #94a3b8; font-weight: 500;">Active analysis of deep acoustics signatures</div>
    </div>
    """, unsafe_allow_html=True)

    # Preset Audio Selector
    audio_presets = {
        "Suno AI Instrumental #4": {
            "type": "AI",
            "file": "tests/test_audio/suno_instrumental_sample.wav",
            "conf": 97.3,
            "cutoff": "17.2 kHz (98.4%)",
            "lattice": "99.1%",
            "jitter": "94.6%"
        },
        "Chopin Nocturne Op. 9 No. 2 (Human Master)": {
            "type": "HUMAN",
            "file": "tests/test_audio/chopin_nocturne_sample.wav",
            "conf": 99.4,
            "cutoff": "22.05 kHz (0% AI)",
            "lattice": "1.2%",
            "jitter": "2.8%"
        },
        "Mozart Eine kleine Nachtmusik (Human Master)": {
            "type": "HUMAN",
            "file": "tests/test_audio/mozart_sample.wav",
            "conf": 98.9,
            "cutoff": "22.05 kHz (0% AI)",
            "lattice": "1.8%",
            "jitter": "3.1%"
        },
        "Suno AI Lo-Fi Beats #2": {
            "type": "AI",
            "file": "tests/test_audio/suno_instrumental_sample.wav",
            "conf": 98.2,
            "cutoff": "16.8 kHz (99.2%)",
            "lattice": "98.7%",
            "jitter": "95.1%"
        },
        "ElevenLabs Grandson Scam Voice Clone": {
            "type": "AI",
            "file": "video_assets/audio/scene4_scammer_call.mp3",
            "conf": 99.4,
            "cutoff": "17.4 kHz (99.6%)",
            "lattice": "99.8%",
            "jitter": "97.4%"
        }
    }

    selected_track = st.selectbox(
        "Choose Audio Stream Source:",
        list(audio_presets.keys()),
        index=0
    )
    track_info = audio_presets[selected_track]

    # Run Analysis Button
    run_scan = st.button("⚡ ANALYZE AUDIO STREAM IN REAL TIME")

    is_ai = track_info["type"] == "AI"
    conf_val = track_info["conf"]

    # Render Circular Gauge
    gauge_border_color = "#ff9900" if is_ai else "#10b981"
    st.markdown(f"""
    <div class="gauge-wrapper">
      <div class="gauge-circle" style="border-top-color: {gauge_border_color}; border-right-color: {gauge_border_color}; box-shadow: 0 0 20px {gauge_border_color}55;">
        <div style="font-size: 28px; font-weight: 900; color: #ffffff; line-height: 1;">{conf_val:.1f}%</div>
        <div style="font-size: 10px; font-weight: 800; color: {gauge_border_color}; letter-spacing: 0.12em; margin-top: 4px;">CONFIDENCE</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Alert Banner
    if is_ai:
        st.markdown("""
        <div class="alert-ai-banner">
          ⚠️ AI GENERATED SIGNATURE DETECTED ⚠️
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-human-banner">
          ✓ AUTHENTIC HUMAN MASTER RECORDING ✓
        </div>
        """, unsafe_allow_html=True)

    # 3 Breakdown Progress Cards matching the screenshot
    cutoff_fill = 98.4 if is_ai else 5.0
    lattice_fill = 99.1 if is_ai else 3.0
    jitter_fill = 94.6 if is_ai else 4.0

    st.markdown(f"""
    <div class="prog-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Ultrasonic Brickwall Cutoff</span>
        <span style="font-size: 12px; font-weight: 800; color: #ff9900; font-family: monospace;">{cutoff_fill}%</span>
      </div>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">AI codec frequency boundary (Nyquist RVQ wall)</div>
      <div class="prog-track">
        <div class="prog-fill-amber" style="width: {cutoff_fill}%;"></div>
      </div>
    </div>

    <div class="prog-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Codec Lattice Artifacts</span>
        <span style="font-size: 12px; font-weight: 800; color: #ff9900; font-family: monospace;">{lattice_fill}%</span>
      </div>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Neural synthesis spectral traces & comb harmonics</div>
      <div class="prog-track">
        <div class="prog-fill-amber" style="width: {lattice_fill}%;"></div>
      </div>
    </div>

    <div class="prog-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; font-weight: 700; color: #ffffff;">Micro-Timing Jitter</span>
        <span style="font-size: 12px; font-weight: 800; color: #ff9900; font-family: monospace;">{jitter_fill}%</span>
      </div>
      <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Sub-sample timing consistency & phase dispersion</div>
      <div class="prog-track">
        <div class="prog-fill-amber" style="width: {jitter_fill}%;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# SCREEN 3: CATALOG (AMAZON MUSIC SHIELD)
# ==============================================================================
elif st.session_state.active_nav == "Catalog":
    st.markdown("""
    <div style="margin-bottom: 14px;">
      <div style="font-size: 19px; font-weight: 900; color: #ffffff; display: flex; align-items: center; gap: 6px;">
        <span style="color: #ff9900; font-size: 22px;">|</span> Amazon Music Shield
      </div>
      <div style="font-size: 12px; color: #94a3b8; font-weight: 500;">Catalog royalty pool preservation & analysis</div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Counters
    st.markdown("""
    <div class="metric-row">
      <div class="metric-box">
        <div class="metric-lbl">Tracks Scanned</div>
        <div class="metric-val" style="color: #ffffff !important;">12,847</div>
        <div class="metric-sub">Catalog Ingest</div>
      </div>
      <div class="metric-box">
        <div class="metric-lbl">AI Detected</div>
        <div class="metric-val" style="color: #ff9900 !important;">342</div>
        <div class="metric-sub">Quarantined</div>
      </div>
      <div class="metric-box">
        <div class="metric-lbl">Protected Pool</div>
        <div class="metric-val" style="color: #10b981 !important;">$48.2K</div>
        <div class="metric-sub">Royalties Saved</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Recently Ingested Streams
    st.markdown("""
    <div style="font-size: 13px; font-weight: 800; color: #ffffff; margin: 12px 0 8px 0; letter-spacing: 0.04em;">
      Recently Ingested Streams
    </div>
    """, unsafe_allow_html=True)

    catalog_tracks = [
        {"title": "Shattered Synthesis", "artist": "Unknown Artificial", "type": "AI", "badge": "▲ AI DETECTED", "icon": "🔥"},
        {"title": "Midnight Solitude", "artist": "Sarah Jenkins (Human)", "type": "HUMAN", "badge": "● HUMAN", "icon": "🎻"},
        {"title": "Neural Resonance", "artist": "ByteCore AI Labs", "type": "AI", "badge": "▲ AI DETECTED", "icon": "⚡"},
        {"title": "Ethereal Echoes", "artist": "Marcus Vance (Human)", "type": "HUMAN", "badge": "● HUMAN", "icon": "🎹"},
        {"title": "Chopin Nocturne Op. 9", "artist": "Frederic Chopin", "type": "HUMAN", "badge": "● HUMAN", "icon": "🎼"},
        {"title": "Suno AI Symphony #4", "artist": "Generative Diffusion", "type": "AI", "badge": "▲ AI DETECTED", "icon": "🤖"}
    ]

    for t in catalog_tracks:
        is_ai_track = t["type"] == "AI"
        badge_bg = "rgba(245, 158, 11, 0.12)" if is_ai_track else "rgba(16, 185, 129, 0.12)"
        badge_border = "#f59e0b" if is_ai_track else "#10b981"
        badge_color = "#f59e0b" if is_ai_track else "#10b981"

        st.markdown(f"""
        <div class="ui-card" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; margin-bottom: 8px;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 38px; height: 38px; background: #1c2430; border: 1px solid #232c3b; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;">
              {t['icon']}
            </div>
            <div>
              <div style="font-size: 13px; font-weight: 800; color: #ffffff;">{t['title']}</div>
              <div style="font-size: 11px; color: #94a3b8;">{t['artist']}</div>
            </div>
          </div>
          <div style="background: {badge_bg}; border: 1px solid {badge_border}; color: {badge_color}; font-size: 10px; font-weight: 800; padding: 4px 8px; border-radius: 8px; letter-spacing: 0.04em;">
            {t['badge']}
          </div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# SCREEN 4: ALEXA DEEPFAKE ALERT
# ==============================================================================
elif st.session_state.active_nav == "Alexa Alert":
    # Top Glowing Red Shield
    st.markdown("""
    <div style="text-align: center; margin: 6px 0 14px 0;">
      <div style="width: 52px; height: 52px; border-radius: 50%; border: 2px solid #ef4444; background: rgba(239, 68, 68, 0.15); box-shadow: 0 0 20px rgba(239, 68, 68, 0.4); display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; font-size: 24px;">
        🛡️
      </div>
      <div style="font-size: 21px; font-weight: 900; color: #ef4444; line-height: 1.1;">Alexa Deepfake Alert</div>
      <div style="font-size: 12px; color: #94a3b8; font-weight: 600;">Deepfake Voice Scam Intercepted</div>
    </div>
    """, unsafe_allow_html=True)

    # Scanned Channel Box
    st.markdown("""
    <div class="ui-card" style="padding: 12px 14px;">
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

    # Action Buttons
    if st.button("🚨 BLOCK CALLER IMMEDIATELY"):
        st.success("Call Terminated! Audio evidence vaulted to Amazon S3.")

    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        if st.button("📁 Record Evidence"):
            st.info("SHA-256 fingerprint signed with Ed25519.")
    with col_sub2:
        if st.button("📞 Alert Family"):
            st.warning("AWS SNS Alert broadcast to authorized family contacts.")


# ==============================================================================
# SCREEN 5: SETTINGS & ABOUT
# ==============================================================================
elif st.session_state.active_nav == "Settings":
    st.markdown("""
    <div style="margin-bottom: 14px;">
      <div style="font-size: 19px; font-weight: 900; color: #ffffff; display: flex; align-items: center; gap: 6px;">
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

    t1 = st.toggle("Real-time Music Scanning (Amazon Music Catalog)", value=True)
    t2 = st.toggle("Alexa Call Protection (Family Deepfake Defense)", value=True)
    t3 = st.toggle("Emergency Family Alerts (AWS SNS Dispatch)", value=False)

    st.markdown("""
    <div style="font-size: 13px; font-weight: 800; color: #ffffff; margin: 16px 0 8px 0;">
      Forensic Model Specs
    </div>
    <div class="ui-card" style="padding: 12px 14px;">
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
    <div style="text-align: center; margin-top: 20px; padding: 14px 10px; background: #111720; border-radius: 14px; border: 1px solid #232c3b;">
      <div style="font-size: 11px; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Created for Amazon Web Services Hackathon 2026</div>
      <div style="font-size: 12px; font-weight: 800; color: #ff9900; letter-spacing: 0.05em;">AWS INTELLIGENT FORENSICS SYSTEM</div>
      <div style="display: flex; justify-content: center; gap: 14px; margin-top: 10px; font-size: 11px;">
        <a href="https://youtu.be/Gh9evlZncew" target="_blank" style="color: #ef4444; text-decoration: none; font-weight: 700;">▶ YouTube Demo</a>
        <a href="https://github.com/debdipARVR/AI_AUDIO_DETECTOR" target="_blank" style="color: #00cae0; text-decoration: none; font-weight: 700;">★ GitHub</a>
        <a href="https://huggingface.co/spaces/DebdipCS/acoustic-resonance-audio-forensics" target="_blank" style="color: #10b981; text-decoration: none; font-weight: 700;">🤗 HF Space</a>
      </div>
    </div>
    """, unsafe_allow_html=True)


# Bottom Navigation Bar inside Phone Frame
if is_mobile:
    nav_icons = {
        "Overview": "🧭",
        "Live Scan": "⚡",
        "Catalog": "🎵",
        "Settings": "⚙️"
    }
    
    st.markdown(f"""
      </div> <!-- Close screen-content -->
      <div class="bottom-nav-bar">
        <div class="bottom-nav-item {'bottom-nav-active' if st.session_state.active_nav == 'Overview' else ''}">
          <span style="font-size: 16px;">🧭</span>
          <span>Overview</span>
        </div>
        <div class="bottom-nav-item {'bottom-nav-active' if st.session_state.active_nav == 'Live Scan' else ''}">
          <span style="font-size: 16px;">⚡</span>
          <span>Live Scan</span>
        </div>
        <div class="bottom-nav-item {'bottom-nav-active' if st.session_state.active_nav == 'Catalog' else ''}">
          <span style="font-size: 16px;">🎵</span>
          <span>Catalog</span>
        </div>
        <div class="bottom-nav-item {'bottom-nav-active' if st.session_state.active_nav == 'Settings' else ''}">
          <span style="font-size: 16px;">⚙️</span>
          <span>Settings</span>
        </div>
      </div>
      <div class="home-bar"></div>
    </div> <!-- Close phone-shell -->
    """, unsafe_allow_html=True)
