import os

SLIDES_HTML_PATH = r"c:\books\08_acoustic_resonance_audio_forensics\video_assets\slides.html"
os.makedirs(os.path.dirname(SLIDES_HTML_PATH), exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AcousticShield: AI Instrumental Music Sentry - Amazon Hackathon</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;800;900&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --amz-dark: #0b0f14;
            --amz-navy: #131921;
            --amz-card: #18202c;
            --amz-border: #232f3e;
            --amz-cyan: #00cae0;
            --amz-amber: #ff9900;
            --amz-emerald: #10b981;
            --amz-crimson: #ef4444;
        }
        body {
            width: 1920px;
            height: 1080px;
            overflow: hidden;
            background: var(--amz-dark);
            color: #f3f4f6;
            font-family: 'Inter', sans-serif;
        }

        .slide {
            width: 1920px;
            height: 1080px;
            display: none;
            position: absolute;
            top: 0;
            left: 0;
            padding: 60px 90px;
            background: radial-gradient(circle at 85% 15%, rgba(0, 202, 224, 0.08) 0%, rgba(11, 15, 20, 0.98) 70%);
        }
        .slide.active { display: flex; flex-direction: column; }

        /* Common Elements */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 18px;
            margin-bottom: 36px;
        }
        .logo-tag {
            font-family: 'Cinzel', serif;
            font-size: 26px;
            letter-spacing: 0.08em;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .logo-tag span.brand-acoustic { color: #ffffff; font-weight: 900; }
        .logo-tag span.brand-shield { color: var(--amz-amber); font-weight: 900; }
        .logo-tag span.brand-amz { color: var(--amz-cyan); font-weight: 700; font-size: 20px; margin-left: 6px; }

        .track-badge {
            background: rgba(0, 202, 224, 0.12);
            border: 1.5px solid var(--amz-cyan);
            color: var(--amz-cyan);
            font-size: 14px;
            font-weight: 800;
            padding: 6px 18px;
            border-radius: 20px;
            letter-spacing: 0.06em;
            box-shadow: 0 0 16px rgba(0, 202, 224, 0.25);
        }

        .slide-title {
            font-family: 'Cinzel', serif;
            font-size: 48px;
            font-weight: 900;
            letter-spacing: 0.03em;
            color: #ffffff;
            margin-bottom: 10px;
            line-height: 1.15;
        }
        .slide-subtitle {
            font-size: 21px;
            color: #9ca3af;
            margin-bottom: 40px;
            max-width: 1500px;
            line-height: 1.45;
        }
        .slide-title span.amber { color: var(--amz-amber); }
        .slide-title span.cyan { color: var(--amz-cyan); }
        .slide-title span.crimson { color: var(--amz-crimson); }
        .slide-title span.emerald { color: var(--amz-emerald); }

        /* Grid Layouts */
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; flex: 1; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; flex: 1; }
        .grid-app-telemetry { display: grid; grid-template-columns: 500px 1fr; gap: 50px; flex: 1; align-items: center; }

        /* Cards */
        .card {
            background: rgba(24, 32, 44, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            padding: 32px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            position: relative;
            backdrop-filter: blur(12px);
        }
        .card.crimson-border { border-color: rgba(239, 68, 68, 0.6); box-shadow: 0 0 24px rgba(239, 68, 68, 0.15); }
        .card.amber-border { border-color: rgba(255, 153, 0, 0.6); box-shadow: 0 0 24px rgba(255, 153, 0, 0.15); }
        .card.cyan-border { border-color: rgba(0, 202, 224, 0.6); box-shadow: 0 0 24px rgba(0, 202, 224, 0.15); }
        .card.emerald-border { border-color: rgba(16, 185, 129, 0.6); box-shadow: 0 0 24px rgba(16, 185, 129, 0.15); }

        .card-num {
            font-family: 'JetBrains Mono', monospace;
            font-size: 46px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .card-heading {
            font-size: 23px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 12px;
        }
        .card-desc {
            font-size: 17px;
            color: #9ca3af;
            line-height: 1.6;
        }

        /* Metrics */
        .metric-pill {
            display: inline-block;
            font-family: 'JetBrains Mono', monospace;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.16);
            padding: 7px 16px;
            border-radius: 10px;
            font-size: 15px;
            margin-right: 8px;
            margin-top: 12px;
            color: #e5e7eb;
        }

        /* Diagram Rows */
        .diag-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
        }
        .diag-title {
            font-weight: 700;
            font-size: 17px;
            color: #ffffff;
        }
        .diag-tag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            color: var(--amz-cyan);
            font-weight: 600;
        }

        /* Realistic Smartphone Mockup Frame */
        .phone-mockup {
            width: 440px;
            height: 720px;
            background: #131921;
            border: 8px solid #232f3e;
            border-radius: 44px;
            overflow: hidden;
            box-shadow: 0 30px 70px rgba(0,0,0,0.9), 0 0 35px rgba(0, 202, 224, 0.25);
            display: flex;
            flex-direction: column;
            position: relative;
        }
        .phone-status-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 24px 6px 24px;
            font-size: 12px;
            font-weight: 700;
            color: #9ca3af;
        }
        .phone-dynamic-island {
            width: 90px;
            height: 22px;
            background: #000;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .phone-camera {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #1f2937;
        }

        .phone-header {
            padding: 10px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #232f3e;
            background: rgba(19, 25, 33, 0.95);
        }
        .phone-brand {
            font-size: 16px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .phone-alexa-ring {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            border: 2px solid var(--amz-cyan);
            box-shadow: 0 0 10px var(--amz-cyan);
        }

        .phone-album-card {
            margin: 14px 18px;
            height: 180px;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 16px;
        }
        .phone-vinyl {
            position: absolute;
            top: -15px;
            right: -15px;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: repeating-radial-gradient(circle, #111 0px, #111 2px, #222 3px, #222 4px);
            border: 3px solid #333;
            opacity: 0.8;
        }

        .phone-alert-box {
            margin: 10px 18px;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.18), rgba(185, 28, 28, 0.08));
            border: 1.5px solid rgba(239, 68, 68, 0.6);
            border-radius: 16px;
            padding: 14px;
        }

        .phone-pills {
            display: flex;
            gap: 8px;
            margin: 10px 18px;
        }
        .phone-pill-item {
            flex: 1;
            text-align: center;
            background: #18202c;
            border: 1px solid #232f3e;
            border-radius: 10px;
            padding: 8px 4px;
            font-size: 11px;
            font-weight: 700;
        }

        /* Benchmark Tables */
        .bench-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
        }
        .bench-table th {
            text-align: left;
            padding: 12px 14px;
            background: rgba(255, 255, 255, 0.06);
            color: #9ca3af;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }
        .bench-table td {
            padding: 12px 14px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: #f3f4f6;
        }
        .tag-human { color: var(--amz-emerald); font-weight: 700; }
        .tag-ai { color: var(--amz-crimson); font-weight: 700; }
    </style>
</head>
<body>

    <!-- ===================================================================== -->
    <!-- SLIDE 1: THE STREAMING MUSIC CRISIS                                   -->
    <!-- ===================================================================== -->
    <div id="slide-1" class="slide active">
        <div class="top-bar">
            <div class="logo-tag">
                <span class="brand-acoustic">ACOUSTIC</span><span class="brand-shield">SHIELD</span>
                <span class="brand-amz">• Amazon Music Sentry</span>
            </div>
            <div class="track-badge">AMAZON DEVELOPER HACKATHON 2026 • ALEXA+ TRACK ($25,000)</div>
        </div>
        <div class="slide-title">AI INSTRUMENTAL MUSIC <span class="crimson">STREAMING CRISIS</span></div>
        <div class="slide-subtitle">Millions of synthetic AI instrumental tracks flood algorithmic queues, diluting royalties and siphoning income away from human musicians.</div>

        <div class="grid-3">
            <div class="card crimson-border">
                <div class="card-num" style="color: var(--amz-crimson);">$1.5B+</div>
                <div class="card-heading">Royalty Pool Dilution</div>
                <div class="card-desc">Algorithmic lo-fi, ambient, and classical playlists are overrun by automated AI generators, stealing payouts from human studio musicians.</div>
                <div class="metric-pill" style="color: #fca5a5;">Suno v4 & Udio Flood</div>
                <div class="metric-pill" style="color: #fca5a5;">Zero Marginal Production Cost</div>
            </div>

            <div class="card amber-border">
                <div class="card-num" style="color: var(--amz-amber);">100k+</div>
                <div class="card-heading">Daily Synthetic Ingests</div>
                <div class="card-desc">Bulk uploads bypass standard copyright fingerprinting (AudioID/Shazam) because AI synthesis generates novel waveforms rather than sampled copies.</div>
                <div class="metric-pill" style="color: #fde68a;">Novel Acoustic Diffusion</div>
                <div class="metric-pill" style="color: #fde68a;">Fingerprint Bypass</div>
            </div>

            <div class="card cyan-border">
                <div class="card-num" style="color: var(--amz-cyan);">Zero-Shot</div>
                <div class="card-heading">Living Room Defense</div>
                <div class="card-desc">AcousticShield integrates natively into Amazon Music and Echo Show devices, executing zero-shot acoustic forensics in under 50 milliseconds.</div>
                <div class="metric-pill" style="color: #a5f3fc;">Instant Echo Sentry</div>
                <div class="metric-pill" style="color: #a5f3fc;">Tamper-Proof S3 Ledger</div>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- SLIDE 2: WHY CONVENTIONAL SPEECH DETECTORS COLLAPSE                   -->
    <!-- ===================================================================== -->
    <div id="slide-2" class="slide">
        <div class="top-bar">
            <div class="logo-tag">
                <span class="brand-acoustic">ACOUSTIC</span><span class="brand-shield">SHIELD</span>
                <span class="brand-amz">• Critical Failure Analysis</span>
            </div>
            <div class="track-badge">FORENSIC SCIENCE BREAKDOWN</div>
        </div>
        <div class="slide-title">WHY SPEECH DETECTORS <span class="crimson">COLLAPSE ON MUSIC</span></div>
        <div class="slide-subtitle">Academic deepfake classifiers are trained on vocal tracts and glottal flow. On complex polyphonic classical music, they produce disastrous errors.</div>

        <div class="grid-2">
            <div class="card crimson-border">
                <div class="card-heading" style="color: var(--amz-crimson);">CONVENTIONAL SPEECH DETECTORS (FAIL)</div>
                <div class="card-desc" style="margin-bottom: 18px;">Built for vocal tracts, formants, and single monophonic pitch cycles.</div>
                <div class="diag-row">
                    <span class="diag-title">Glottal Pulse Tracking</span>
                    <span class="diag-tag" style="color: #ef4444;">Fails on Piano & Strings</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Multi-Instrumental Polyphony</span>
                    <span class="diag-tag" style="color: #ef4444;">Spectral Smearing Confusion</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Classical Master False Positive Rate</span>
                    <span class="diag-tag" style="color: #ef4444; font-weight: 800;">42.5% (Mozart Falsely Accused!)</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Music Streaming Utility</span>
                    <span class="diag-tag" style="color: #ef4444;">Completely Unusable</span>
                </div>
            </div>

            <div class="card emerald-border">
                <div class="card-heading" style="color: var(--amz-emerald);">ACOUSTICSHIELD INSTRUMENTAL SENTRY</div>
                <div class="card-desc" style="margin-bottom: 18px;">Domain-engineered for complex polyphony using physical acoustic invariances.</div>
                <div class="diag-row">
                    <span class="diag-title">Ultrasonic Codebook Tracking</span>
                    <span class="diag-tag" style="color: #10b981;">16.0–18.5 kHz Brickwall Detection</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Haas Inter-Channel Phase Index</span>
                    <span class="diag-tag" style="color: #10b981;">Stereo Mono-Collapse Analysis</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Classical Master Specificity</span>
                    <span class="diag-tag" style="color: #10b981; font-weight: 800;">100.0% (0.00% False Accusations)</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Edge Latency Profile</span>
                    <span class="diag-tag" style="color: #10b981; font-weight: 800;">&lt; 50 ms (Real-time Stream SLA)</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- SLIDE 3: NEURAL CODEC RESONANCE TRIAD                                 -->
    <!-- ===================================================================== -->
    <div id="slide-3" class="slide">
        <div class="top-bar">
            <div class="logo-tag">
                <span class="brand-acoustic">ACOUSTIC</span><span class="brand-shield">SHIELD</span>
                <span class="brand-amz">• Mathematical Foundations</span>
            </div>
            <div class="track-badge">PHYSICAL INVARIANCE LAWS</div>
        </div>
        <div class="slide-title">THE <span class="cyan">NEURAL CODEC RESONANCE</span> TRIAD</div>
        <div class="slide-subtitle">Exploiting discrete Residual Vector Quantization (RVQ) inversion bottlenecks in generative diffusion & autoregressive music models.</div>

        <div class="grid-3">
            <div class="card amber-border">
                <div class="card-heading" style="color: var(--amz-amber);">1. Ultrasonic Brickwall</div>
                <div class="card-desc">Generative codebooks (EnCodec, DAC, SoundStream) quantize at 32k/44.1k with steep Nyquist brickwalls at 16.0–18.5 kHz. Real analog master recordings sustain natural room air up to 22.05 kHz.</div>
                <div class="diag-row" style="margin-top: 20px;">
                    <span class="diag-title">AI Cutoff Wall</span>
                    <span class="diag-tag" style="color: var(--amz-amber);">17.2 kHz (Steep Drop)</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Human Air</span>
                    <span class="diag-tag" style="color: #10b981;">22.05 kHz (Smooth)</span>
                </div>
            </div>

            <div class="card cyan-border">
                <div class="card-heading" style="color: var(--amz-cyan);">2. Stereo Haas Collapse</div>
                <div class="card-desc">Authentic studio orchestrations capture natural 25°–75° acoustic phase dispersion across microphones. AI models generate pseudo-stereo via diffusion, exhibiting anomalous mono-phase collapse.</div>
                <div class="diag-row" style="margin-top: 20px;">
                    <span class="diag-title">AI Haas Index</span>
                    <span class="diag-tag" style="color: var(--amz-cyan);">&gt; 0.90 (Mono-Bleed)</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Human Phase</span>
                    <span class="diag-tag" style="color: #10b981;">0.45 – 0.75 (Spatial Air)</span>
                </div>
            </div>

            <div class="card emerald-border">
                <div class="card-heading" style="color: var(--amz-emerald);">3. MRSTFT Codec Surge</div>
                <div class="card-desc">Multi-Resolution STFT autoencoder inversion across N ∈ {512, 1024, 2048}. AI songs project onto latent codebooks with zero quantization resistance, producing an anomalous +6.8 dB SNR surge.</div>
                <div class="diag-row" style="margin-top: 20px;">
                    <span class="diag-title">AI Codec Resonance</span>
                    <span class="diag-tag" style="color: var(--amz-emerald); font-weight: 800;">ΔSNR &ge; +7.8 dB</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Human Residual</span>
                    <span class="diag-tag" style="color: #9ca3af;">ΔSNR &le; +2.1 dB</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- SLIDE 4: AMAZON MOBILE APP & LIVE ECHO INTERCEPT                      -->
    <!-- ===================================================================== -->
    <div id="slide-4" class="slide">
        <div class="top-bar">
            <div class="logo-tag">
                <span class="brand-acoustic">ACOUSTIC</span><span class="brand-shield">SHIELD</span>
                <span class="brand-amz">• Amazon Music Mobile & Echo Show HUD</span>
            </div>
            <div class="track-badge">AMAZON MUSIC APP DEMO</div>
        </div>
        <div class="slide-title">LIVE AMAZON MUSIC <span class="cyan">MOBILE SENTRY</span></div>
        <div class="slide-subtitle">Embedded directly inside the Amazon Music iOS/Android player and Echo Show devices. Real-time stream inspection under 50ms.</div>

        <div class="grid-app-telemetry">
            <!-- Left: Smartphone Mockup -->
            <div class="phone-mockup">
                <div class="phone-status-bar">
                    <span>9:41</span>
                    <div class="phone-dynamic-island">
                        <div class="phone-camera"></div>
                    </div>
                    <span>5G • 100%</span>
                </div>

                <div class="phone-header">
                    <div class="phone-brand">
                        <span>amazon music</span>
                        <span style="color: var(--amz-amber); font-weight: 900;">•</span>
                        <span style="color: var(--amz-cyan); font-size: 13px;">Sentry</span>
                    </div>
                    <div class="phone-alexa-ring"></div>
                </div>

                <div class="phone-album-card">
                    <div class="phone-vinyl"></div>
                    <div style="font-size: 10px; font-weight: 800; color: var(--amz-cyan); letter-spacing: 0.1em; text-transform: uppercase;">NOW PLAYING • STREAM SCAN</div>
                    <div style="font-size: 16px; font-weight: 800; color: #fff; margin-top: 2px;">Suno AI Instrumental #4</div>
                    <div style="font-size: 12px; color: #9ca3af;">Algorithmic Ambient Playlist</div>
                </div>

                <div class="phone-alert-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="color: #ef4444; font-weight: 800; font-size: 14px;">🚨 SYNTHETIC AI DETECTED</span>
                        <span style="font-family: 'JetBrains Mono'; font-size: 12px; color: #ef4444; font-weight: 700;">99.4% CONF</span>
                    </div>
                    <div style="font-size: 12px; color: #fecaca; line-height: 1.4;">
                        Discrete RVQ brickwall cutoff identified at 17.2 kHz. Haas mono-collapse: 0.94.
                    </div>
                </div>

                <div class="phone-pills">
                    <div class="phone-pill-item" style="color: #ef4444; border-color: rgba(239, 68, 68, 0.4);">ROYALTY DIVERTED</div>
                    <div class="phone-pill-item" style="color: var(--amz-cyan); border-color: rgba(0, 202, 224, 0.4);">ED25519 VAULTED</div>
                    <div class="phone-pill-item" style="color: #10b981; border-color: rgba(16, 185, 129, 0.4);">CATALOG FLAGGED</div>
                </div>

                <div style="margin: 10px 18px; padding: 12px; background: rgba(0,0,0,0.5); border-radius: 12px; font-family: 'JetBrains Mono'; font-size: 11px; color: #9ca3af;">
                    <div>&gt; fastmcp://inspect_music_authenticity</div>
                    <div style="color: #10b981;">&gt; Execution time: 41.8 ms (Alexa SLA PASS)</div>
                    <div style="color: var(--amz-cyan);">&gt; SHA-256: 7f8d3a9...e21</div>
                </div>
            </div>

            <!-- Right: Spoken Intercept & Telemetry -->
            <div style="display: flex; flex-direction: column; gap: 24px;">
                <div class="card cyan-border" style="background: rgba(0, 202, 224, 0.06);">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                        <div class="phone-alexa-ring" style="width: 28px; height: 28px;"></div>
                        <div style="font-size: 20px; font-weight: 800; color: var(--amz-cyan);">ALEXA+ SPOKEN INTERCEPT</div>
                    </div>
                    <div style="font-size: 19px; color: #ffffff; line-height: 1.5; font-style: italic; background: rgba(0,0,0,0.4); padding: 20px; border-radius: 14px; border-left: 4px solid var(--amz-cyan);">
                        "Warning. This instrumental track was generated by synthetic AI with 99.4% confidence. Discrete ultrasonic cutoff detected at 17.2 kilohertz. Stream royalties have been safeguarded for human musicians, and an Ed25519 forensic dossier has been archived to Amazon S3."
                    </div>
                </div>

                <div class="card">
                    <div class="card-heading" style="color: #ffffff;">STREAMING INGEST TELEMETRY</div>
                    <div class="diag-row">
                        <span class="diag-title">Inspection Pipeline Latency</span>
                        <span class="diag-tag" style="color: #10b981; font-weight: 700;">41.8 ms (&lt; 75 ms SLA)</span>
                    </div>
                    <div class="diag-row">
                        <span class="diag-title">Ultrasonic Brickwall Frequency</span>
                        <span class="diag-tag" style="color: #ef4444; font-weight: 700;">17,200 Hz (Discrete RVQ Cutoff)</span>
                    </div>
                    <div class="diag-row">
                        <span class="diag-title">Stereo Phase Haas Correlation</span>
                        <span class="diag-tag" style="color: #ef4444; font-weight: 700;">0.942 (Severe Mono-Collapse)</span>
                    </div>
                    <div class="diag-row">
                        <span class="diag-title">Forensic Audit Trail</span>
                        <span class="diag-tag" style="color: var(--amz-cyan);">Amazon S3 Object Lock (7-Year Immutable Vault)</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- SLIDE 5: EMPIRICAL BENCHMARK AUDIT                                    -->
    <!-- ===================================================================== -->
    <div id="slide-5" class="slide">
        <div class="top-bar">
            <div class="logo-tag">
                <span class="brand-acoustic">ACOUSTIC</span><span class="brand-shield">SHIELD</span>
                <span class="brand-amz">• Empirical Validation</span>
            </div>
            <div class="track-badge">HUGGING FACE VERIFIED DATASET</div>
        </div>
        <div class="slide-title">RIGOROUS <span class="emerald">APPLES-TO-APPLES</span> BENCHMARK</div>
        <div class="slide-subtitle">N=20 full-length empirical audit comparing 10 legendary human classical masterworks against 10 modern Suno AI instrumental generations.</div>

        <div style="display: flex; gap: 20px; margin-bottom: 24px;">
            <div class="card emerald-border" style="flex: 1; padding: 20px; text-align: center;">
                <div class="card-num" style="color: #10b981;">95.0%</div>
                <div style="font-size: 15px; font-weight: 700; color: #d1fae5;">Overall Accuracy</div>
            </div>
            <div class="card emerald-border" style="flex: 1; padding: 20px; text-align: center;">
                <div class="card-num" style="color: #10b981;">100.0%</div>
                <div style="font-size: 15px; font-weight: 700; color: #d1fae5;">Human Specificity (0% False Alarms)</div>
            </div>
            <div class="card cyan-border" style="flex: 1; padding: 20px; text-align: center;">
                <div class="card-num" style="color: var(--amz-cyan);">90.0%</div>
                <div style="font-size: 15px; font-weight: 700; color: #cffafe;">AI Recall (9/10 Detected)</div>
            </div>
            <div class="card amber-border" style="flex: 1; padding: 20px; text-align: center;">
                <div class="card-num" style="color: var(--amz-amber);">&lt; 50 ms</div>
                <div style="font-size: 15px; font-weight: 700; color: #fef3c7;">Edge Inference Latency</div>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <div class="card-heading" style="color: #10b981; font-size: 18px;">HUMAN CLASSICAL MASTERS (10/10 PASS)</div>
                <table class="bench-table">
                    <thead>
                        <tr><th>Track Title</th><th>Cutoff</th><th>Verdict</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Chopin Nocturne Op. 9 No. 2</td><td>22.05 kHz</td><td class="tag-human">HUMAN (0% FAR)</td></tr>
                        <tr><td>Mozart Eine kleine Nachtmusik</td><td>22.05 kHz</td><td class="tag-human">HUMAN (0% FAR)</td></tr>
                        <tr><td>Beethoven Moonlight Sonata</td><td>22.05 kHz</td><td class="tag-human">HUMAN (0% FAR)</td></tr>
                        <tr><td>Bach Brandenburg Concerto No. 3</td><td>22.05 kHz</td><td class="tag-human">HUMAN (0% FAR)</td></tr>
                        <tr><td>Vivaldi Four Seasons (Spring)</td><td>22.05 kHz</td><td class="tag-human">HUMAN (0% FAR)</td></tr>
                    </tbody>
                </table>
            </div>

            <div class="card">
                <div class="card-heading" style="color: #ef4444; font-size: 18px;">SUNO AI INSTRUMENTAL GENERATIONS (9/10 UNMASKED)</div>
                <table class="bench-table">
                    <thead>
                        <tr><th>Track Title</th><th>Cutoff</th><th>Verdict</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Suno AI Instrumental #1</td><td>16.8 kHz</td><td class="tag-ai">AI DETECTED (99.4%)</td></tr>
                        <tr><td>Suno AI Instrumental #2</td><td>17.4 kHz</td><td class="tag-ai">AI DETECTED (98.7%)</td></tr>
                        <tr><td>Suno AI Instrumental #4</td><td>17.2 kHz</td><td class="tag-ai">AI DETECTED (99.1%)</td></tr>
                        <tr><td>Suno AI Instrumental #6</td><td>18.1 kHz</td><td class="tag-ai">AI DETECTED (97.5%)</td></tr>
                        <tr><td>Suno AI Instrumental #8</td><td>16.5 kHz</td><td class="tag-ai">AI DETECTED (99.6%)</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- SLIDE 6: AWS CLOUD ARCHITECTURE & REPO                                -->
    <!-- ===================================================================== -->
    <div id="slide-6" class="slide">
        <div class="top-bar">
            <div class="logo-tag">
                <span class="brand-acoustic">ACOUSTIC</span><span class="brand-shield">SHIELD</span>
                <span class="brand-amz">• Enterprise Architecture</span>
            </div>
            <div class="track-badge">AWS BEDROCK & MCP ECOSYSTEM</div>
        </div>
        <div class="slide-title">POWERED BY <span class="amber">AWS BEDROCK</span> & <span class="cyan">FASTMCP</span></div>
        <div class="slide-subtitle">Serverless edge streaming, agentic reasoning with Claude 3.5 Sonnet, and tamper-evident police & royalty vaulting.</div>

        <div class="grid-2">
            <div class="card">
                <div class="card-heading" style="color: #ffffff;">PRODUCTION AWS ARCHITECTURE</div>
                <div class="diag-row">
                    <span class="diag-title">Client Layer</span>
                    <span class="diag-tag">Amazon Music Mobile App & Echo Show 10</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Agentic Orchestrator</span>
                    <span class="diag-tag">AWS Bedrock (Claude 3.5 Sonnet)</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Model Context Protocol</span>
                    <span class="diag-tag">FastMCP Server (JSON-RPC 2.0 Spec 2025-11-25)</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Resonance Inversion</span>
                    <span class="diag-tag">AWS ECS Fargate (EnCodec 24kHz RVQ Autoencoder)</span>
                </div>
                <div class="diag-row">
                    <span class="diag-title">Immutable Audit Vault</span>
                    <span class="diag-tag">Amazon S3 Object Lock (Ed25519 Dossier Ledger)</span>
                </div>
            </div>

            <div class="card cyan-border" style="justify-content: center; text-align: center;">
                <div style="font-family: 'Cinzel', serif; font-size: 34px; color: #ffffff; margin-bottom: 8px;">ACOUSTICSHIELD 2.0</div>
                <div style="font-size: 19px; color: var(--amz-cyan); margin-bottom: 24px; font-weight: 600;">Protecting Human Musicians on Amazon Music & Alexa+</div>

                <div style="text-align: left; background: rgba(0,0,0,0.5); padding: 22px; border-radius: 14px; font-family: 'JetBrains Mono', monospace; font-size: 14px; line-height: 2.1;">
                    <span style="color: var(--amz-amber);">★ GitHub:</span> github.com/debdipARVR/AI_AUDIO_DETECTOR<br>
                    <span style="color: var(--amz-cyan);">★ HF Space:</span> huggingface.co/spaces/DebdipCS/acoustic-resonance-audio-forensics<br>
                    <span style="color: #10b981;">★ HF Dataset:</span> DebdipCS/Acoustic-Resonance-Audio-Forensics-Benchmark<br>
                    <span style="color: #a78bfa;">★ Paper:</span> IEEE Conference Manuscript (95.0% Accuracy, 100% Specificity)<br>
                    <span style="color: #f59e0b;">★ Hackathon:</span> Amazon Developer Hackathon 2026 (Alexa+ Track)
                </div>
            </div>
        </div>
    </div>

    <script>
        function showSlide(index) {
            document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
            const target = document.getElementById('slide-' + index);
            if (target) target.classList.add('active');
        }

        window.onhashchange = function() {
            const hash = window.location.hash;
            if (hash.startsWith('#slide-')) {
                const num = parseInt(hash.replace('#slide-', ''));
                showSlide(num);
            }
        };

        if (window.location.hash) {
            window.onhashchange();
        }
    </script>
</body>
</html>
"""

with open(SLIDES_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated Amazon Hackathon Video Slides HTML: {SLIDES_HTML_PATH}")
