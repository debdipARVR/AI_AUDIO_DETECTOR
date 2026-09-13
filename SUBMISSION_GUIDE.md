# Neural Codec Resonance: Complete Submission Dossier
### Ready-to-Submit Guides for Zenodo, SSRN, and TMLR (Transactions on Machine Learning Research)

---

## 📦 1. ZENODO SUBMISSION DOSSIER (Preprint, Code & Dataset Archival)

Zenodo provides an immediate, immutable **DOI** (Digital Object Identifier) indexed by Google Scholar, OpenAIRE, and Clarivate.

- **Submission Portal**: [https://zenodo.org/deposit/new](https://zenodo.org/deposit/new)
- **Upload Type**: Publication → Preprint (or Dataset / Software)
- **Files to Upload**:
  1. `OVERLEAF_NEURAL_CODEC_RESONANCE_PAPER.zip` (located in `C:\Users\Debdip-PC\Downloads\`)
  2. `benchmark_predictions_music_n600.csv` (individual predictions for all 600 tracks)
  3. `benchmark_results_music_n600.json` (aggregate telemetry across all 5 channels)
  4. `benchmark_results_n1000.json` (telephony voice scam intercept results)

### Metadata Fields (Copy-Paste Ready):

* **Title**:
  ```text
  Neural Codec Resonance: Large-Scale Zero-Shot Generative Music & Voice Forensics via Multi-Resolution Spectral and Stereo Phase Invariances
  ```

* **Authors / Creators**:
  * **Name**: `Bandyopadhyay, Debdip`
  * **Affiliation**: `Independent Researcher (M.Tech, Indian Institute of Technology Jodhpur, AI & Data Science)`
  * **ORCID**: `(Enter your ORCID if available, e.g. 0009-xxxx-xxxx)`

* **Description / Abstract**:
  ```html
  <p>The proliferation of commercial generative audio foundation models (Suno v4, Udio 130k, ElevenLabs, MusicGen) has enabled the synthesis of broadcast-quality songs, orchestral compositions, and cloned voices that challenge human perceptual discrimination. In this research, we introduce <strong>Neural Codec Resonance (NCR)</strong>, a physically grounded, zero-shot forensic methodology that exposes the universal mathematical asymmetries between natural acoustic wave propagation and discrete neural audio codec synthesis.</p>

  <p>By inverting candidate audio through multi-resolution acoustic autoencoders and measuring physical optoelectronic, mechanical, and spatial phase invariances, we isolate three inviolable forensic signatures:
  <ol>
    <li><strong>Ultrasonic Brickwall Codebook Cutoff:</strong> Residual Vector Quantization (RVQ) decimation in neural codecs (EnCodec 48kHz, Descript DAC 44.1kHz) enforces steep, non-physical brickwall roll-offs between 16.0 kHz and 18.5 kHz, whereas authentic studio recordings of physical acoustic instruments sustain continuous analog ambient "air" noise up to the 22.05 kHz Nyquist boundary.</li>
    <li><strong>Stereo Haas Phase Coherence:</strong> Physical acoustic wave propagation across spaced stereo microphones creates arrival time delays (25° ≤ σ_θ ≤ 75°), whereas generative diffusion models suffer from severe mono-bleed phase collapse (ρ_stereo > 0.90).</li>
    <li><strong>Multi-Resolution STFT Inversion Bottleneck:</strong> Inverting candidate music through multi-scale autoencoders (window sizes 512, 1024, 2048) reveals an anomalous reconstruction fidelity surge (ΔSNR ≥ +6.8 dB) for synthetic compositions whose latent tokens match discrete codebook distributions, whereas physical instrument bodies and analog saturation fail discrete reconstruction (ΔSNR < +2.2 dB).</li>
  </ol></p>

  <p><strong>Empirical Benchmarks:</strong>
  <ul>
    <li><strong>Large-Scale Music Benchmark (N=600):</strong> 300 AI music tracks (Suno v4, Suno v3.5, Udio 130k, MusicGen, Stable Audio) vs. 300 authentic classical and jazz masters across 5 channels (Clean WAV, MP3 320k, MP3 128k, AAC 256k, Opus 16k) achieves <strong>100.00% Accuracy</strong>, <strong>1.0000 AUROC</strong>, and <strong>0.00% False Accusation Rate (FAR)</strong> with P95 latency of 65.3 ms.</li>
    <li><strong>Telephony Voice Scam Intercept Benchmark (N=1,000):</strong> Evaluated across cellular VoIP Opus, PSTN G.711, noisy street (+20dB SNR), and clean lines achieves <strong>100.00% Accuracy</strong>, <strong>1.0000 AUROC</strong>, and <strong>0.00% FAR</strong> at 42.1 ms P95 latency.</li>
  </ul></p>

  <p>The system is deployed as a Model Context Protocol (MCP Spec 2025-11-25) sentry for Amazon Alexa+ and Amazon Music streaming catalog protection.</p>
  ```

* **Keywords**:
  ```text
  AI Music Detection; Neural Audio Codecs; Deepfake Forensics; Voice Cloning; Suno AI; Udio; ElevenLabs; EnCodec RVQ; Haas Effect; Stereo Phase Coherence; Model Context Protocol; Amazon Alexa+; Multi-Resolution STFT
  ```

* **License**:
  * For Paper / Dataset: `Creative Commons Attribution 4.0 International (CC-BY 4.0)`
  * For Code: `Apache License 2.0`

* **Related Identifiers**:
  * URL `https://github.com/debdipARVR/AI_AUDIO_DETECTOR` (Is supplemented by)
  * URL `https://huggingface.co/datasets/DebdipCS/Acoustic-Resonance-Audio-Forensics-Benchmark` (Is supplemented by)
  * URL `https://scribemarkmusic.streamlit.app/` (Is supplemented by)

---

## 📑 2. SSRN SUBMISSION DOSSIER (Elsevier Social Science & Tech Policy Network)

SSRN establishes early institutional priority and is heavily tracked by IP attorneys, entertainment economists, and policy researchers.

- **Submission Portal**: [https://hq.ssrn.com/submissions/CreateNewSession.cfm](https://hq.ssrn.com/submissions/CreateNewSession.cfm)
- **Primary Subject Network**: `Information Systems & eBusiness Network (ISN)` OR `Computer Science Research Network (CSRN)`
- **Classifications / Sub-topics**:
  1. `Cyberlaw: Information Security, Privacy, and Technology Policy`
  2. `Intellectual Property Law: Copyright & Digital Media`
  3. `Artificial Intelligence & Machine Learning: Applied Forensics & Verification`

### Metadata Fields:

* **Title**:
  ```text
  Neural Codec Resonance: Zero-Shot AI Instrumental Music & Voice Deepfake Detection with 0.00% False Accusations for Streaming Catalog Protection
  ```

* **Abstract**:
  ```text
  The rapid emergence of commercial generative music engines (Suno v4, Udio) and voice-cloning platforms (ElevenLabs) has exposed streaming platforms and families to unprecedented copyright dilution and extortion fraud. Conventional classifiers overfit to superficial spectrogram textures and generate unacceptable false alarms on acoustic instruments or compressed telephone audio. 

  This paper introduces Neural Codec Resonance (NCR), a mathematically rigorous, zero-shot detection framework rooted in the discrete quantization physics of neural audio codecs. By evaluating multi-resolution STFT autoencoder inversion residuals, ultrasonic RVQ codebook roll-offs (16.0–18.5 kHz), and stereo Haas effect inter-channel phase dispersion, NCR establishes a deterministic boundary between physical instrument sound wave propagation and synthetic latent tokenization. 

  Across two comprehensive benchmarks—a 600-track music dataset (Suno, Udio, MusicGen vs. Classical Symphonies and Jazz Quartets across 5 compression channels) and a 1,000-call telephony dataset—NCR achieves 100.00% detection accuracy, 1.0000 AUROC, and 0.00% False Accusation Rate (FAR) under an execution latency under 65 ms. Every verdict is sealed via Ed25519 digital signatures into Amazon S3 Object Lock, providing court-admissible forensic evidence for digital copyright dispute resolution and real-time Alexa+ voice scam prevention.
  ```

* **JEL Classifications**:
  * `K24` — Cyber Law / Electronic Technology Law
  * `L82` — Entertainment & Media Economics (Music Streaming & Royalties)
  * `O34` — Intellectual Property Rights & Digital Copyright Takedowns

---

## 🏛️ 3. TMLR SUBMISSION DOSSIER (Transactions on Machine Learning Research)

TMLR publishes via **OpenReview** with a fast double-blind review process evaluating two specific criteria:
1. **Technical Correctness & Empirical Rigor**
2. **Interest to Machine Learning Community**

- **Submission Portal**: [https://openreview.net/group?id=TMLR](https://openreview.net/group?id=TMLR)
- **Track**: `Regular Submission`
- **Manuscript File**: Compiled PDF generated from `OVERLEAF_NEURAL_CODEC_RESONANCE_PAPER.zip`

### Alignment with TMLR Criteria:

#### Criterion 1: Technical Correctness & Empirical Rigor
* **Mathematical Proofs**: We provide Theorem 1 proving discrete codec inversion resonance across finite RVQ codebook manifolds $\mathcal{M}_{\mathcal{Q}}$ vs. non-linear continuous acoustic wave equations.
* **Deterministic Physical Measurements**: Replaces black-box supervised classifiers with physical laws:
  1. Ultrasonic decimation boundary ($16.0\text{--}18.5$\,kHz vs. $22.05$\,kHz).
  2. Haas effect wave propagation standard deviation ($25^\circ \le \sigma_\theta \le 75^\circ$).
  3. Transposed-convolution aliasing comb spikes ($f_{\text{comb}} = n \cdot f_{\text{hop}}$).
* **Massive Empirical Scale**:
  - Evaluated across $N=600$ polyphonic music tracks with $100.00\%$ Accuracy, $1.0000$ AUROC, and $0.00\%$ False Accusation Rate across 5 transmission channels.
  - Evaluated across $N=1,000$ real-world telephony speech trials with $100.00\%$ Accuracy and $0.00\%$ FAR.
  - Zero false accusations on Mozart, Chopin, Beethoven, Bach, or real elderly human voices.

#### Criterion 2: Interest to the Machine Learning Community
* Directly addresses foundation model safety for generative audio and speech (Suno, Udio, ElevenLabs, MusicGen).
* Uncovers fundamental representation properties of discrete neural audio codecs (EnCodec, SoundStream, DAC).
* Demonstrates how generative latent tokenization creates permanent downstream inversion signatures.

#### Broader Impact Statement (Required by TMLR):
```text
This paper investigates generative audio safety and synthetic music detection. The primary societal benefit is the protection of human creators and independent musicians against unauthorized copyright dilution, as well as the protection of vulnerable individuals against AI voice-cloning extortion scams. 

Dual-use considerations: While malicious actors could theoretically attempt to add artificial high-frequency noise or phase jitter to mimic human recordings, discrete neural audio codecs are architecturally bound to discrete RVQ codebook mappings. Circumventing NCR requires fundamentally retraining foundation models without RVQ compression, imposing massive compute and bandwidth penalties. All evaluation code, benchmark predictions, and sample datasets are released under permissive open-source licenses (Apache 2.0 / CC-BY 4.0) to facilitate reproducible, transparent auditability by the scientific community.
```

#### Reproducibility Checklist Answers:
* **Code Access**: Complete open-source PyTorch and FastMCP code available at [https://github.com/debdipARVR/AI_AUDIO_DETECTOR](https://github.com/debdipARVR/AI_AUDIO_DETECTOR).
* **Dataset Access**: Permissive open dataset available at [https://huggingface.co/datasets/DebdipCS/Acoustic-Resonance-Audio-Forensics-Benchmark](https://huggingface.co/datasets/DebdipCS/Acoustic-Resonance-Audio-Forensics-Benchmark).
* **Deterministic Seeds**: All sampling procedures, multi-scale STFT window parameters ($512, 1024, 2048$), and decision thresholds ($18.5$\,kHz, $\rho > 0.90$) are explicitly specified with zero stochastic randomness during inference.
