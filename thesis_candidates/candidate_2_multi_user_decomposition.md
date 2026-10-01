# Thesis Candidate 2: Multi-Occupant Spatial-Temporal Decomposition & Pervasive Sensing

## 1. Metadata
- **Working Title:** Spatial-Temporal Blind Source Separation and Multi-User Activity Decomposition in Crowded Residential WiFi Environments
- **Discipline:** Pervasive Computing / Wireless Signal Processing / Multi-User Pervasive Systems
- **Target Venues:** ACM MobiSys, ACM SenSys, IEEE Transactions on Mobile Computing (TMC), ECCV / CVPR (Wireless Sensing Tracks)

---

## 2. Abstract
The vast majority of published WiFi CSI activity recognition and health monitoring frameworks operate under an artificial laboratory constraint: exactly one human subject moving in an otherwise empty room. In real-world domestic homes, multi-occupant co-presence is the norm. Because electromagnetic propagation obeys linear superposition, received CSI reflects the tangled superposition of simultaneous reflections from multiple moving residents, children, and pets. Conventional single-user classifiers experience catastrophic confusion in multi-user settings. This thesis tackles the multi-occupant sensing frontier. We formulate a spatial-temporal signal decomposition pipeline combining tensor factor analysis and set-prediction transformer architectures to estimate occupant counts, separate overlapping Doppler spectra, and assign concurrent activity labels. Evaluated on the WiMANS multi-user benchmark across 0 to 5 concurrent occupants, this research investigates the fundamental spatial resolution and separation boundaries of commodity wireless sensing.

---

## 3. Primary Research Questions
- **RQ 2.1:** What is the maximum number of concurrent moving occupants that can be robustly counted and separated given standard commodity MIMO antenna topologies ($2 \times 2$ vs $3 \times 3$)?
- **RQ 2.2:** How effectively can Canonical Polyadic (CP) tensor decomposition and Independent Component Analysis (ICA) disentangle overlapping Doppler trajectories when occupants cross physical paths?
- **RQ 2.3:** Does set-prediction attention (Hungarian matching) outperform traditional cascading pipelines (Count $\rightarrow$ Localize $\rightarrow$ Classify) under dynamic occupant entry and exit events?

---

## 4. Theoretical Foundations & Mathematical Formulation
1. **Multi-User Electromagnetic Superposition:**
   For $P$ active occupants in an indoor multipath environment:
   $$H(f, t) = H_{\text{static}}(f) + \sum_{p=1}^{P} \left( \sum_{m \in \mathcal{M}_p} \alpha_{p,m}(t) e^{-j 2\pi f \tau_{p,m}(t)} \right) + N(f, t)$$
   Where $\mathcal{M}_p$ represents the set of RF multipath reflection paths scattering off the body of occupant $p$.
2. **Tensor Decomposition for Multi-Source Separation:**
   Construct a 3-way CSI tensor $\boldsymbol{\mathcal{X}} \in \mathbb{C}^{M \times K \times T}$ (Antennas $\times$ Subcarriers $\times$ Time). Under rank-$R$ Canonical Polyadic decomposition:
   $$\boldsymbol{\mathcal{X}} \approx \sum_{r=1}^{R} \mathbf{a}_r \circ \mathbf{b}_r \circ \mathbf{c}_r$$
   Where factor vectors $\mathbf{a}_r$, $\mathbf{b}_r$, and $\mathbf{c}_r$ correspond to spatial antenna signatures, frequency channel responses, and temporal motion signatures of individual physical entities.
3. **Bipartite Matching Loss (Hungarian Matching):**
   To train multi-user prediction networks without pre-defined occupant ordering:
   $$\mathcal{L}_{\text{match}}(y, \hat{y}) = \min_{\sigma \in \mathfrak{S}_P} \sum_{i=1}^{P} \mathcal{L}_{\text{entity}}(y_i, \hat{y}_{\sigma(i)})$$

---

## 5. Benchmarking & Experimental Plan
- **Primary Datasets:**
  - **WiMANS (ECCV 2024):** The premier public benchmark dataset specifically designed for multi-user WiFi sensing, recording 0 to 5 concurrent participants performing everyday activities across multiple environments with fine-grained bounding boxes and identity tags.
  - **MM-Fi (2023):** Multi-modal dataset featuring multi-person indoor interaction sequences.
  - **TensorBeat / MultiSense Experimental Baselines:** Dual-person and triple-person respiration datasets.
- **Evaluation Protocols:**
  - Accuracy of Occupant Count Estimation ($P \in \{0, 1, 2, 3, 4, 5\}$).
  - Multi-label Activity Recognition Macro-F1 under concurrent locomotion.
  - Track-to-Identity Association Error across path-crossing events.

---

## 6. Novelty & High-Impact Contributions
1. Shifting wireless sensing from "single-person toy setups" to realistic multi-person domestic living.
2. First systematic evaluation comparing classical blind source separation (ICA/CP-Tensor) against modern deep set-prediction transformers on public multi-user CSI data.
3. Formalizing physical antenna bounds: proving theoretical limits on occupant separability given commercial antenna constraints.

---

## 7. Adversarial Stress-Test (Known Vulnerabilities & Risks)
- **Risk 1 (Under-determined System Limit):** When the number of concurrent occupants ($P \ge 3$) exceeds the number of coherent receive antennas ($N_{\text{RX}} \le 2$), spatial separation becomes mathematically under-determined.
- **Risk 2 (Proximity Occlusion):** When two occupants sit or stand within the same Fresnel zone ($<0.5$ m), Doppler signatures merge into a single indistinguishable component.
- **Risk 3 (Annotation Sparsity):** WiMANS clips are short (3-second duration), which limits continuous long-term tracking evaluation.

---

## 8. Feasibility & Scope Assessment
- **Scientific Impact:** Very High (9.0/10) — Highly prized at top networking and ubiquitous computing conferences.
- **Undergraduate Feasibility:** Good (7.5/10) — The WiMANS dataset is publicly accessible and Python-ready; set-prediction models can be trained on standard single-GPU setups.
- **Supervisor Appeal:** Extremely High for professors in Pervasive Systems, Mobile Computing, and IoT.
