#!/usr/bin/env python3
"""
Generate Hardware Capability Matrix for Thesis Gate 2 Review.
Codifies RF topologies, coherent chains, phase ratio capabilities,
and edge constraints for Intel 5300, Raspberry Pi 4B, ESP32, and ESPARGOS.
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "data" / "hardware_capability_matrix.json"

HARDWARE_MATRIX = {
    "intel_5300": {
        "platform_name": "Intel 5300 NIC (Linux 802.11n CSI Tool)",
        "rf_topology": "3x3 MIMO (Coherent Receiver Chains)",
        "coherent_rx_channels": 3,
        "frequency_bands": ["2.4 GHz", "5.825 GHz"],
        "channel_bandwidth": "20 MHz / 40 MHz",
        "subcarrier_granularity": "30 subcarrier groups per TX-RX pair",
        "phase_ratio_support": True,
        "phase_difference_support": True,
        "physical_phase_mechanism": "Hardware clock sharing across 3 onboard RF front-ends allows instantaneous inter-antenna phase subtraction and CSI ratioing, eliminating packet-level CFO.",
        "max_packet_rate_hz": 1000,
        "compute_architecture": "x86-64 host system via PCIe",
        "memory_ram": "Host RAM (>= 4 GB)",
        "power_consumption_watts": "2.0 - 5.0 W (NIC alone) + 15-30 W (Host PC)",
        "edge_tier": "Tier-3 (Edge Server / High-End Gateway)",
        "deployment_role": "High-fidelity reference benchmarking, BVP velocity profile extraction, multi-path Doppler profiling."
    },
    "raspberry_pi_4b": {
        "platform_name": "Raspberry Pi 4B (Broadcom BCM43455C0 + Nexmon CSI)",
        "rf_topology": "1x1 SISO (Single-Chain Monitor Sniffer)",
        "coherent_rx_channels": 1,
        "frequency_bands": ["2.4 GHz", "5.0 GHz (e.g. Ch 36 @ 80 MHz)"],
        "channel_bandwidth": "20 MHz / 40 MHz / 80 MHz",
        "subcarrier_granularity": "234 subcarriers (at 80 MHz) / 52 or 108 (at 20/40 MHz)",
        "phase_ratio_support": False,
        "phase_difference_support": False,
        "physical_phase_mechanism": "Single antenna receiver cannot form spatial ratio or spatial phase difference. Raw phase is corrupted by packet-level STO/CFO slopes. Sensing relies on amplitude modulus |H| or spectral Doppler.",
        "max_packet_rate_hz": 100,
        "compute_architecture": "Quad-core Cortex-A72 @ 1.5 GHz (ARMv8 64-bit)",
        "memory_ram": "2 GB / 4 GB / 8 GB LPDDR4",
        "power_consumption_watts": "3.5 - 6.5 W",
        "edge_tier": "Tier-2 (Single-Board Edge Gateway)",
        "deployment_role": "Local edge inference of deep HAR architectures (ResNet-18, TCN, BabyMamba), multi-channel amplitude tracking, local gateway state-machine coordination."
    },
    "esp32_wroom_s3": {
        "platform_name": "Espressif ESP32 / ESP32-S3 (ESP-IDF CSI API)",
        "rf_topology": "1x1 SISO (Single-Chain Transceiver with Switched Diversity)",
        "coherent_rx_channels": 1,
        "frequency_bands": ["2.4 GHz (802.11b/g/n)"],
        "channel_bandwidth": "20 MHz / 40 MHz",
        "subcarrier_granularity": "52 subcarriers (HT-LTF 20 MHz) / 114 subcarriers (40 MHz)",
        "phase_ratio_support": False,
        "phase_difference_support": False,
        "physical_phase_mechanism": "Single RF receiver chain. Switched antenna diversity uses a time-multiplexed SPDT RF switch; non-concurrent packets suffer non-zero switching latency and phase-drift discontinuities. Cannot compute true concurrent CSI ratio. Amplitude autocorrelation and relative power variance are required.",
        "max_packet_rate_hz": 200,
        "compute_architecture": "Dual-core Xtensa LX6/LX7 @ 240 MHz (32-bit)",
        "memory_ram": "512 KB internal SRAM (optional 4-8 MB PSRAM with bus latency)",
        "power_consumption_watts": "0.5 - 1.1 W (Active Wi-Fi Rx/Tx)",
        "edge_tier": "Tier-1 (Resource-Constrained Microcontroller)",
        "deployment_role": "Ultra-low-cost, battery-compatible ambient presence detection, quantized INT8 TCN / BabyMamba inference, local threshold triggering."
    },
    "espargos_array": {
        "platform_name": "ESPARGOS Coherent Antenna Array (Multi-ESP32 Synchronized)",
        "rf_topology": "Distributed Coherent Array (Shared Clock Distribution)",
        "coherent_rx_channels": 8,
        "frequency_bands": ["2.4 GHz"],
        "channel_bandwidth": "20 MHz",
        "subcarrier_granularity": "52 subcarriers per antenna element",
        "phase_ratio_support": True,
        "phase_difference_support": True,
        "physical_phase_mechanism": "Hardware distribution of shared local oscillator and clock signal across multiple synchronized ESP32 nodes restores phase coherence, enabling inter-element phase interferometry and 2D Angle-of-Arrival (AoA).",
        "max_packet_rate_hz": 150,
        "compute_architecture": "Synchronized MCU cluster with external gateway host",
        "memory_ram": "Distributed SRAM + Host RAM",
        "power_consumption_watts": "5.0 - 10.0 W",
        "edge_tier": "Tier-3 (Distributed Coherent Array Sensor)",
        "deployment_role": "High-resolution indoor localization, fine-grained AoA multipath separation without x86 Intel 5300 dependency."
    }
}

def main():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(HARDWARE_MATRIX, f, indent=2)
    print(f"[+] Wrote Hardware Capability Matrix to {OUTPUT_PATH.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
