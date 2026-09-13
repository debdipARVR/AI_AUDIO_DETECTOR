# Amazon Developer Hackathon 2026: Official Friction Log

**Project**: AcousticShield (AI Voice & Instrumental Music Sentry for Alexa+)  
**Track**: Alexa+ ($25K) • AWS Builder Mini Challenge • Open Source Mini Challenge  
**Submitter**: Debdip Bandyopadhyay ([@debdipARVR](https://github.com/debdipARVR))  
**Repository**: [https://github.com/debdipARVR/AI_AUDIO_DETECTOR](https://github.com/debdipARVR/AI_AUDIO_DETECTOR)  

---

## Executive Summary
This friction log documents real-world developer integration challenges, system behaviors, and actionable feedback gathered while building **AcousticShield** using **Amazon Bedrock**, **Model Context Protocol (FastMCP)**, **AWS ECS Fargate**, and **Amazon S3 Object Lock** for real-time audio safety on Alexa+ devices and Amazon Music.

---

## Log Entry 1: Amazon Bedrock Agent & Model Context Protocol (MCP) Schema Interoperability

- **Task Attempted**:  
  Connecting an AWS Bedrock Agent (powered by Anthropic Claude 3.5 Sonnet) directly with a streaming FastMCP server running over SSE (Server-Sent Events) to expose the `inspect_music_authenticity` tool for real-time Alexa+ audio verification.

- **Steps Taken**:
  1. Implemented `inspect_music_authenticity` tool conforming to official MCP Spec (2025-11-25) using FastMCP Python SDK.
  2. Attempted to register the MCP tool definitions inside AWS Bedrock Agent Action Groups via OpenAPI 3.0 YAML schema.
  3. Streamed simulated 24kHz/44.1kHz audio buffers from an Echo Show test harness to evaluate end-to-end response latency.

- **Expected Result**:  
  Seamless zero-code tool invocation where the Bedrock Agent automatically ingests the dynamic JSON-RPC 2.0 tool definitions exposed by the MCP endpoint, executing tools and receiving structured forensic payloads under 50ms.

- **Actual Result**:  
  Encountered a structural mismatch: AWS Bedrock Agent Action Groups strictly require static OpenAPI 3.0 / Swagger schema specifications, whereas the Model Context Protocol uses dynamic JSON-RPC 2.0 schema discovery (`tools/list` and `tools/call`). Additionally, Bedrock Action Group Lambda targets imposed payload serialization overhead when base64-encoding raw PCM audio blocks.

- **Severity Rating**:  
  **Medium (Integration Friction & Latency Overhead)**

- **Workaround Used**:  
  Engineered a lightweight translation adapter running in our AWS ECS Fargate container. The adapter translates incoming Bedrock Agent OpenAPI action requests into standardized MCP JSON-RPC 2.0 calls, passing audio buffers as pre-hashed PCM blocks with SHA-256 integrity verification.

- **Actionable Suggestion for AWS / Amazon Developer Team**:  
  Provide native Bedrock Agent support for the Model Context Protocol (MCP Spec 2025-11-25) as a first-class Action Group provider type. Enabling native MCP tool discovery would eliminate the need for intermediary API Gateway / OpenAPI adapter layers and drastically accelerate agentic tool development for Alexa+.

---

## Log Entry 2: High-Frequency Audio Streaming Payload Limits on API Gateway

- **Task Attempted**:  
  Streaming high-resolution stereo audio (44.1kHz 16-bit PCM) from the Amazon Music mobile client directly to the ECS Fargate container for live forensic analysis.

- **Steps Taken**:
  1. Configured Amazon API Gateway (REST/HTTP) as the entry ingress for audio chunk streaming.
  2. Transmitted 5-second audio buffers (~882 KB raw PCM) to the `/inspect` endpoint.

- **Expected Result**:  
  Smooth binary stream pass-through with sub-20ms ingress overhead.

- **Actual Result**:  
  API Gateway 10 MB payload limits and lack of native duplex binary streaming caused chunk fragmentation and serialization latency (~120ms total latency, exceeding Alexa's strict real-time audio SLA).

- **Severity Rating**:  
  **High (Performance & SLA Impact)**

- **Workaround Used**:  
  Implemented direct WebSocket and Streamable HTTP chunking on ECS Fargate using FastAPI with asynchronous streaming iterators, bypassing the API Gateway REST buffer.

- **Actionable Suggestion for AWS**:  
  Introduce an **AWS Bedrock Streaming Audio Gateway** optimized for real-time edge voice/music buffers that natively supports chunked Opus and raw PCM transfers without requiring base64 encoding.

---

## Log Entry 3: S3 Object Lock High-Frequency Micro-Dossier Retention Latency

- **Task Attempted**:  
  Vaulting tamper-proof Ed25519 forensic dossiers and SHA-256 audio fingerprints into an Amazon S3 Object Lock bucket with Compliance Mode retention during active streaming playback.

- **Steps Taken**:
  1. Enabled S3 Object Lock with legal retention on target audit bucket.
  2. Issued `put_object` calls with `ObjectLockMode='COMPLIANCE'` and `RetainUntilDate` on every detected synthetic track.

- **Expected Result**:  
  Immediate asynchronous write confirmation with minimal client-side execution wait.

- **Actual Result**:  
  Direct synchronous PUT requests with Object Lock metadata introduced a 60–85ms round-trip overhead per detected event when executed in the primary request thread.

- **Severity Rating**:  
  **Low (Architectural Polish)**

- **Workaround Used**:  
  Decoupled the vaulting pipeline using an in-memory asynchronous worker queue (`asyncio.Queue` / Amazon SQS) that batches and vaults forensic attestation dossiers in the background without blocking real-time listener playback.

- **Actionable Suggestion for AWS**:  
  Provide an asynchronous batch-attestation API for Amazon S3 Object Lock specifically designed for high-frequency security and copyright compliance logging.
