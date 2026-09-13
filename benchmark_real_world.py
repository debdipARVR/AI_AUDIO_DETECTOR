"""
AcousticShield 2.0: Real-World In-The-Wild Audio Benchmark
Evaluates AcousticResonanceEngine on authentic ElevenLabs synthetic speech vs real human YouTube speech
from the public deepfake audio benchmark dataset (garystafford/deepfake-audio-detection).
"""

import os
import sys
import time
import json
import numpy as np
import soundfile as sf
from huggingface_hub import hf_hub_download, HfApi

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from acousticshield.engine import AcousticResonanceEngine
from benchmark_resonance import compute_roc_metrics


def run_real_world_benchmark(n_samples_per_class: int = 30, output_file: str = "benchmark_results_real_world_n60.json"):
    print("=" * 80)
    print(f"  ACOUSTICSHIELD 2.0 REAL-WORLD EMPIRICAL BENCHMARK (N={n_samples_per_class * 2})")
    print("  Evaluating on Real ElevenLabs AI Speech vs Real YouTube Human Speech")
    print("  Benchmark Source: garystafford/deepfake-audio-detection (Hugging Face Hub)")
    print("=" * 80)

    repo_id = "garystafford/deepfake-audio-detection"
    api = HfApi()

    print("\n[1/3] Querying repository file manifest...")
    all_files = api.list_repo_files(repo_id, repo_type="dataset")
    fake_candidates = [f for f in all_files if f.startswith("fake/") and f.endswith(".flac")][:n_samples_per_class]
    real_candidates = [f for f in all_files if f.startswith("real/") and f.endswith(".flac")][:n_samples_per_class]

    print(f"Selected {len(fake_candidates)} ElevenLabs AI files and {len(real_candidates)} YouTube human files.")

    engine = AcousticResonanceEngine()
    y_true = []
    y_scores = []
    latencies = []
    evaluations = []

    print("\n[2/3] Downloading and executing forensic resonance analysis...")

    # 1. Evaluate ElevenLabs AI speech (Label = 1)
    print(f"\n--- Evaluating {len(fake_candidates)} ElevenLabs AI Audio Files ---")
    for i, path in enumerate(fake_candidates):
        t0 = time.perf_counter()
        local_file = hf_hub_download(repo_id=repo_id, filename=path, repo_type="dataset")
        audio_data, sr = sf.read(local_file)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        rep = engine.analyze_audio(audio_array=audio_data, sample_rate=sr)
        lat = (time.perf_counter() - t0) * 1000.0

        score = rep.confidence if rep.verdict == "AI_CLONE" else (1.0 - rep.confidence)
        y_true.append(1)
        y_scores.append(score)
        latencies.append(lat)

        evaluations.append({
            "file": path,
            "ground_truth": "AI_SYNTHETIC",
            "verdict": rep.verdict,
            "confidence": round(rep.confidence, 4),
            "score": round(score, 4),
            "resonance_delta_db": round(rep.resonance_delta_db, 2),
            "comb_ratio": round(rep.comb_energy_ratio, 2),
            "noise_floor_dbfs": round(rep.noise_floor_dbfs, 2),
            "latency_ms": round(lat, 2)
        })

        if (i + 1) % 5 == 0 or i == 0:
            print(f"  [AI {i+1:02d}/{len(fake_candidates)}] {os.path.basename(path)} -> {rep.verdict} "
                  f"(conf={rep.confidence:.2f}, delta={rep.resonance_delta_db:+.1f}dB, floor={rep.noise_floor_dbfs:.1f}dBFS, lat={lat:.1f}ms)")

    # 2. Evaluate Real YouTube Human speech (Label = 0)
    print(f"\n--- Evaluating {len(real_candidates)} Real Human Audio Files ---")
    for j, path in enumerate(real_candidates):
        t0 = time.perf_counter()
        local_file = hf_hub_download(repo_id=repo_id, filename=path, repo_type="dataset")
        audio_data, sr = sf.read(local_file)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        rep = engine.analyze_audio(audio_array=audio_data, sample_rate=sr)
        lat = (time.perf_counter() - t0) * 1000.0

        score = rep.confidence if rep.verdict == "AI_CLONE" else (1.0 - rep.confidence)
        y_true.append(0)
        y_scores.append(score)
        latencies.append(lat)

        evaluations.append({
            "file": path,
            "ground_truth": "AUTHENTIC_HUMAN",
            "verdict": rep.verdict,
            "confidence": round(rep.confidence, 4),
            "score": round(score, 4),
            "resonance_delta_db": round(rep.resonance_delta_db, 2),
            "comb_ratio": round(rep.comb_energy_ratio, 2),
            "noise_floor_dbfs": round(rep.noise_floor_dbfs, 2),
            "latency_ms": round(lat, 2)
        })

        if (j + 1) % 5 == 0 or j == 0:
            print(f"  [Human {j+1:02d}/{len(real_candidates)}] {os.path.basename(path)} -> {rep.verdict} "
                  f"(conf={rep.confidence:.2f}, delta={rep.resonance_delta_db:+.1f}dB, floor={rep.noise_floor_dbfs:.1f}dBFS, lat={lat:.1f}ms)")

    print("\n[3/3] Computing real-world benchmark metrics...")
    metrics = compute_roc_metrics(y_true, y_scores, threshold=0.5)

    lat_arr = np.array(latencies)
    latency_summary = {
        "mean_ms": round(float(np.mean(lat_arr)), 2),
        "median_ms": round(float(np.median(lat_arr)), 2),
        "p95_ms": round(float(np.percentile(lat_arr, 95)), 2),
        "max_ms": round(float(np.max(lat_arr)), 2)
    }

    report = {
        "benchmark_dataset": "garystafford/deepfake-audio-detection",
        "cohort_size": len(y_true),
        "n_synthetic_elevenlabs": len(fake_candidates),
        "n_authentic_youtube": len(real_candidates),
        "metrics": metrics,
        "latency_summary": latency_summary,
        "detailed_evaluations": evaluations
    }

    out_path = os.path.join(CURRENT_DIR, output_file)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 80)
    print("  REAL-WORLD BENCHMARK RESULTS SUMMARY")
    print("=" * 80)
    print(f"  Cohort Size:           {len(y_true)} authentic audio files")
    print(f"  AUROC:                 {metrics['auroc']}")
    print(f"  Accuracy:              {metrics['accuracy'] * 100:.2f}%")
    print(f"  Precision:             {metrics['precision'] * 100:.2f}%")
    print(f"  Recall (Detection):    {metrics['recall'] * 100:.2f}%")
    print(f"  Specificity:           {metrics['specificity'] * 100:.2f}%")
    print(f"  False Accusation Rate: {metrics['false_accusation_rate'] * 100:.2f}% (Human falsely flagged)")
    print(f"  Confusion Matrix:      TP={metrics['confusion_matrix']['true_positives']}, "
          f"TN={metrics['confusion_matrix']['true_negatives']}, "
          f"FP={metrics['confusion_matrix']['false_positives']}, "
          f"FN={metrics['confusion_matrix']['false_negatives']}")
    print(f"  Mean Latency:          {latency_summary['mean_ms']} ms (P95: {latency_summary['p95_ms']} ms)")
    print(f"  Results saved to:      {output_file}")
    print("=" * 80)

    return report


if __name__ == "__main__":
    run_real_world_benchmark(n_samples_per_class=30)
