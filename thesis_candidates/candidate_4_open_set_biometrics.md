# Thesis Candidate 4: Few-Shot Open-Set Biometric Verification & Security

## 1. Metadata
- **Working Title:** Few-Shot Device-Free Occupant Authentication and Open-Set Intruder Rejection via Locomotion Metric Learning
- **Discipline:** Security & Privacy / Deep Metric Learning / Contactless Biometrics
- **Target Venues:** ACM WiSec, IEEE Transactions on Information Forensics and Security (TIFS), IEEE IoT Journal

---

## 2. Abstract
Device-free physical security using commodity WiFi signals promises non-invasive residential access control without wearable tokens or privacy-invasive cameras. However, conventional RF biometrics suffer from two major scientific defects: (1) relying on closed-set Softmax classifiers that erroneously assign high confidence to unseen visitors and intruders, and (2) pursuing unvalidated physiological heartbeat signatures that suffer from low cardiac SNR, respiration harmonic masking, and high vulnerability to spoofing. This thesis formulates device-free occupant verification as an open-set few-shot recognition problem anchored strictly in dynamic locomotion kinematics. By leveraging deep metric learning with Cosine Margin Loss and Extreme Value Theory (EVT) distance ratios, we map walking sequences into compact hyperspherical embeddings that tightly cluster enrolled household members while establishing an adaptive rejection boundary for unknown individuals. Evaluated across multi-room locomotion benchmarks, our system demonstrates robust resident authentication and zero-shot intruder rejection without requiring prior negative training samples of unauthorized visitors.

---

## 3. Primary Research Questions
- **RQ 4.1:** How reliably can deep metric learning differentiate enrolled household members ($N \in [3, 8]$) from completely unknown visitors using only $3\text{--}5$ walking passes for enrollment?
- **RQ 4.2:** What are the empirical failure modes and False Rejection Rates (FRR) induced by everyday walking variations (e.g., carrying heavy groceries, changing footwear, altered gait speeds)?
- **RQ 4.3:** How do spatial multipath variations across different rooms corrupt gait biometric embeddings, and can domain-adversarial regularization decouple walking style from room geometry?

---

## 4. Theoretical Foundations & Mathematical Formulation
1. **Locomotion Doppler Kinematics:**
   During human bipedal walking, limbs, torso, and head translate at differential velocities, generating time-varying micro-Doppler signatures $f_D(t) = \frac{2 v_k(t)}{\lambda} \cos \theta_k(t)$. The unique combination of stride length, cadence, and limb swing reflects individual biomechanics.
2. **Deep Metric Learning with Additive Angular Margin (ArcFace):**
   $$\mathcal{L}_{\text{metric}} = -\frac{1}{N} \sum_{i=1}^{N} \log \frac{e^{s (\cos(\theta_{y_i} + m))}}{e^{s (\cos(\theta_{y_i} + m))} + \sum_{j \neq y_i} e^{s \cos \theta_j}}$$
   Enforces tight intra-class compactness and maximum inter-class angular separation in latent embedding space.
3. **Open-Set Decision Boundary via Extreme Value Theory (EVT):**
   For test embedding $\mathbf{z}$, distance to the nearest enrolled resident centroid $\mathbf{c}^*$ is evaluated against an extreme-value Weibull distribution $\mathcal{W}(\mu, \sigma, \xi)$:
   $$\mathcal{P}(\text{Enrolled} \mid \mathbf{z}) = 1 - \exp\left( -\left(\frac{\max(0, \|\mathbf{z} - \mathbf{c}^*\| - \tau)}{\sigma}\right)^\xi \right)$$
   If $\mathcal{P}(\text{Enrolled} \mid \mathbf{z}) < \delta_{\text{reject}}$, the individual is classified as \texttt{UNKNOWN\_VISITOR}.

---

## 5. Benchmarking & Experimental Plan
- **Primary Datasets:**
  - **Widar 3.0 Gait Dataset (GaitID / GaitSense):** Multi-receiver CSI captures of participants walking across diverse rooms and orientations.
  - **CSI-Bench (User Identification Task):** 20,300 samples across enrolled participants evaluated under `test_cross_user` splits.
  - **WhoFi / NTU-Fi Gait Datasets:** Multi-subject walking traces recorded across independent sessions.
- **Evaluation Protocols:**
  - Receiver Operating Characteristic (ROC): True Accept Rate (TAR) vs. False Accept Rate (FAR).
  - Equal Error Rate (EER) and Area Under the ROC Curve (AUROC).
  - Open-Set Identification F1 across varying intruder pool sizes.

---

## 6. Novelty & High-Impact Contributions
1. First systematic rejection of closed-set classifiers in WiFi security: formulating a rigorous open-set rejection boundary.
2. Explicitly correcting the literature on "WiFi heartbeat biometrics" by establishing realistic, reproducible gait-based verification.
3. Few-shot enrollment requiring $<1$ minute of walking calibration per resident.

---

## 7. Adversarial Stress-Test (Known Vulnerabilities & Risks)
- **Risk 1 (Short Walking Trajectories):** In small apartments, walking segments may be $<2$ seconds (3–4 steps), which restricts the temporal duration needed to resolve gait cadence.
- **Risk 2 (Physical State Variation):** Fatigue, temporary injury, or carrying packages alters gait kinematics, causing temporary false rejections.
- **Risk 3 (Non-Walking Postures):** Gait authentication cannot identify someone who enters while crawling, tiptoeing, or sitting on a wheelchair.

---

## 8. Feasibility & Scope Assessment
- **Scientific Impact:** High (8.5/10) — Highly relevant for cybersecurity, smart home security, and biometric verification.
- **Undergraduate Feasibility:** Very High (9.0/10) — Gait datasets are well-structured, metric learning algorithms (ArcFace, Contrastive) are mature in PyTorch, and evaluation metrics (ROC/EER) are mathematically precise.
- **Supervisor Appeal:** High for security, privacy, and pattern recognition advisors.
