# Amazon Developer Hackathon 2026: Feature Requests

**Project**: AcousticShield (AI Voice & Instrumental Music Sentry for Alexa+)  
**Track**: Alexa+ ($25K) • AWS Builder Mini Challenge • Open Source Mini Challenge  
**Submitter**: Debdip Bandyopadhyay ([@debdipARVR](https://github.com/debdipARVR))  
**Repository**: [https://github.com/debdipARVR/AI_AUDIO_DETECTOR](https://github.com/debdipARVR/AI_AUDIO_DETECTOR)  

---

### Feature Request 1: Duplex Audio Streaming directly over Model Context Protocol (MCP)
- **Description**: Enable native bidirectional chunked PCM/Opus audio streaming over MCP SSE/Streamable HTTP transports without requiring base64 string serialization.
- **Priority**: **Critical**
- **Why it matters**: Drastically reduces latency and CPU serialization overhead for real-time Alexa+ audio sentry tools and smart home devices.

### Feature Request 2: Amazon Bedrock Native Audio Modality for Claude 3.5 Sonnet
- **Description**: Direct audio token ingestion within Bedrock Converse APIs to enable listening, acoustic feature analysis, and audio reasoning natively.
- **Priority**: **Important**
- **Why it matters**: Eliminates the need for separate edge transcription or heavy DSP pre-processing before invoking the Bedrock reasoning agent.

### Feature Request 3: Amazon S3 Object Lock Batch Retention API for Micro-Dossiers
- **Description**: A lightweight API to seal high-frequency forensic attestation JSON records into an immutable legal vault with sub-10ms commit latency.
- **Priority**: **Nice-to-have**
- **Why it matters**: Streamlines millions of real-time song scans into a unified legal compliance audit trail.
