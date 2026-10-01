# Multi-Thesis Exploration & Scientific Selection Framework

## Purpose
This directory houses the comprehensive exploration of multiple competing thesis candidates in the WiFi Channel State Information (CSI) sensing domain. Rather than prematurely narrowing down to a single angle without validation, this workspace formulates, stress-tests, and benchmarks five distinct research avenues to enable rigorous comparative analysis.

---

## The Candidate Theses Portfolio

| Candidate ID | Focus Track | Core Paradigm | Key Datasets | Primary Technical Lever |
| :--- | :--- | :--- | :--- | :--- |
| **Candidate 1** | **Foundation Models & Invariance** | Deep Representation Learning | CSI-Bench, Widar 3.0, MM-Fi | Self-supervised masked autoencoding, spherical Doppler velocity mapping (BVP/DoRF++) |
| **Candidate 2** | **Multi-User Decomposition** | Pervasive Signal Processing | WiMANS, MM-Fi, Widar 3.0 | Blind source separation, tensor decomposition (TensorBeat), set-prediction attention (AMAR) |
| **Candidate 3** | **Cardiopulmonary & Fall Safety** | Digital Health & Safety FSM | eHealth CSI, CSI-Bench, VitalCSI | Dual-antenna CSI ratioing (FarSense), spectral breath fusion, non-suppression safety state machines |
| **Candidate 4** | **Open-Set Biometric Verification** | Security & Metric Learning | Widar 3.0 (GaitID), CSI-Bench, WhoFi | Deep metric learning (Cosine margin / ArcFace), Extreme Value Theory (EVT) unknown rejection |
| **Candidate 5** | **TinyML Bare-Metal Execution** | Embedded Systems & Edge AI | ESP32 capture streams, SenseFi | INT8 quantization, SRAM buffer optimization (512KB ESP32 limit), lightweight TCN / BabyMamba |

---

## The Synthesis: "Multiplying All of Them"
In addition to the five individual candidates, **`multiplied_synthesis_framework.md`** establishes how a modular, unified master architecture synthesizes the strengths of all five angles:
- **Representation Backbone:** Invariant Doppler features (from Candidate 1).
- **Spatial Pre-Filter:** Multi-user source separation (from Candidate 2).
- **High-Level Reasoning:** Safety-critical 5-state FSM (from Candidate 3).
- **Access Control:** Open-set gait metric authentication (from Candidate 4).
- **Execution Target:** Sub-50ms quantized INT8 execution on bare-metal microcontrollers (from Candidate 5).

---

## Evaluation Dimensions
Each candidate is evaluated in `candidate_matrix_comparison.md` across:
1. **Scientific Novelty:** Extent of contribution beyond published 2024–2026 baselines.
2. **RF Physical Rigor:** Realism regarding multi-path, hardware phase drift, and SNR constraints.
3. **Empirical Data Availability:** Availability of public, licensed raw/amplitude benchmarks.
4. **Feasibility within Undergrad Timeline:** Realistic deliverability within 4–6 months.
5. **Hardware & Compute Cost:** Need for specialized x86 hardware vs cheap commodity microcontrollers.
6. **Risk Profile:** Falsifiability and potential failure modes.
7. **Supervisor Appeal:** Clear, demonstrable impact to academic review committees.
