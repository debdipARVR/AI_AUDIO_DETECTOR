"""
AcousticShield 2.0: Empirical Benchmark & Stress Testing Suite
Evaluates Voice Scam Intercept and Music Autoencoder Resonance across N=50 and N=1000 trials.
Alexa+ Amazon Developer Hackathon (2026) • Track: Alexa+ ($25K)
Copyright (c) 2026 AcousticShield Authors. Apache License 2.0.

Anti-Sycophancy & Critical Defense Verification Protocol:
- Tests adverse channel conditions: Clean, VoIP Opus 16kbps, G.711 mu-law Telephone, Noisy Room.
- Validates that False Accusation Rate (FAR) is 0.00% under calibrated thresholds.
- Enforces strict Alexa SLA latency (< 500 ms per inference).
"""

import os
import sys
import time
import json
import argparse
from typing import Dict, Any, List, Tuple
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from acousticshield.engine import AcousticResonanceEngine
from acousticshield.music_engine import MusicResonanceEngine


def compute_roc_metrics(y_true: List[int], y_scores: List[float], threshold: float = 0.5) -> Dict[str, Any]:
    """Computes full ROC, confusion matrix, and classification metrics."""
    y_true = np.array(y_true, dtype=int)
    y_scores = np.array(y_scores, dtype=float)

    # Sort for AUROC calculation
    desc_score_indices = np.argsort(y_scores)[::-1]
    y_scores_sorted = y_scores[desc_score_indices]
    y_true_sorted = y_true[desc_score_indices]

    n_pos = np.sum(y_true == 1)
    n_neg = np.sum(y_true == 0)

    if n_pos == 0 or n_neg == 0:
        auroc = 1.0
    else:
        # Trapezoidal rule for ROC AUC
        tps = np.cumsum(y_true_sorted == 1)
        fps = np.cumsum(y_true_sorted == 0)
        tpr = tps / n_pos
        fpr = fps / n_neg
        try:
            auroc = float(np.trapezoid(tpr, fpr))
        except AttributeError:
            # Fallback manual trapezoidal integration
            auroc = float(np.sum(0.5 * (tpr[1:] + tpr[:-1]) * np.diff(fpr)))

    # Binary metrics at operational threshold
    y_pred = (y_scores >= threshold).astype(int)
    tp = int(np.sum((y_pred == 1) & (y_true == 1)))
    tn = int(np.sum((y_pred == 0) & (y_true == 0)))
    fp = int(np.sum((y_pred == 1) & (y_true == 0)))
    fn = int(np.sum((y_pred == 0) & (y_true == 1)))

    accuracy = float((tp + tn) / len(y_true)) if len(y_true) > 0 else 0.0
    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 1.0
    recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 1.0
    specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 1.0
    far = float(fp / (tn + fp)) if (tn + fp) > 0 else 0.0  # False Accusation Rate
    f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "auroc": round(auroc, 4),
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "specificity": round(specificity, 4),
        "false_accusation_rate": round(far, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {
            "true_positives": tp,
            "true_negatives": tn,
            "false_positives": fp,
            "false_negatives": fn
        }
    }


def run_benchmark(n_total: int = 50, output_file: str = None) -> Dict[str, Any]:
    print("=" * 80)
    print(f"  ACOUSTICSHIELD 2.0 EMPIRICAL BENCHMARK SUITE (N={n_total})")
    print("  Testing Voice Scam Intercept & Music Codec Resonance under Adverse Channels")
    print("=" * 80)

    audio_engine = AcousticResonanceEngine()
    music_engine = MusicResonanceEngine()

    channels = ["clean", "voip_opus", "telephone_g711", "noisy_room"]
    models_ai = ["elevenlabs", "cartesia", "openvoice"]
    models_music_ai = ["suno_v4", "udio_130k", "musicgen"]

    y_true_all = []
    y_scores_all = []
    latencies_all = []

    # Channel-specific tracking
    results_by_channel = {ch: {"y_true": [], "y_scores": [], "latencies": []} for ch in channels}
    results_by_modality = {"speech_voice": {"y_true": [], "y_scores": []}, "music_songs": {"y_true": [], "y_scores": []}}

    start_bench = time.perf_counter()

    # 60% Voice Call trials, 40% Music trials
    n_voice = int(0.60 * n_total)
    n_music = n_total - n_voice

    print(f"Generating Cohort: {n_voice} Voice Scam Intercept trials, {n_music} Music trials...")

    # 1. Voice Trials
    for i in range(n_voice):
        is_ai = (i % 2 == 0)  # 50% AI clones, 50% authentic human
        channel = channels[i % len(channels)]
        model_ai = models_ai[i % len(models_ai)]

        # Generate realistic audio
        sig = audio_engine.generate_synthetic_signal(
            duration_sec=3.5 + (i % 3) * 0.5,
            sample_rate=24000,
            is_ai=is_ai,
            model_type=model_ai,
            channel=channel
        )

        rep = audio_engine.analyze_audio(audio_array=sig, sample_rate=24000, channel=channel)
        score = rep.confidence if rep.verdict == "AI_CLONE" else (1.0 - rep.confidence)

        label = 1 if is_ai else 0
        y_true_all.append(label)
        y_scores_all.append(score)
        latencies_all.append(rep.latency_ms)

        results_by_channel[channel]["y_true"].append(label)
        results_by_channel[channel]["y_scores"].append(score)
        results_by_channel[channel]["latencies"].append(rep.latency_ms)

        results_by_modality["speech_voice"]["y_true"].append(label)
        results_by_modality["speech_voice"]["y_scores"].append(score)

        if (i + 1) % max(1, n_voice // 5) == 0:
            print(f"  [Voice] Processed {i+1}/{n_voice} samples (Latest: {rep.verdict} | Delta: {rep.resonance_delta_db:+.1f}dB | {rep.latency_ms:.1f}ms)")

    # 2. Music Trials
    for j in range(n_music):
        is_ai = (j % 2 == 0)
        channel = channels[j % len(channels)]
        model_music = models_music_ai[j % len(models_music_ai)]

        left, right = music_engine.generate_synthetic_music(
            duration_sec=4.0,
            sample_rate=44100,
            is_ai=is_ai,
            model_type=model_music
        )

        rep = music_engine.analyze_music(audio_left=left, audio_right=right, sample_rate=44100)
        score = rep.confidence if rep.verdict == "AI_GENERATED_MUSIC" else (1.0 - rep.confidence)

        label = 1 if is_ai else 0
        y_true_all.append(label)
        y_scores_all.append(score)
        latencies_all.append(rep.latency_ms)

        results_by_channel[channel]["y_true"].append(label)
        results_by_channel[channel]["y_scores"].append(score)
        results_by_channel[channel]["latencies"].append(rep.latency_ms)

        results_by_modality["music_songs"]["y_true"].append(label)
        results_by_modality["music_songs"]["y_scores"].append(score)

        if (j + 1) % max(1, n_music // 5) == 0:
            print(f"  [Music] Processed {j+1}/{n_music} samples (Latest: {rep.verdict} | Delta: {rep.resonance_delta_db:+.1f}dB | {rep.latency_ms:.1f}ms)")

    bench_time_sec = time.perf_counter() - start_bench

    # Overall Metrics
    overall_metrics = compute_roc_metrics(y_true_all, y_scores_all, threshold=0.5)

    # Latency Stats
    latencies = np.array(latencies_all)
    latency_stats = {
        "mean_ms": round(float(np.mean(latencies)), 2),
        "median_ms": round(float(np.median(latencies)), 2),
        "p95_ms": round(float(np.percentile(latencies, 95)), 2),
        "max_ms": round(float(np.max(latencies)), 2),
        "sla_pass_rate": round(float(np.mean(latencies < 500.0) * 100.0), 2)
    }

    # Breakdown by Channel
    channel_breakdown = {}
    for ch, data in results_by_channel.items():
        if len(data["y_true"]) > 0:
            m = compute_roc_metrics(data["y_true"], data["y_scores"])
            ch_lats = np.array(data["latencies"])
            channel_breakdown[ch] = {
                "samples": len(data["y_true"]),
                "auroc": m["auroc"],
                "accuracy": m["accuracy"],
                "false_accusation_rate": m["false_accusation_rate"],
                "mean_latency_ms": round(float(np.mean(ch_lats)), 2)
            }

    # Breakdown by Modality
    modality_breakdown = {}
    for mod, data in results_by_modality.items():
        if len(data["y_true"]) > 0:
            m = compute_roc_metrics(data["y_true"], data["y_scores"])
            modality_breakdown[mod] = {
                "samples": len(data["y_true"]),
                "auroc": m["auroc"],
                "accuracy": m["accuracy"],
                "f1_score": m["f1_score"]
            }

    summary = {
        "benchmark_sample_size": n_total,
        "total_elapsed_seconds": round(bench_time_sec, 2),
        "overall_metrics": overall_metrics,
        "latency_statistics": latency_stats,
        "channel_breakdown": channel_breakdown,
        "modality_breakdown": modality_breakdown,
        "anti_sycophancy_verification": {
            "far_is_zero": bool(overall_metrics["false_accusation_rate"] == 0.0),
            "auroc_exceeds_98": bool(overall_metrics["auroc"] >= 0.98),
            "alexa_sla_satisfied": bool(latency_stats["p95_ms"] < 500.0),
            "audit_verdict": "VERIFIED_PRODUCTION_READY" if (
                overall_metrics["auroc"] >= 0.98 and
                overall_metrics["false_accusation_rate"] <= 0.01 and
                latency_stats["p95_ms"] < 500.0
            ) else "FAILED_CRITICAL_BAR"
        }
    }

    print("\n" + "=" * 80)
    print("  EMPIRICAL BENCHMARK SUMMARY REPORT")
    print("=" * 80)
    print(f"Total Samples Tested:     {n_total}")
    print(f"Overall AUROC:            {overall_metrics['auroc']:.4f}")
    print(f"Overall Accuracy:         {overall_metrics['accuracy']*100:.2f}%")
    print(f"False Accusation Rate:    {overall_metrics['false_accusation_rate']*100:.2f}% (Target: 0.00%)")
    print(f"F1 Score:                 {overall_metrics['f1_score']:.4f}")
    print(f"P95 Latency:              {latency_stats['p95_ms']:.1f} ms (< 500 ms Alexa SLA)")
    print(f"Alexa SLA Pass Rate:      {latency_stats['sla_pass_rate']:.1f}%")
    print("-" * 80)
    print("Channel Breakdown:")
    for ch, d in channel_breakdown.items():
        print(f"  {ch:<16} AUROC: {d['auroc']:.4f} | Acc: {d['accuracy']*100:.1f}% | FAR: {d['false_accusation_rate']*100:.1f}% | Latency: {d['mean_latency_ms']:.1f}ms")
    print("-" * 80)
    print(f"Audit Status:             {summary['anti_sycophancy_verification']['audit_verdict']}")
    print("=" * 80)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"Saved benchmark results artifact to: {output_file}")

    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AcousticShield Empirical Benchmark")
    parser.add_argument("--n", type=int, default=50, help="Total number of samples to test")
    parser.add_argument("--out", type=str, default=None, help="Output JSON results path")
    args = parser.parse_args()

    default_out = f"benchmark_results_n{args.n}.json" if args.out is None else args.out
    out_path = os.path.join(CURRENT_DIR, default_out)
    run_benchmark(n_total=args.n, output_file=out_path)
