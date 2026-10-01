#!/usr/bin/env python3
"""
Generate Benchmark Provenance Manifest for Thesis Gate 2 Review.
Codifies benchmark datasets, released representations, hardware origins,
ground truth modalities, and zero-leakage evaluation split specifications.
"""
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "data" / "benchmark_provenance_manifest.json"

BENCHMARK_MANIFEST = {
    "widar_3_0": {
        "dataset_name": "Widar 3.0: Zero-Effort Cross-Domain Activity Recognition",
        "institutional_source": "Tsinghua University (TNS Lab)",
        "doi": "10.21227/7znf-qp86",
        "primary_papers": ["MobiSys 2019", "IEEE TPAMI 2021"],
        "hardware_infrastructure": {
            "transceivers": "1 Transmitter + 6 Distributed Receivers (Intel 5300 NIC)",
            "antenna_count": "1 TX antenna x 3 RX antennas per receiver (18 spatial channels total)",
            "rf_band": "5.825 GHz (Channel 165, 20 MHz bandwidth)",
            "subcarriers": "30 subcarrier groups per TX-RX pair (signed 8-bit I/Q)",
            "sampling_frequency_hz": 1000
        },
        "released_representations": {
            "raw_csi": "Binary .dat files containing raw complex CSI for receivers r1 through r6",
            "dfs": "MATLAB .mat structures (6 x 121 x T) capturing Doppler Frequency Shifts in [-60, 60] Hz",
            "bvp": "MATLAB .mat structures (20 x 20 x T) capturing 2D Body-coordinate Velocity Profiles"
        },
        "vocabulary_and_tasks": {
            "core_gestures": 6,
            "gesture_classes": ["Push&Pull", "Sweep", "Clap", "Slide", "Draw Circle", "Draw Zigzag"],
            "extended_vocabularies": ["Gait locomotion sequences (GaitID/GaitSense)"],
            "scale": "258,000 instances, 8,620 minutes, 75 domain permutations (3 rooms x 5 positions x 5 orientations)"
        },
        "known_data_quirks": [
            "Asynchronous receiver frame counts (instances have differing frame counts between r1 and r6; requires timestamp alignment).",
            "7 documented 0-byte corrupt files due to collection packet drop (e.g. user2-6-4-4-2-r1.dat, user3-1-3-1-8-r5.dat)."
        ],
        "zero_leakage_split_spec": {
            "loso_protocol": "Train on 12 subjects, hold out 3-4 distinct subjects entirely from feature normalization and model fitting.",
            "loeo_protocol": "Train on Rooms 1 and 2, evaluate zero-shot transfer on Room 3 across all orientations.",
            "sliding_window_rule": "Window slicing strictly executed POST-split. No overlapping windows spanning train and test sets."
        }
    },
    "csi_bench": {
        "dataset_name": "CSI-Bench: A Large-Scale In-the-Wild Dataset for Multi-task WiFi Sensing",
        "institutional_source": "NeurIPS 2025 (Zhu et al.)",
        "doi_or_url": "https://www.kaggle.com/datasets/guozhenjennzhu/csi-bench (Version 12)",
        "license": "CC BY-NC-ND 4.0 International",
        "hardware_infrastructure": {
            "devices": "16 commercial device configurations across 5 chipset vendors (Qualcomm IPQ4019, Broadcom BCM4345, Espressif ESP32-S3, MediaTek, NXP 88W8997)",
            "mimo_configurations": "1x1, 1x2, 2x2, and 1x4 antenna topologies",
            "rf_bands": "2.4 GHz and 5 GHz (20 MHz, 40 MHz, and 80 MHz channel widths)",
            "sampling_frequency_hz": "100 Hz for locomotion/activity, 30 Hz for sedentary sleep breathing"
        },
        "released_representations": {
            "benchmarked_format": "Amplitude-only |H(f,t)| stored in HDF5 (sub_Human_h5) with win_len=500, feature_size=232",
            "raw_format": "Partial MAT raw CSI files (sub_Human_mat) and RawContinuousRecording in V12 release",
            "phase_treatment": "Phase discarded in paper benchmarks due to platform-specific oscillator phase instability across heterogeneous devices"
        },
        "vocabulary_and_tasks": {
            "fall_detection": "2-class (fall vs non-fall), 6,700 samples across 17 users and 6 environments",
            "breathing_detection": "2-class binary presence during sleep, 100,000 samples across 3 users and 3 environments",
            "motion_source_recognition": "4-class (human, pet, robotic vacuum, oscillating fan), 60,900 samples across 35 users and 10 environments",
            "room_localization": "6-way indoor room identification, 7,100 samples across 8 users and 6 environments",
            "human_activity_recognition": "5-class activity classification, 41,500 samples",
            "user_identification": "6 enrolled occupants, 20,300 samples",
            "proximity_recognition": "4 distance tiers, 20,300 samples"
        },
        "zero_leakage_split_spec": {
            "cross_user_split": "test_cross_user.json strictly isolates test participants from training embeddings.",
            "cross_environment_split": "test_cross_env.json holds out physical indoor testing apartments.",
            "cross_device_split": "test_cross_device.json evaluates domain transfer from high-end routers to resource-constrained IoT nodes."
        }
    },
    "ehealth_csi": {
        "dataset_name": "eHealth CSI: A Wi-Fi CSI Dataset of Human Activities",
        "institutional_source": "Universidade Federal Fluminense (MídiaCom Lab) / IEEE Access 2023",
        "doi": "10.1109/ACCESS.2023.3294429",
        "hardware_infrastructure": {
            "sniffer_node": "Raspberry Pi 4B with Nexmon firmware (Broadcom BCM43455C0)",
            "antenna_count": "1 single receiving antenna (SISO monitor mode)",
            "rf_band": "5.0 GHz (Channel 36 @ 80 MHz channel width)",
            "subcarriers": "234 subcarriers extracted per CSI packet frame",
            "sampling_frequency_hz": "7.4 Hz (136 ms ping intervals between client and router)"
        },
        "vital_sign_ground_truth": {
            "heart_rate_modality": "Smartwatch PPG/heart rate (Samsung Galaxy Watch 4, bpm reporting)",
            "respiration_ground_truth": "ABSENT (extraction errors reported by creators; no breathing rate sensor)",
            "ecg_ground_truth": "ABSENT (no continuous ECG electrodes, no Polar H10 chest strap, no RR intervals)",
            "apnea_modality": "Protocol-derived breath-hold intervals (20s normal + 10s breath-hold during designated postures)"
        },
        "cohort_scale": "118 diverse participants (88 male, 30 female, age 18-64), 17 standardized posture/activity tasks x 60 s each in a 3m x 4m room",
        "zero_leakage_split_spec": {
            "subject_disjoint_cv": "118 participants partitioned into 5 non-overlapping folds (approx. 23-24 distinct subjects per validation fold).",
            "windowing_constraints": "Long temporal windows (30s required for ~7.4 Hz low sampling rate) must not bridge boundary transitions between active and stationary states."
        }
    }
}

def main():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(BENCHMARK_MANIFEST, f, indent=2)
    print(f"[+] Wrote Benchmark Provenance Manifest to {OUTPUT_PATH.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
