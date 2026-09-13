"""
AcousticShield: Interactive Alexa+ Scam Intercept Simulation
Runs the exact live scenario featured in the hackathon video demo.
"""

import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.dirname(CURRENT_DIR)
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

try:
    from acousticshield.engine import AcousticResonanceEngine
except ImportError:
    from engine import AcousticResonanceEngine


def run_simulation():
    engine = AcousticResonanceEngine()
    
    print("=" * 75)
    print("    ACOUSTICSHIELD 2.0 • ALEXA+ AGENTIC INTERCEPT CONSOLE")
    print("=" * 75)
    print("Simulating Incoming VoIP Call on Amazon Echo Show 10...")
    time.sleep(0.5)
    
    print("\n[INCOMING CALL] Caller ID: Grandson Tommy (+1-555-0192)")
    print("[AUDIO STREAMING INTO ALEXA+ MICROPHONE ARRAY]")
    print("\n>>> CALLER AUDIO (ElevenLabs Voice Clone):")
    print('    "Grandma! I got into a terrible car accident in Chicago.')
    print('     The police are holding me until I pay $4,500 bail.')
    print('     Please wire the money right now, don\'t tell mom!"')
    
    time.sleep(0.6)
    print("\n>>> GRANDMOTHER: 'Alexa, Tommy sounds frightened... is this really him calling me?'")
    
    time.sleep(0.5)
    print("\n[*] Alexa+ invokes MCP Tool: inspect_audio_authenticity(stream_buffer)...")
    print("    --> Forwarding audio tensors to Amazon Bedrock Agent...")
    print("    --> AWS SageMaker ECS: Performing EnCodec 24kHz RVQ Multi-Codec Inversion...")
    
    time.sleep(0.5)
    report = engine.analyze_audio(preset_type="grandparent_scam", channel="voip_opus")
    
    print(f"    --> Resonance Inversion STFT-SNR: {report.stft_snr_db} dB (Delta: +{report.resonance_delta_db} dB SURGE)")
    print(f"    --> 1D Vocoder Comb Spikes: {report.comb_peak_frequencies_hz} (HiFi-GAN periodic artifacts)")
    print(f"    --> Diaphragm Johnson Thermal Noise: ABSENT ({report.noise_floor_dbfs} dBFS silence floor)")
    print(f"    --> Cryptographic Attestation: {report.ed25519_signature[:28]}... (SEALED)")
    print(f"    --> Inversion Latency: {report.latency_ms:.1f} ms (< 500 ms Alexa SLA)")
    
    time.sleep(0.5)
    print("\n" + "!" * 75)
    print("    [ALEXA+ SPOKEN WARNING & EMERGENCY RED HUD ACTIVATED]")
    print("!" * 75)
    print(f'ALEXA+: "Warning! This call is NOT your grandson. I have detected an AI synthetic')
    print(f'         voice clone with {report.confidence*100:.1f}% confidence, attributed to ElevenLabs.')
    print(f'         The physical microphone noise is absent, and the vocal cords show mathematical')
    print(f'         neural codec resonance. I am blocking this call immediately and alerting')
    print(f'         your daughter Sarah on her mobile app."')
    
    print("\n>>> ECHO SHOW SCREEN ACTIONS:")
    print("    [1] Intercept & Block Caller (Default - Auto Executed)")
    print("    [2] Require Secret Family Cryptographic Passphrase")
    print("    [3] Download Ed25519 Police Forensic Dossier PDF")
    print("=" * 75)
    print("STATUS: Scam Prevented. Zero Financial Loss. Audio Vaulted in Amazon S3.")
    print("=" * 75)


if __name__ == "__main__":
    run_simulation()
