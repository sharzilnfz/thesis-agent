#!/usr/bin/env python3
"""
TinyML Edge Profiling and SRAM Budget Auditor for ThesisAgent.
Pure Python standard library implementation.
Profiles parameter memory footprint, peak intermediate activation buffers,
and theoretical inference latency for Physics-Guided TCN on ESP32-S3 and Raspberry Pi 4B.

Evaluates against hardware boundaries:
- ESP32-S3 Internal SRAM: 512 KB total (~320 KB usable DRAM/heap for ML buffers)
- Real-time packet throughput: 20 Hz minimum processing budget (<= 50 ms latency)
"""
import json
import math
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "data" / "tinyml_edge_profiling_results.json"

def profile_tcn_architecture():
    # Architecture: 4 Dilated Residual Temporal Convolutional Blocks
    # Input: (Batch=1, Channels=2 [e.g. In-phase / Quadrature or 2 antennas], Subcarriers=52, Window_Steps=100)
    input_shape = (2, 52, 100) # (C, K, T)
    feature_dim = 64 # Bottleneck feature projection

    # Layer specifications: (kernel_size, in_channels, out_channels, dilation)
    layers = [
        {"name": "input_projection_conv1d", "k": 1, "in_c": 52 * 2, "out_c": 64, "d": 1, "time_steps": 100},
        {"name": "tcn_block_1_conv1d", "k": 3, "in_c": 64, "out_c": 64, "d": 1, "time_steps": 100},
        {"name": "tcn_block_2_conv1d", "k": 3, "in_c": 64, "out_c": 64, "d": 2, "time_steps": 100},
        {"name": "tcn_block_3_conv1d", "k": 3, "in_c": 64, "out_c": 64, "d": 4, "time_steps": 100},
        {"name": "tcn_block_4_conv1d", "k": 3, "in_c": 64, "out_c": 64, "d": 8, "time_steps": 100},
        {"name": "physics_attention_fc1", "k": 1, "in_c": 64, "out_c": 16, "d": 1, "time_steps": 1},
        {"name": "physics_attention_fc2", "k": 1, "in_c": 16, "out_c": 64, "d": 1, "time_steps": 1},
        {"name": "global_pool_and_classifier", "k": 1, "in_c": 64, "out_c": 6, "d": 1, "time_steps": 1}
    ]

    total_params = 0
    total_macs = 0
    peak_activation_elements = 0

    for layer in layers:
        weights = layer["k"] * layer["in_c"] * layer["out_c"]
        biases = layer["out_c"]
        params = weights + biases
        macs = layer["k"] * layer["in_c"] * layer["out_c"] * layer["time_steps"]
        activations = layer["out_c"] * layer["time_steps"]

        total_params += params
        total_macs += macs
        if activations > peak_activation_elements:
            peak_activation_elements = activations

    # Memory calculations
    fp32_param_bytes = total_params * 4
    int8_param_bytes = total_params * 1

    # Double-buffering activation requirement (ping-pong buffer for inference engine)
    fp32_activation_bytes = peak_activation_elements * 4 * 2
    int8_activation_bytes = peak_activation_elements * 1 * 2

    fp32_total_sram_kb = (fp32_param_bytes + fp32_activation_bytes) / 1024.0
    int8_total_sram_kb = (int8_param_bytes + int8_activation_bytes) / 1024.0

    # Latency estimation:
    # ESP32-S3: 240 MHz Xtensa LX7 dual-core. SIMD PIE instructions execute ~2 MACs per cycle in optimal INT8.
    esp32_cycles_per_mac = 1.8 # with memory bus overhead
    esp32_int8_latency_ms = (total_macs * esp32_cycles_per_mac) / (240.0 * 1e6) * 1000.0

    # Raspberry Pi 4B: 1.5 GHz Cortex-A72 NEON SIMD.
    rpi4_cycles_per_mac = 0.25 # Quad-issue NEON
    rpi4_int8_latency_ms = (total_macs * rpi4_cycles_per_mac) / (1.5 * 1e9) * 1000.0
    rpi4_fp32_latency_ms = rpi4_int8_latency_ms * 2.8

    # Platform verdicts
    esp32_sram_limit_kb = 320.0 # Usable heap in 512KB SRAM
    esp32_fp32_fit = fp32_total_sram_kb <= esp32_sram_limit_kb
    esp32_int8_fit = int8_total_sram_kb <= esp32_sram_limit_kb

    profile_summary = {
        "architecture_name": "Physics-Guided Lightweight TCN",
        "total_parameters": total_params,
        "total_macs": total_macs,
        "peak_activation_elements": peak_activation_elements,
        "memory_footprint": {
            "fp32_parameters_kb": round(fp32_param_bytes / 1024.0, 2),
            "int8_parameters_kb": round(int8_param_bytes / 1024.0, 2),
            "fp32_activation_buffer_kb": round(fp32_activation_bytes / 1024.0, 2),
            "int8_activation_buffer_kb": round(int8_activation_bytes / 1024.0, 2),
            "fp32_total_sram_kb": round(fp32_total_sram_kb, 2),
            "int8_total_sram_kb": round(int8_total_sram_kb, 2)
        },
        "platforms": {
            "esp32_s3": {
                "clock_speed": "240 MHz (Xtensa LX7)",
                "usable_sram_limit_kb": esp32_sram_limit_kb,
                "fp32_deployment_possible": esp32_fp32_fit,
                "int8_deployment_possible": esp32_int8_fit,
                "int8_latency_ms": round(esp32_int8_latency_ms, 2),
                "max_inference_rate_hz": round(1000.0 / esp32_int8_latency_ms, 1),
                "verdict": "INT8 fits safely within internal SRAM with real-time throughput (>20 Hz)" if esp32_int8_fit else "OOM"
            },
            "raspberry_pi_4b": {
                "clock_speed": "1.5 GHz (ARM Cortex-A72 Quad)",
                "fp32_latency_ms": round(rpi4_fp32_latency_ms, 2),
                "int8_latency_ms": round(rpi4_int8_latency_ms, 2),
                "int8_max_inference_rate_hz": round(1000.0 / rpi4_int8_latency_ms, 1),
                "verdict": "High-throughput gateway execution with ample resource headroom"
            }
        }
    }

    print(f"[*] TinyML Model Profile:")
    print(f"    - Total Parameters: {total_params:,}")
    print(f"    - Total MACs per Inference Window: {total_macs:,}")
    print(f"    - FP32 SRAM Footprint: {fp32_total_sram_kb:.2f} KB (Fits ESP32: {esp32_fp32_fit})")
    print(f"    - INT8 Quantized SRAM Footprint: {int8_total_sram_kb:.2f} KB (Fits ESP32: {esp32_int8_fit})")
    print(f"\n[*] Hardware Execution Benchmarks:")
    print(f"    - ESP32-S3 INT8 Latency: {esp32_int8_latency_ms:.2f} ms ({1000.0 / esp32_int8_latency_ms:.1f} inferences/sec)")
    print(f"    - Raspberry Pi 4B INT8 Latency: {rpi4_int8_latency_ms:.2f} ms ({1000.0 / rpi4_int8_latency_ms:.1f} inferences/sec)")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(profile_summary, f, indent=2)
    print(f"\n[+] Wrote edge profiling summary to {OUTPUT_PATH.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    profile_tcn_architecture()
