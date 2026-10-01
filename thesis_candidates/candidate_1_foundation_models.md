# Thesis Candidate 1: Cross-Domain Invariant Representation Learning & Foundation Models

## 1. Metadata
- **Working Title:** Zero-Shot Cross-Domain WiFi CSI Sensing via Self-Supervised Invariant Feature Representations and Geometric Velocity Mapping
- **Discipline:** Deep Representation Learning / Self-Supervised Learning / Pervasive Computing
- **Target Venues:** ACM IMWUT / UbiComp, IEEE INFOCOM, ACM MobiSys, NeurIPS Datasets & Benchmarks

---

## 2. Abstract
Current deep learning models for WiFi Channel State Information (CSI) sensing exhibit catastrophic performance collapse when deployed in uncalibrated physical spaces, often losing 25–40% in recognition accuracy due to environmental multipath shifts. While supervised domain adaptation requires target-domain calibration samples, real-world smart environments require true zero-shot cross-domain generalization. This thesis explores the design and evaluation of a self-supervised foundation model for ambient RF sensing. By pretraining masked temporal-spectral autoencoders across large-scale in-the-wild datasets (CSI-Bench and MM-Fi) coupled with coordinate-invariant physical projections (Body-coordinate Velocity Profiles), we formulate a representation backbone that decouples human kinematics from room-specific electromagnetic scattering. We benchmark cross-environment, cross-user, and cross-device transfer under strict Leave-One-Environment-Out (LOEO) protocols, demonstrating that physically constrained self-supervised pretraining establishes generalizable spatial intelligence without target data.

---

## 3. Primary Research Questions
- **RQ 1.1:** How significantly does self-supervised masked subcarrier reconstruction improve out-of-distribution (OOD) generalization compared to supervised empirical risk minimization across unseen rooms?
- **RQ 1.2:** Under what mathematical transformations (e.g., Doppler Velocity Profiles vs. Raw Spectrograms) do latent representations become invariant to room geometry while retaining fine-grained human action dynamics?
- **RQ 1.3:** How do heterogeneous RF front-ends (bandwidths, antenna numbers, subcarrier grouping) degrade foundation model transfer, and can unified subcarrier interpolation bridge cross-device disparities?

---

## 4. Theoretical Foundations & Mathematical Formulation
1. **Narrowband Multipath Modeling:**
   $$H(f, t) = \sum_{l=1}^{L} \alpha_l(t) e^{-j 2\pi f \tau_l(t)} = H_{\text{static}}(f) + H_{\text{dynamic}}(f, t)$$
   Where $H_{\text{static}}(f)$ represents room-specific static reflections that must be disentangled from dynamic reflections $H_{\text{dynamic}}(f, t)$.
2. **Self-Supervised Masked CSI Pretraining:**
   Given a CSI spectrogram tensor $\mathbf{X} \in \mathbb{R}^{C \times K \times T}$, a subset of time-frequency patches $\mathcal{M}$ is randomly masked. The encoder-decoder network $\mathcal{F}_{\theta}$ minimizes the reconstruction loss:
   $$\mathcal{L}_{\text{MAE}} = \frac{1}{|\mathcal{M}|} \sum_{(k,t) \in \mathcal{M}} \|\mathbf{X}(k, t) - \hat{\mathbf{X}}(k, t)\|^2_2$$
3. **Domain-Adversarial Invariance Constraint:**
   $$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{task}} - \lambda \mathcal{L}_{\text{domain}}(\mathcal{D}(\mathbf{z}), d_{\text{env}})$$

---

## 5. Benchmarking & Experimental Plan
- **Primary Datasets:**
  - **CSI-Bench (NeurIPS 2025):** 461 hours, 35 users, 26 real-world environments, 16 commercial devices. Provides official `test_cross_env` and `test_cross_device` partitions.
  - **Widar 3.0 (ACM MobiSys):** 258,000 instances, 75 domain permutations (3 rooms $\times$ 5 positions $\times$ 5 orientations) with co-released BVP velocity profiles.
  - **MM-Fi (2023):** Multi-modal 4D dataset providing synchronized LiDAR, RGB-D, and CSI across multiple rooms.
- **Evaluation Split:** Strict Leave-One-Environment-Out (LOEO) and Leave-One-Device-Out (LODO).

---

## 6. Novelty & High-Impact Contributions
1. Moving beyond single-room supervised HAR to a generalizable RF foundation model.
2. Direct ablation of self-supervised pretraining objectives (Masked Autoencoding vs. Contrastive Learning vs. Autoregressive Prediction) on wireless channel data.
3. Establishing reproducible zero-shot transfer baselines on CSI-Bench without data leakage.

---

## 7. Adversarial Stress-Test (Known Vulnerabilities & Risks)
- **Risk 1 (Compute Bottleneck):** Pretraining large transformer foundation models on 461 hours of CSI requires multi-GPU infrastructure (NVIDIA A100/H100), which may strain undergraduate compute allocations.
- **Risk 2 (Phase Incoherence):** CSI-Bench releases amplitude-only features because phase is corrupted across heterogeneous hardware; this prevents pure complex phase-based AoA pretraining.
- **Risk 3 (Novelty Collision):** Concurrently emerging preprints (e.g., AM-FM 2026, DoRF++ 2026) are already investigating foundation models, raising the bar for architectural novelty.

---

## 8. Feasibility & Scope Assessment
- **Scientific Impact:** Extremely High (9.5/10)
- **Undergraduate Feasibility:** Moderate to Challenging (6.5/10) due to GPU compute and training dataset scale.
- **Supervisor Appeal:** High, especially for machine learning and AI-focused faculties.
