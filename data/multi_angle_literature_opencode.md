# Multi-Angle Literature Audit: Multi-User Sensing/BSS + WiFi Foundation Models (2024–2026)

Date: 2026-10-01. Scope: (1) multi-user sensing and blind source separation — WiMANS (ECCV 2024), AMAR (2026), MultiSense (MobiCom 2020, still the canonical BSS reference reused by 2024–2026 work); (2) foundation models and self-supervised pretraining — AM-FM (Feb 2026), DoRF++ (Sep 2026, incl. DoRF CAMSAP 2025 / ICASSP 2026 prelims), SSL tutorial-cum-survey (COMST 2025). Focus: mathematical representations, released datasets/weights, limitations. No LaTeX citation keys are emitted (per project protocol); sources are plain URLs.

---

## PART 1 — Multi-user sensing and blind source separation

### 1.1 WiMANS (ECCV 2024) — the multi-user benchmark all later methods train on

Sources: paper https://arxiv.org/abs/2402.09430 , ECCV PDF https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/05826.pdf , poster https://eccv.ecva.net/virtual/2024/poster/1818 , code https://github.com/huangshk/wimans , data https://www.kaggle.com/datasets/shuokanghuang/wimans

**Mathematical representation.**

- Raw sample: dual-band CSI tensor per 3-second window. Transmitter and receiver each have 3 antennas, 30 subcarriers per antenna pair, so instantaneous CSI is `3 x 3 x 30` and a full sample is `3000 x 3 x 3 x 30` (3000 packets at ~1000 Hz). Synchronised video is 90 frames at 30 Hz, 3 RGB channels.
- Released in two forms: `wifi_csi/mat/*.mat` (raw complex, loaded with `scipy.io.loadmat`) and `wifi_csi/amp/*.npy` (amplitude, loaded with `numpy.load`). Labels in `annotation.csv` (read with `pandas.read_csv(dtype=str)`): per-sample (anonymised) user identities, locations, activities; occupancy `Np` ranges 0–5 users performing identical or different activities simultaneously.
- Benchmark formulation used by the authors and reused by AMAR/SSL-survey: multi-label classification over an identity×activity matrix with independent binary cross-entropy, plus location and activity heads. Metrics are per-task accuracy (identity / location / activity) split by band (2.4 / 5 GHz) and environment (classroom / meeting room / empty room). Representative numbers: THAT reaches ~94–98% identity but only ~58–64% HAR, which is the headroom AMAR targets.

**Released datasets/weights.**

- Dataset: 11,286 samples, 9.4+ hours, dual band (2.4 + 5 GHz) + synchronised `.mp4` video, Kaggle direct download (free account). Repo provides `benchmark/wifi_csi/{preset,preprocess,run}.py` (models ST-RF, MLP, LSTM, CNN-1D/2D, CLSTM, ABLSTM, THAT) and `benchmark/video/*` (ResNet, S3D, MViT-v1/v2, Swin-T/S) with `environment.yaml` (Ubuntu 20.04, Python 3.9.12, PyTorch 2.0.1). No pretrained weights are released; `preprocess.py` recomputes amplitude from `mat/` but the `amp/` folder is already provided so this step is optional.
- License: no explicit dataset license badge on the Kaggle/GitHub pages audited; default to research-only with citation of `huang2024wimans` (arXiv 2402.09430). Confirm before redistribution.

**Limitations (load-bearing for thesis).**

- Only 3 rooms, single TX–RX link geometry, scripted 3-second clips — not continuous in-the-wild data (contrast CSI-Bench 26 environments / 461 h). Cross-environment claims beyond classroom/meeting/empty-room are extrapolations.
- Identity-coupled label matrix encourages user-specific features rather than generalisable activity patterns (the exact critique AMAR Sec. 2.2 makes). Combinatorial label explosion with `Np` up to 5.
- Amplitude `.npy` is the path every baseline actually uses; raw `.mat` phase is available but uncalibrated across the two bands. Single-link only — no multi-AP diversity (cf. MultiTrack/MUSE-Fi discussion in AMAR Sec. 2.1).
- Video is reference/pose-estimation material, not a synced vital-sign ground truth.

### 1.2 AMAR (2026) — set-prediction + edge-cloud RVQ, current best on WiMANS multi-user HAR

Sources: paper HTML https://arxiv.org/html/2605.20649v1 , code https://github.com/amirhosseinmhd/AMAR (linked from Sec. 1 footnote)

**Mathematical representation.**

- CSI measurement model (Sec. 3.1). For a MIMO-OFDM system with `Nt` TX, `Nr` RX antennas and `Nsc` subcarriers, CSI at time `t`, subcarrier `k` is the multipath sum `x(t,k) = sum_{p=1..P} alpha_p(t) exp(-j 2 pi f_k tau_p(t))`, collected over a window `T` as a complex tensor in `C^{T x Nr x Nt x Nsc}`.
- Edge preprocessing converts to amplitude and flattens to `X in R^{T x C}` with `C = Nr Nt Nsc` (justified by cross-subcarrier/antenna correlation). Backbone is depthwise-separable convolutions (denoise + compress, `O(kd Cd_in + Cd_in Cd_out)` vs `O(kd Cd_in Cd_out)`) followed by atrous convolutions with dilation `d_a^{(i)} = 2^{i-1}` for multi-scale temporal features, ending in `Z in R^{Tz x Dz}`.
- Core novelty (Sec. 3.2–3.3): multi-user HAR as **set prediction**. Target is an unordered multiset `y = {y1..yNp}`, `yi` in `{1..Nact}`, `Np` unknown. This cuts the hypothesis space from `(Nact)^{Np}` ordered sequences to `C(Nact+Np-1, Np)` multisets (46× reduction for `Nact=9, Np=5`). Fixed output size `Nq` (max occupancy) with a `null` ("no person") class pads the target to `~y`; loss is Hungarian-matched cross-entropy `L(~y, ^y) = min_{sigma} sum_i Lcls(~yi, ^y_{sigma(i)})` solved in `O(Nq^3)`. No occupancy pre-estimation, no signal decomposition, no identity/location auxiliary labels.
- Edge-cloud compression (Sec. 4.2): residual vector quantisation over `V` codebooks of size `kappa`. Per-frame `z_t` is quantised to `b_t^{(0)} = Q^{(0)}(z_t)`, residuals `r_t^{(v+1)} = r_t^{(v)} - b_t^{(v)}` passed onward, final `b_t = sum_v b_t^{(v)}`. Capacity grows as `kappa^V`. Training loss is commitment + codebook `L_RVQ = sum_{v,t} [||r - sg[b]||_2 + beta ||sg[r] - b||_2]` with layer-wise dropout; deployment transmits only integer index sequences `Gamma^{(v)}` (`log2(kappa)` bits each), cloud reconstructs from synchronised codebooks. Reported: >99.2% bandwidth reduction, 0.32 M total parameters.
- Cloud: transformer encoder (long-range temporal) + decoder with `Nq` learnable query embeddings ("activity detectors") via cross-attention to CSI encodings and self-attention between queries for interdependent predictions, trained end-to-end with the matching loss.
- Evaluation (Sec. 5–6, WiMANS classroom/meeting/empty-room): count-based precision/recall/F1, Perfect Prediction Score (all concurrent activities correct), Occupancy Counting Error. Headline: F1 53.4% vs 45.6% best baseline, PPS ~1.72× best baseline (≈doubles perfect-prediction rate), OCE −74%.

**Released datasets/weights.**

- Code repository linked above; no weight file was advertised in the audited HTML version — assume train-from-scratch on WiMANS. Evaluation datasets are WiMANS splits (Sec. 5.1); baselines compared are BCE-based (WiMANS multi-label), DEM-based, and MultiSenseX (two-stage localise-then-classify). No new dataset is released.

**Limitations.**

- Evaluated only on WiMANS (3 rooms, single-link, scripted clips). No cross-dataset (CSI-Bench), cross-device, or continuous-daily-activity proof.
- Requires fixing `Nq` (max occupancy) at design time; `null`-class trick avoids explicit counting but does not remove the capacity ceiling.
- RVQ assumes synchronised edge/cloud codebooks and is trained for discriminative HAR only (unlike EfficientFi/RSCNet reconstruction objectives) — bit-rate/accuracy tradeoff outside HAR is untested.
- Absolute accuracy remains modest (F1 ~53%, HAR per-class ~60% regime on WiMANS) — entanglement is reduced, not solved; occlusion and same-activity multi-user cases remain hard.
- Comparison is against WiMANS-era baselines; no comparison to CSI-Bench-trained or foundation-model (AM-FM) backbones.

### 1.3 MultiSense (MobiCom 2020) + MultiResp (TMC 2023) — canonical BSS formulation for multi-person respiration

Sources: paper PDF https://hal.science/hal-03363355/file/3411816.pdf , DOI https://dl.acm.org/doi/10.1145/3411816 , follow-up limitations https://taogu.site/pub/paper/23-tmc-MultiResp.pdf , demo https://www.youtube.com/watch?v=mMl5o11QuVU

**Mathematical representation.**

- Key modelling claim (verified in Sec. 4 of the PDF): with carefully processed multi-antenna CSI, reflected signals from multiple breathers are **linearly mixed at each antenna**, so multi-person respiration is a blind source separation problem `x(t) = A s(t)` where `s(t)` holds per-person breathing waveforms and `A` is the unknown mixing matrix from chest motion through multipath. Solved with independent component analysis (ICA) after conjugate-multiplication / ratio preprocessing that suppresses sampling and carrier offsets while preserving periodic chest-motion phase. Each separated component is then tracked as one person's detailed respiration waveform (not just a rate number).
- Reported: up to 4 simultaneous persons with mean absolute respiration-rate error on the order of ~0.5 bpm in the tested room (exact number varies by distance/orientation; cite the PDF table, not the ResearchGate snippet).

**Released datasets/weights.**

- None found in the audit. System description only; no Kaggle/DataPort set, no code or weights linked from the HAL record. Treat as method reference, not a reusable artefact.

**Limitations (explicit, including from the MultiResp follow-up which lists them to motivate its own design).**

- Requires a priori (or separately estimated) person count; cannot adapt cleanly to dynamic entry/exit during monitoring.
- Fails or degrades when subjects face away, are blocked by furniture/other subjects, or sit beyond ~6 m / in too-large rooms (weak multipath, low SNR).
- Cannot separate subjects with identical or near-identical breathing rates (difference < ~1 bpm) — ICA independence assumption breaks.
- Single-room, static-posture evaluation; motion artefacts (walking, fidgeting) are out of scope. No occupancy + HAR joint task.
- Thesis implication: BSS/ICA is the correct classical baseline for multi-person vital signs, but the 2024–2026 HAR line (WiMANS/AMAR) deliberately avoids explicit decomposition because the linear-mixing assumption does not hold for general overlapping activities.

---

## PART 2 — Foundation models and self-supervised pretraining

### 2.1 AM-FM (Feb 2026) — first WiFi ambient-intelligence foundation model

Sources: paper HTML https://arxiv.org/html/2602.11200v1 (arXiv 2602.11200, CC BY-NC-ND 4.0), authors Zhu, Hu, Jayaweera, Gao, Wang, Zhang, Wang, Wu, Liu (Origin Research / HKU)

**Mathematical representation.**

- Input (Sec. 3.3): raw CSI parsed to complex `H in C^{Ntx x Nrx x Nsub x T}`, flattened over space–frequency to `X in C^{F x T}` (`F = Ntx Nrx Nsub`), amplitude `A = |X|` (phase discarded for commodity-hardware robustness), segmented into non-overlapping windows `S_i in R^{L x F}`, zero-padded to `Fmax`, per-segment min–max normalised to [0,1], stored HDF5. Target packet rate 100 Hz; streams below 2/3 of target are discarded.
- Architecture (Sec. 4.1): adaptive frequency aggregation via cross-attention compressing `F` subcarriers to `F' = 10` latent channels `z_t = sum_f alpha_{tf} (W_v x_{tf} + p_f)` with `alpha_{tf} = softmax_f(q^T (W_k x_{tf} + p_f)/sqrt(d))` (5–11× compression, handles heterogeneous subcarrier quality and non-local multipath correlations); relative temporal bias `Attn_{ij} = softmax(q_i^T k_j/sqrt(dk) + b_{ij}) v_j`, `b_{ij} = f_theta(j-i)` for translation-invariant respiration/gait/gesture periods (0.2–0.5 / 1–2 / 2–5 Hz). Encoder is 6-layer transformer, `d = 256`, 8 heads; 3-layer reconstruction decoder. Configurations: Small 2 M, Base 5 M, Large 12 M.
- SSL (Sec. 4.2): joint `L = 1·L_CL + 4·L_REC + 3·L_ACF`. (i) NT-Xent contrastive `L_CL` (`tau = 0.2`, MLP projection, 9 domain-informed augmentations: Gaussian noise, amplitude modulation for AGC/path-loss, temporal shift/crop, frequency perturbation/masking, blur). (ii) Masked reconstruction `L_REC = ||^X - X||_2^2` masking 10% temporal blocks + 10% frequency bands but reconstructing the full signal (packet-loss / selective-fading surrogate). (iii) Physics-informed autocorrelation prediction: `s_t = E_f[X_{tf}^2]`, `ACF[k] = sum_{t<T-k} s_t s_{t+k} / sum_t s_t^2` (FFT), MLP regresses first `K = 50` lags, `L_ACF = ||^ACF - ACF(X)||_2^2` (rewards rhythmic motion structure).
- Adaptation (Sec. 4.4): frozen-encoder Temporal Probe `^y = g_phi(LSTM(z1..zT))` vs Bottleneck Adapters `A_l(h) = W_up GELU(W_down h)` (`d = r = 192`, 6 layers, ~393 K params, <3% encoder, zero-init `W_up`). Optimiser AdamW, `lr = 1e-3` downstream (`1e-4` pretrain, warmup 10 + cosine, FP16, 8×A100, batch 256, grad-clip 1.0, 200 epochs).
- Pretraining data (Sec. 3.1, App. B): 439 days continuous (24/7, 6–9 concurrent links/env), ~20 TB / 9.2 M samples, 20 commercial device types (33 physical instances), 8 chipset families (MediaTek, Qualcomm, Broadcom, Espressif, NXP, Marvell, Realtek, Altobeam), 1×1–2×2 MIMO, 20/40/80 MHz @ 2.4/5 GHz, >20 dB RSSI spread, 11 environments (576–3,800 sq ft, 1–3 floors), 26 users, natural daily activity.
- Downstream (Sec. 5, App. E): 9 tasks on CSI-Bench (fall, HAR, UID, localisation, MSR, occupancy, proximity), SignFi (276-class gesture; text says 279-way in one table — flag as typo), WiFiCam (imaging SSIM/PSNR). Metric AUROC (95% bootstrap CI). Base+BA exceeds 0.90 on all 8 classification tasks (e.g. HAR 0.923 vs scratch 0.527, proximity 0.936 vs 0.494, localisation 0.995 vs 0.631); gesture needs adapters (TP 0.634 → BA 0.999); UID/MSR already separable under TP. Imaging 0.726 SSIM / 18.87 PSNR. Few-shot (`K = 5–500`/class): pretraining dominates at low `K` (localisation scratch ~0.27 flat vs AM-FM 0.925 at `K = 500`); inter-class distance grows 14–52× (mean 25.9×). Scaling: Base > Small on most tasks; Large degrades on several (fixed 9.2 M-scale data bottleneck).

**Released datasets/weights.**

- Pretraining set (20 TB in-the-wild) and model weights: **no public download found** in the audited HTML version (no Kaggle/HuggingFace/GitHub link). Downstream evaluation reuses public sets (CSI-Bench, SignFi, WiFiCam). Treat AM-FM as architecture + training recipe + reported numbers, not yet a reusable checkpoint. Recheck before depending on it; the CSI-Bench repo (same first authors) is the closest public artefact.

**Limitations.**

- Amplitude-only (`|X|`), so phase/AoA/ToF techniques are out of scope by construction.
- Pretraining corpus is private; reproducibility and cross-lab fine-tuning are blocked until weights/data appear.
- Classification-centric (AUROC); regression (continuous rate/position) and long-horizon tracking are not demonstrated.
- Large-model degradation shows data, not capacity, is the ceiling — scaling claims need broader collection.
- Adaptation guidance is task-dependent (probe suffices for UID/MSR/localisation/occupancy; adapters required for fine-grained gesture) — no single adaptation recipe.

### 2.2 DoRF++ (Sep 2026) — Doppler-radiance + spherical transformer for cross-user robustness

Sources: paper HTML https://arxiv.org/html/2608.08381v2 (arXiv 2608.08381, CC BY-NC-ND 4.0), authors N. Hasanzadeh, S. Valaee (Toronto); prelims CAMSAP 2025 / ICASSP 2026; project page https://dorf.navidhasanzadeh.com (returned an unpacking stub at audit time)

**Mathematical representation.**

- CSI estimation (Sec. II-A): per-subcarrier `x = H_{fc} s_tx + n`, LS estimate `H^{LS}_{fc} = Y_p S_p^H (S_p S_p^H)^{-1}`; multipath `H^{fc}_{m,n}(s) = sum_l beta_l(s) exp(-j 2 pi d_{m,n,l}(s) fc / c)`.
- Phase sanitisation (Sec. II-B, novel): **common-RX stream ratio** `H^{fc}_{m1,m2,n}(s) = ^H^{fc}_{m1,n}(s) / ^H^{fc}_{m2,n}(s)` from two TX antennas to the same RX antenna. Cancels receiver-wide + chain-dependent STO/SFO (conventional same-TX/different-RX ratios leave `Delta rho`/`Delta eta` residuals). Full impairment model with CSD/STO/SFO/beamforming terms is Eq. 4.
- Motion model (Sec. II-C): per-component path change `Delta L_p ≈ v^T r_p t = g_p ||v|| t cos theta_p = v_p t`, delay `Delta tau_p = Delta L_p/c`, channel evolution `H_{m,n}^{fc}(s+t) ≈ sum_p H_{p,m,n}^{fc}(s) exp(-j 2 pi fc Delta tau_p)`. Each resolvable (or blurred group) component is a 1-D virtual camera on the shared 3-D velocity `v`.
- Doppler extraction (Sec. II-D): per common-RX ratio stream, windowed MUSIC on subcarrier snapshots `C_i(s) = (1/Nsc) sum_k h_{i,k} h_{i,k}^H`, pseudospectrum `P^{(i)}_{MUSIC}(f) = 1 / a^H U_N U_N^H a`, peak `f_i^*(s)`, velocity `v_r = lambda f`, `lambda = c/fc`. Keeps only the dominant peak per stream/time (`N = 6` streams per RX in their setup); more robust than delay-bin methods (e.g. MORIC) especially at 5 GHz where timing-error phase scales with `fc`.
- Radiance field (Sec. III): stack projections to `V_r in R^{T x N}`, factorise `V_r = V R + E` with `V in R^{T x 3}` (latent velocity) and `R in R^{3 x N}` (effective Doppler vectors). Objective `min_{V,R} (1/2TN)||V_r - VR||_F^2 + (mu/2T)||V||_F^2 + (gamma/2N)||R||_F^2` via alternating ridge updates initialised from rank-3 truncated SVD, with a closed-form SVD global solution and latent-frame ambiguity analysis. Re-project `v(s)` onto a fixed equiangular unit-sphere grid `P(s,u,w) = v(s)^T d_{uw}`, `P in R^{T x M x 2M}` — sparse environment-dependent views become a dense comparable spherical field.
- Recognition (Sec. IV, DoRF++ proper): per-direction temporal features → spherical tokens → quadrature-aware spherical self-attention (relative encoding depends only on inter-direction angle) → pooling + multi-DoRF (per-RX) permutation-invariant fusion → classifier. Key distinction: DoRF is the representation, DoRF++ is the spherical model on it (prior DoRF+order-invariant classifier discarded angular organisation).

**Released datasets/weights.**

- Evaluation is on the authors' own challenging hand-gesture set with a **single multi-antenna receiver AP**; cross-user generalisation is the headline (beats SOTA HAR and DoRF+generic classifier, especially on difficult gestures). No public dataset, code, or checkpoint link was present in the audited version (project page stub). Prelims at CAMSAP/ICASSP do not add artefacts.

**Limitations.**

- Single-AP, hand-gesture-only proof; no multi-user, multi-room, or multi-device evaluation.
- Requires multi-TX (multiple TX-antenna pairs per RX) to form ratios; single-TX deployments cannot use the sanitiser as stated.
- Dominant-peak MUSIC + quasi-static window assumption discards secondary Doppler components; fast/composite motions violate the local-stationarity premise.
- Spherical grid (`M x 2M`) and quadrature transformer add compute vs order-invariant pooling — edge feasibility is unaddressed.
- Environment-dependent effective directions are learned per deployment; "comparable across environments" rests on re-projection, not on cross-environment data shown.

### 2.3 SSL tutorial-cum-survey (COMST 2025) — what transfers and what does not

Sources: preprint HTML https://arxiv.org/html/2506.12052v1 (arXiv 2506.12052, CC BY 4.0), authors Radwan, Yildirim, Hasanzadeh, Tabassum, Valaee; journal version Radwan et al., IEEE COMST 2025 (DOI record `11071965` in the HTML header); companion evaluation Xu et al., ACM TOSN 2025

**Mathematical representation (taxonomy the thesis can reuse).**

- CSI fundamentals + measurement (active vs passive), motion-induced Doppler/ToF/AoA, testbed mechanics.
- Extraction tools compared: 802.11n CSI Tool (Intel 5300, 30 groups), Atheros, WARP, Nexmon (Broadcom, up to 242 data subcarriers @ 80 MHz), ESP32.
- Preprocessing (Sec. IV): outlier removal (smoothing/Hampel/KF/WT/anomaly), phase compensation (common-phase-error, phase-difference, CSI-ratio model), compression (PCA, low-rank factorisation), transforms (FFT/STFT/WT/MUSIC/BVP/MiniRocket).
- SSL (Sec. VI): cluster-discrimination, end-to-end contrastive, memory-bank, momentum-encoder, instance-discrimination, hybrid. Contrastive: SimCLR, MoCo (and SwAV); non-contrastive: BYOL, SwAV, Barlow Twins, VICReg, SimSiam, MAE, SimMIM. Mechanics of positive-pair construction and collapse-avoidance are elaborated for CSI (augmentation sensitivity is higher than vision because time–frequency structure is easily destroyed).
- Experiments (Sec. VII): SimCLR, VICReg, Barlow Twins, SimSiam + supervised baselines on **WiMANS (multi-user multi-label), UT-HAR, SignFi**, with few-shot fine-tuning and transfer (including WiMANS transfer). Augmentations, encoder, and compute are ablated.

**Released datasets/weights.**

- Survey only: no new dataset or checkpoint. Value is the qualitative dataset table (Sec. III-C: HAR / gesture-sign / health-specialised / other, with specs and shortcomings) and the quantitative SSL comparison harness described in Sec. VII (re-implement from the listed methods; no weights file).

**Limitations (the survey's own conclusions — directly usable as thesis gap statements).**

- SSL ≈ supervised **same-domain**, especially few-shot; cross-task and cross-environment/domain adaptation remains weak (data quality, environment, and task-specific variation dominate).
- Prior SSL evaluations are mostly intra-dataset (user/room/receiver shifts within Widar/CSIDA); extreme cross-dataset/cross-task tests are missing — the survey's WiMANS/UT-HAR/SignFi extension is a step but still classification-only.
- Open datasets are scarce and heterogeneous (formats, rates, antenna/subcarrier counts, annotation quality); synchronisation and annotation cost are the bottleneck, not architectures.
- Privacy (identity leakage through motion biometrics), lightweight design for edge (memory/bandwidth), and multi-modal (CSI+vision/depth) learning are listed as open opportunities (Sec. VIII). No regression, tracking, or vital-sign SSL is benchmarked.

---

## Cross-cutting synthesis for the thesis

- Representation ladder (increasing geometry-awareness): raw complex CSI → amplitude → ratio/sanitised phase → delay/Doppler projections → DoRF spherical field → SSL/foundation embeddings (contrastive + masked + ACF). The 2026 direction is **Doppler/spherical for robustness** (DoRF++) and **amplitude + SSL at scale for transfer** (AM-FM); BSS/ICA remains the respiration-specific classical tool.
- Multi-user: WiMANS proves single-link multi-label HAR stalls near ~60% activity accuracy; AMAR shows set-prediction + queries + RVQ is the current best fix (+8 pp F1, 1.72× perfect-prediction, −74% counting error, 0.32 M params, −99.2% bandwidth) but still single-dataset and modest in absolute terms. True multi-user vital signs (≥2 simultaneous breathing/HR traces from one link) is **not** demonstrated by any 2024–2026 HAR method audited — MultiSense covers respiration for ≤4 static persons only.
- Foundation models: AM-FM is the only large-scale WiFi FM audited (9.2 M / 20 TB / 8 families / 11 envs) with a reusable recipe (adaptive frequency attention + relative time + CL/MAE/ACF + probe/adapter), but weights/data are private and Large-scale training already saturates. DoRF++ is the strongest cross-user gesture result with one AP but also private. The COMST survey confirms SSL matches supervision in-domain yet fails cross-task — exactly the gap a thesis combining AM-FM-style pretraining with DoRF-style physics features on CSI-Bench + WiMANS + eHealth would fill.
- Artefact reality check: downloadable today are **WiMANS (Kaggle + GitHub benchmarks)** and the **survey's evaluation datasets (WiMANS/UT-HAR/SignFi)**; **AMAR code** is linked; **MultiSense, AM-FM weights/data, DoRF++ data/weights** were not publicly released at audit time. Plan experiments around WiMANS + CSI-Bench (+ eHealth for HR) and re-implement AMAR/SSL/DoRF-preprocessing from papers.

## Open verification items

- AMAR repo liveness and weight/config parity with the arXiv v1 numbers (F1 53.4%, PPS, OCE) — clone and run the WiMANS preset before citing as baseline.
- AM-FM weight/data release status — recheck (no link in v1 HTML); if released, record URL + license (paper is CC BY-NC-ND 4.0) in the provenance manifest.
- DoRF++ dataset/code release — recheck project page (stub at audit); confirm TX-antenna requirement against available hardware (needs ≥2 TX antennas per RX for common-RX ratios).
- SignFi class-count typo (276 vs 279) and WiMANS activity vocabulary Version — pin to dataset `annotation.csv` / README before fixing thesis class counts.
