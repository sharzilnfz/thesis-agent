# Multi-Thesis Comparative Analysis & Evaluation Matrix

## 1. Comprehensive Comparison Matrix

| Evaluation Dimension | Candidate 1: Foundation Models & Generalization | Candidate 2: Multi-User Decomposition | Candidate 3: Vital Signs & Fall Safety FSM | Candidate 4: Open-Set Biometric Verification | Candidate 5: TinyML Bare-Metal Execution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Discipline** | Deep Learning / Representation Theory | Pervasive Computing / Signal Processing | Digital Health / Safety Cyber-Physical Systems | Cybersecurity / Biometrics / Metric Learning | Embedded Systems / Edge AI / TinyML |
| **Core Problem Solved** | Catastrophic 35% accuracy collapse across unseen rooms | Destructive interference when 2–5 occupants move concurrently | Dangerous false alarms during rest; premature clearing of fall alerts | Flawed closed-set classifiers; impossible heartbeat biometrics | High-power x86 cloud dependence; privacy leaks from raw CSI streams |
| **Primary Technical Lever** | Masked CSI Autoencoders & Velocity (BVP) Invariance | CP-Tensor Decomposition & Set-Prediction Transformers | Dual-antenna CSI ratio ($\mathcal{R}=H_1/H_2$) & 5-State Safety FSM | Cosine Margin (ArcFace) & Extreme Value Theory (EVT) | INT8 Quantized TCN vs. Selective State-Space Models (Mamba) |
| **Key Datasets** | CSI-Bench (461h), Widar 3.0, MM-Fi | WiMANS (ECCV 2024), MM-Fi, MultiSense | CSI-Bench Fall/Breath, eHealth CSI, VitalCSI | Widar 3.0 GaitID, CSI-Bench User-ID, WhoFi | ESP32-S3 Capture Streams, CSI-Bench, SenseFi |
| **Hardware Required** | High-end GPU Cluster (NVIDIA A100/RTX 4090) | Standard Single GPU (RTX 3080/4070 or Colab) | Standard Laptop / GPU + Simulation | Standard Single GPU (RTX 3070/Colab) | $5 ESP32-S3 Dev Board + Laptop |
| **Scientific Impact (1–10)** | **9.5 / 10** (Frontier AI topic) | **9.0 / 10** (Major pervasive sensing frontier) | **9.5 / 10** (Immediate life-safety societal value) | **8.5 / 10** (Strong security & privacy value) | **9.0 / 10** (High practical engineering impact) |
| **Undergraduate Feasibility (1–10)** | **6.5 / 10** (Compute-heavy; training foundation models is costly) | **7.5 / 10** (WiMANS dataset ready, but Hungarian loss has learning curve) | **8.5 / 10** (Datasets ready; FSM mathematically deterministic) | **9.0 / 10** (Standard metric learning libraries in PyTorch) | **9.5 / 10** (Low hardware cost; concrete profiling results) |
| **Theoretical Rigor** | High (Self-supervised bounds, domain invariance proofs) | Very High (Tensor rank algebra, electromagnetic superposition) | High (Fresnel diffraction, bio-kinematics, state invariants) | High (Hyperspherical embeddings, EVT Weibull distributions) | High (Quantization arithmetic, DMA concurrency, linear SSM) |
| **Falsification Risk** | Phase incoherence across devices forces amplitude-only | Under-determined when occupants > antennas ($P > N_{\text{RX}}$) | Fresnel dead zones reduce respiration SNR | Non-walking postures (sitting/crawling) cannot be verified | Complex C/C++ firmware debugging on ESP-IDF |
| **Supervisor Appeal** | AI / Deep Learning / Vision & Language Labs | Pervasive Systems / Wireless Networking Labs | Biomedical Engineering / IoT / Digital Health Labs | Cybersecurity / Applied Cryptography / Privacy Labs | Embedded Systems / Computer Architecture / Edge AI Labs |

---

## 2. Dimensional Strengths & Trade-Offs

### Candidate 1 (Foundation Models & Generalization)
- **Strengths:** Hits the absolute hottest academic buzzword ("Foundation Models for Ambient Wireless Intelligence"). High citation potential if successful.
- **Weaknesses:** Requires substantial GPU compute to train across hundreds of hours of raw CSI. High risk of competing preprints (AM-FM, DoRF++) appearing concurrently.

### Candidate 2 (Multi-User Decomposition)
- **Strengths:** Solves the most glaring real-world critique of wireless sensing ("What happens when your spouse walks into the room?"). Evaluators always ask this question.
- **Weaknesses:** High mathematical complexity in tensor decomposition; physical limitation when occupants outnumber antenna paths.

### Candidate 3 (Vital Signs & Fall Safety FSM)
- **Strengths:** Solves life-safety problems with undeniable real-world healthcare impact. The medical safety invariant (respiration never clears a fall) is intellectually bulletproof and immediately impresses evaluators.
- **Weaknesses:** Requires careful handling of public vital sign datasets (acknowledging that eHealth CSI has smartwatch HR but lacks reference respiration).

### Candidate 4 (Open-Set Biometric Verification)
- **Strengths:** Mathematically clean and elegant formulation (Metric Learning + EVT). Clear distinction between realistic gait kinematics and impossible heartbeat claims.
- **Weaknesses:** Only works when subjects are walking; does not cover stationary posture identification.

### Candidate 5 (TinyML Bare-Metal Execution)
- **Strengths:** The most feasible and tangibly demonstrable undergraduate project. Examiners love seeing a working $5 microcontroller doing real-time inference on an LED or serial monitor without cloud servers.
- **Weaknesses:** Microcontroller RF front-ends are single-chain (SISO), which precludes complex multi-antenna phase ratioing.

---

## 3. How to Choose Based on Your Committee & Faculty Strengths

- **If your supervisor specializes in Machine Learning / Deep Learning:** $\rightarrow$ Select **Candidate 1** (Foundation Models) or **Candidate 4** (Metric Learning).
- **If your supervisor specializes in Wireless Networks / Pervasive Computing:** $\rightarrow$ Select **Candidate 2** (Multi-User Decomposition) or **Candidate 3** (Vital Signs & Fall Safety).
- **If your supervisor specializes in Embedded Systems / IoT / Hardware:** $\rightarrow$ Select **Candidate 5** (TinyML Bare-Metal Execution).
- **If you want the ultimate, unbeatable thesis that synthesizes the best of everything:** $\rightarrow$ Select the **Unified Multiplied Framework** (detailed in `multiplied_synthesis_framework.md`).
