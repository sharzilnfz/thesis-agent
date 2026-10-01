# Thesis Candidate 3: Contactless Healthcare, Vital Signs & Safety-Critical Fall Monitoring

## 1. Metadata
- **Working Title:** Contactless Cardiopulmonary Vital Signs and Fall Emergency Sensing with Physics-Gated Inactivity State Machines
- **Discipline:** Digital Health / Biomedical Pervasive Computing / Safety-Critical Cyber-Physical Systems
- **Target Venues:** ACM Transactions on Computing for Healthcare (HEALTH), IEEE Journal of Biomedical and Health Informatics (J-BHI), ACM IMWUT

---

## 2. Abstract
Ambient residential safety systems for elderly care face a severe operational dilemma: false alarm fatigue during quiet sedentary rest versus catastrophic missed detections during acute fall emergencies. Contactless Channel State Information (CSI) from commodity WiFi offers a non-wearable, privacy-preserving solution to monitor both macroscopic falls and subtle cardiopulmonary chest displacements. However, prevailing literature suffers from two hazardous flaws: (1) unvalidated claims of passive heartbeat biometrics on single-link transceivers, and (2) medically unsafe logic where detected respiration is misconstrued as patient safety, improperly canceling fall alerts. This thesis establishes a clinically grounded, physics-aware home safety framework. We introduce a dual-antenna CSI ratio front-end that isolates respiratory rhythms down to 0.1 Hz without specialized radar, and formulate a 5-state Finite State Machine governed by two strict medical safety invariants: detected respiration acts as an observability indicator during stationary rest, but is strictly prohibited from suppressing fall emergency escalations. Evaluated across CSI-Bench, eHealth CSI, and clinical reference datasets, this work delivers a verifiable, safety-certified framework for domestic health monitoring.

---

## 3. Primary Research Questions
- **RQ 3.1:** How effectively does dual-antenna CSI ratioing ($\mathcal{R} = H_1 / H_2$) isolate respiratory rhythms across varying room positions compared to single-antenna amplitude demodulation?
- **RQ 3.2:** What are the empirical detection limits and SNR thresholds for separating true human respiration from environmental mechanical oscillations (e.g., HVAC units, rotating fans)?
- **RQ 3.3:** Can a 5-state uncertainty-aware Finite State Machine reduce false absence/inactivity alerts by $>85\%$ during quiet sedentary rest while maintaining $100\%$ alert retention during verified fall impact events?

---

## 4. Theoretical Foundations & Mathematical Formulation
1. **Chest Wall Phase Modulation:**
   A minute physiological displacement $d(t) = d_{\text{resp}}(t) + d_{\text{cardiac}}(t)$ alters the dynamic path length $d_k(t) = 2 d(t)$, inducing phase modulation:
   $$\Delta \phi(t) = \frac{2\pi}{\lambda} \Delta d(t) = \frac{2\pi f_c}{c} (2 d(t))$$
   At 5 GHz ($\lambda \approx 6$ cm), a $5$ mm chest expansion yields $\Delta \phi \approx 1.05$ rad (readily observable), whereas a $0.5$ mm heartbeat yields $\Delta \phi \approx 0.10$ rad (easily buried in noise).
2. **CSI Ratio Sanitization (FarSense):**
   $$\mathcal{R}(f_k, t) = \frac{H_1(f_k, t) e^{j \theta_{\text{noise}}(t)}}{H_2(f_k, t) e^{j \theta_{\text{noise}}(t)}} = \frac{H_1(f_k, t)}{H_2(f_k, t)}$$
   Cancels packet-level clock jitter on simultaneous coherent receive chains.
3. **Medical Safety Invariant 1 (Non-Suppression Rule):**
   $$\text{If } \mathcal{S}_t = \texttt{STATE\_ALERT\_REQUIRED} \implies \mathcal{S}_{t+\tau} \neq \texttt{STATE\_STATIONARY\_OCCUPIED} \quad \forall \, \tau \in [0, T_{\text{reset}}]$$
   Regardless of whether periodic respiration $\hat{f}_{\text{resp}} \in [10, 24] \text{ bpm}$ is detected post-impact.

---

## 5. Benchmarking & Experimental Plan
- **Primary Datasets:**
  - **CSI-Bench (Fall & Breathing Subsets):** 6,700 real-world fall samples; 100,000 sleep breathing samples across 3 environments and 6 devices.
  - **eHealth CSI (IEEE Access 2023):** 118 participants, 17 standardized posture/activity tasks, Raspberry Pi 4B Nexmon sniffer.
  - **VitalCSI Dataset (Sensors 2026):** Seated and resting vital signs verified against clinical nasal airflow reference sensors.
- **Evaluation Protocols:**
  - Fall Sensitivity, Specificity, and False Alarm Rate per 24 hours.
  - Respiration Mean Absolute Error (MAE in breaths/min) against clinical reference.
  - State Machine Transition Latency and Stability under multipath dead zones.

---

## 6. Novelty & High-Impact Contributions
1. First WiFi sensing framework to formalize medical safety invariants preventing fall emergency suppression.
2. Replacing binary "presence/absence" detectors with a 5-state uncertainty-aware lifecycle (Unknown, Vacant, Active, Stationary, Alert).
3. Rigorous characterization of single-chain vs multi-chain hardware bounds in contactless vital sign monitoring.

---

## 7. Adversarial Stress-Test (Known Vulnerabilities & Risks)
- **Risk 1 (Destructive Fresnel Nulls):** When an occupant lies in a multipath blind spot where chest displacement is orthogonal to the RF ellipse, dynamic reflection power drops below the noise floor.
- **Risk 2 (eHealth Ground Truth Limits):** eHealth CSI contains smartwatch HR bpm but *lacks continuous ECG and respiration reference*, requiring careful decoupling of vital sign claims.
- **Risk 3 (Non-human Periodic Confounders):** Rotating fans (5–25 Hz) can leak harmonics into the vital sign band (0.2–3.0 Hz).

---

## 8. Feasibility & Scope Assessment
- **Scientific Impact:** Extremely High (9.5/10) — Highly publishable in digital health, pervasive computing, and medical informatics.
- **Undergraduate Feasibility:** Excellent (8.5/10) — Benchmark datasets (CSI-Bench Fall, eHealth) are readily available; state-machine logic can be fully simulated and verified deterministically.
- **Supervisor Appeal:** Unanimously High — Interdisciplinary crossover between computer science, IoT, and healthcare technology.
