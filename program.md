# Thesis Research Agenda & Program Specification

## 1. Project Metadata
- **Thesis Working Title:** Quality-Aware Cross-Domain WiFi CSI Sensing for Residential Home Safety: Activity Recognition, Inactivity Monitoring, and Open-Set Occupant Verification on Edge Hardware
- **Field of Study:** Computer Science / Pervasive Computing / Edge Machine Learning
- **Target Chapters:**
  - Chapter 1: Introduction, Motivation, and Problem Formulation (Environmental Shift and the False-Alert Dilemma in Ambient Home Safety)
  - Chapter 2: Literature Review, Theoretical Foundations, and the CSI Evaluation Leakage Audit
  - Chapter 3: Physics-Grounded Feature Representation and Quality-Aware Finite-State Architecture
  - Chapter 4: Cross-Domain Evaluation under Session-Disjoint, Subject-Held-Out, and Environment-Held-Out Protocols
  - Chapter 5: Embedded Edge Execution (ESP32 vs. Raspberry Pi 4), Failure Mode Analysis, Limitations, and Future Work

---

## 2. Research Scope & Constraints (Gate 1 Refined Specification)
- **Primary Research Question:**
  - How can measurement-quality-aware selective prediction and temporal state-machine gating reduce false alerts during stationary residential occupancy across unseen environments without suppressing detection of falls or prolonged immobility?
- **Secondary Questions / Sub-Tracks:**
  - **Track A (Signal Representation & Phase Stability):** Under what hardware assumptions (coherent multi-RX chains vs single-chain amplitude Doppler) do phase-difference, CSI ratio, and conjugate product representations stabilize dynamic motion features without falsely claiming complete static multipath elimination?
  - **Track B (Cross-Domain Generalization & Disentangled Encoders):** How do source-domain alignment and data augmentation techniques perform under strict Leave-One-Subject-Out (LOSO) and Leave-One-Environment-Out (LOEO) evaluation, and how can activity-invariant representations be decoupled from identity-bearing gait embeddings?
  - **Track C (Quality-Gated Finite-State Machine & Inactivity Safety):** How can a 5-state operational model (Unknown, Vacant, Occupied Active, Stationary Occupied, Alert Required) prevent false alarms during quiet rest while guaranteeing that suspected fall impacts never clear automatically upon observing respiration?
  - **Track D (Few-Shot Open-Set Occupant Verification):** How reliably can deep metric learning on walking locomotion sequences differentiate enrolled household residents from unenrolled unknown visitors without making unvalidated claims of intruder malicious intent or cardiac biometric identification?
  - **Track E (Edge Profiling & Latency Bounds):** What are the empirical memory, inference latency, and capture throughput trade-offs of lightweight Temporal Convolutional Networks (TCN) versus Selective State-Space Models (BabyMamba) on ESP32 microcontrollers and Raspberry Pi 4 platforms?
- **Inclusion Criteria:**
  - Peer-reviewed proceedings and journals in pervasive computing, wireless networking, and edge AI (ACM MobiCom, ACM MobiSys, ACM SenSys, ACM IMWUT/UbiComp, IEEE INFOCOM, IEEE TMC, IEEE SECON, NeurIPS, Patterns, IEEE IoT-J).
  - Public datasets with verifiable recording provenance, participant identifiers, and discrete environment labels (Widar 3.0, CSI-Bench, eHealth CSI, WiMANS).
  - Controlled residential pilot recordings with documented antenna topology, synchronization checks, and reference sensor ground truth.
- **Exclusion Criteria:**
  - Passive CSI heartbeat biometric identification (unvalidated on commodity hardware due to low cardiac SNR, respiratory masking, and longitudinal instability).
  - Unsafe medical inference claiming that detected respiration proves patient consciousness or cancels fall escalation.
  - Asserting room vacancy solely from low Doppler energy without exit evidence or entry/exit boundary tracking.
  - Random sliding-window shuffling across overlapping time series or non-disjoint subjects during model evaluation.

---

## 3. Active Research Milestones
- [x] **Milestone 0:** Ingest and synthesize raw corpus (93 papers in `data/raw_papers/` indexed into `data/corpus_summary.json`).
- [x] **Milestone 1:** Refine Gate 1 scope in `program.md` incorporating external audit feedback and physical constraints.
- [x] **Milestone 2:** Produce hardware capability matrix (`data/hardware_capability_matrix.json`) and dataset provenance audit (`data/benchmark_provenance_manifest.json`) for Gate 2 review.
- [x] **Milestone 3:** Extract verified mathematical proofs, baseline claims, and empirical counter-evidence into `data/evidence_ledger.json` and `data/gaps.json` (Gate 3).
- [x] **Milestone 4:** Draft full thesis chapters (Chapters 1–5) in LaTeX backed strictly by verified evidence ledger entries.
- [x] **Milestone 5:** Execute deterministic citation verification via `python scripts/verify_bibtex.py` passing with zero errors across all chapters (Gate 4).
- [x] **Milestone 6:** Implement automated LOSO/LOEO evaluation harness scripts on released benchmark datasets (Widar 3.0 and CSI-Bench) via `scripts/evaluate_zero_leakage_splits.py`.
- [x] **Milestone 7:** Execute TinyML edge emulator and profile SRAM/latency constraints for ESP32 and Raspberry Pi 4B deployments via `scripts/profile_edge_tinyml.py`.

---

## 4. Steering Directives & Methodological Rules
- **Evidence Ledger Rule:** Every citation emitted in `.tex` must resolve in `paper/references.bib` and correspond to an entry in `data/evidence_ledger.json`.
- **Zero Leakage Protocol:** Partitioning by session, subject, and room must occur prior to windowing and preprocessing. Feature scaling and normalization parameters must be computed strictly on the training partition.
- **Reporting Rigor:** Report Macro F1, Balanced Accuracy, and confusion matrices for classification; report AUROC, EER, and False Reject Rate at fixed False Accept Rate for open-set verification; report coverage versus risk curves for quality-based abstention.
- **Physical Feasibility:** Distinguish clearly between multi-antenna coherent capture (e.g. Raspberry Pi + Nexmon, Intel 5300) and single-chain switched capture (ESP32). Never assume coherent phase ratios on hardware lacking simultaneous receiver chains.
