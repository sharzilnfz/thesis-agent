# Benchmark Audit: WiFi CSI Datasets (Widar 3.0 / CSI-Bench / eHealth CSI)

Date: 2026-10-01. Purpose: verify exact released data format, license, and download availability before thesis use. No `\cite` keys emitted (per AGENTS.md Gate rules); sources are plain URLs below.

---

## 1. Widar 3.0 (Tsinghua TNS) — gesture (+ gait) CSI benchmark

**Primary sources (verified 2026-10-01):**

- Project page: http://tns.thss.tsinghua.edu.cn/widar3.0
- IEEE DataPort (DOI `10.21227/7znf-qp86`): https://ieee-dataport.org/open-access/widar-30-wifi-based-activity-recognition-dataset
- Papers: MobiSys 2019 (primary: "Zero-Effort Cross-Domain Gesture Recognition With Wi-Fi"), TPAMI 2021 extended version. Gait offshoot: GaitID (WASA 2020), GaitSense (TOSN 2021).
- CSI tool it builds on: https://dhalperi.github.io/linux-80211n-csitool

### 1.1 Raw complex CSI vs processed BVP — answer: BOTH, raw IS released

- Raw complex CSI **is** available, not BVP-only. Tsinghua "Feature File Format Illustration" defines three co-released representations:
  1. **CSI (raw):** `id-a-b-c-d-rx.dat`, where `id`=user, `a`=room, `b`=position, `c`=orientation, `d`=instance, `rx`=`r1`..`r6` (6 receivers). Loadable by the Linux 80211n CSITool MATLAB supplementary code (https://github.com/dhalperi/linux-80211n-csitool-supplementary/tree/master/matlab).
  2. **DFS:** `id-a-b-c-d.mat`, struct `6 x 121 x T` (6 receivers x 121 Doppler bins in [-60,60] Hz x time).
  3. **BVP:** `id-a-b-c-d.mat`, struct `20 x 20 x T` (x-velocity x y-velocity x time).
- Hardware encoding (cross-checked MobiSys19 Sec.6 + Wi-CBR survey + CSITool spec):
  - 1 transmitter + 6 receivers, each an Intel 5300 NIC mini-desktop, monitor mode, channel 165 @ 5.825 GHz, ~1000 packets/s.
  - Each receiver has 3 antennas in a line. Intel 5300 reports 30 subcarrier groups (complex, signed 8-bit I/Q per TX-RX pair). Denoised-CSI tensor cited in MobiSys19 is `18 (=6 Rx x 3 ant) x 30 (subcarriers) x T`.
  - So each `.dat` is one TX-RX link's raw complex trace; a full instance ideally has 6 files (r1..r6).
- Independent confirmation that raw is usable: Wi-CBR benchmark table lists Recurrent ConFormer / THAT as "Raw CSI" methods evaluated on Widar 3.0; EI uses "CSI amplitude"; Widar3.0 baseline uses CSI/DFS/BVP comparison.

### 1.2 Link configurations and known data quirks (load-bearing for thesis)

- Scale as advertised: 258K gesture instances, 8,620 minutes, 75 domains (abstract on DataPort). CSI-Bench comparison table reports 271.1k samples / 16 users / 3 envs / 1 task for Widar3.0 — use DataPort numbers as canonical, note the secondary count differs by version.
- Gestures: 6 core hand gestures visualised on Tsinghua page (Push&Pull, Sweep, Clap, Slide, Draw Circle, Draw Zigzag). Gait dataset added later ("Gait recognition dataset is available in Widar3 dataset! Stay tuned" news 2021/5).
- Domains = rooms x positions x orientations (e.g. 3 x 5 x 5 = 75). Paper setup uses "one transmitter and at least three receivers"; released files contain up to 6 receivers per instance.
- **Do not assume equal frame counts across r1..r6.** User-reported example (DataPort comments): same instance `user1-5-4-2-15` has 2545–2615 frames depending on receiver. Align by timestamps, do not stack naively into frames x Rx x SC x ant.
- 7 `.dat` files are 0-byte due to packet-loss during collection (enumerated in DataPort comments, e.g. `20181109/user2/user2-6-4-4-2-r1.dat`, `20181109/user3/user3-1-3-1-8-r5.dat`, etc.). Maintainers (Yi Zhang reply 2021-03-27) intentionally retain them and document in README — skip them at load time.
- Baidu/Tsinghua extraction codes on project page: CSI `gj8c`, DFS `v4h5`, BVP `puly`. Runtime for their reference code is legacy (CentOS 6.9, Python 3.5.0, Keras 2.0.3 + TF 1.1.0) — treat reference BVP extraction as MATLAB (`DVM_main.m`, `get_rotated_spectrum` fix 2021-12-31) rather than a modern Python pipeline.

### 1.3 File formats

- `.dat` = Intel 5300 CSITool binary (complex). No per-packet JSON; parse with CSITool readers, then denoise (amplitude noise + phase offsets per MobiSys19 Sec.3).
- `.mat` (DFS/BVP) = MATLAB matrices as above.
- RSSI also logged per abstract, but benchmark use is CSI/DFS/BVP.

### 1.4 License and download availability

- **IEEE DataPort: Open Access, DOI `10.21227/7znf-qp86`.** Requires free IEEE/DataPort login; files are listed under "Open Access data files are available to all users upon login". No explicit CC license badge on the page (unlike CSI-Bench). Last updated 2026-08-20. Cite MobiSys 2019 (requested by authors).
- Mirrors on Tsinghua page: Tsinghua Cloud disk (https://cloud.tsinghua.edu.cn/d/2760bb9557ca4d09a74d/) and Baidu Disk (https://pan.baidu.com/s/1E-iG3Oo5gYRCXGl8uykuTQ, password `4m47`). Kaggle mirror exists as a 2022 competition ("Wi-Fi Gesture Recognition Dataset (Widar3.0)") but is not canonical and had 0 submissions — do not use as source of truth.
- Practical status: **direct download available, no request gate**, but account-gated (DataPort login or Chinese cloud disks). No commercial-use grant stated; default to research-only + citation.

---

## 2. CSI-Bench (NeurIPS 2025) — in-the-wild multi-task benchmark

**Primary sources (verified 2026-10-01):**

- Paper (v2, 20 Nov 2025): https://arxiv.org/abs/2505.21866 ; full HTML: https://arxiv.org/html/2505.21866v2
- Project page: https://ai-iot-sensing.github.io/projects/project.html
- Code: https://github.com/Jenny-Zhu/CSI-Bench-Real-WiFi-Sensing-Benchmark (note: repo path uses `guozhen-jenn-zhu` in some URLs; canonical owner per paper is `Jenny-Zhu`)
- Dataset (Kaggle, Version 12): https://www.kaggle.com/datasets/guozhenjennzhu/csi-bench
- Venue: NeurIPS 2025 poster 121605. Citation: Zhu et al., "CSI-Bench: A Large-Scale In-the-Wild Dataset for Multi-task WiFi Sensing", NeurIPS 38 (2026 per repo BibTeX).

### 2.1 Released representations — answer: amplitude-only is the benchmarked default; partial raw MAT added in V12

- **Benchmarked representation is amplitude-only.** Sec. 4.2 "Amplitude extraction": with `H(f,t)` complex, input is `|H(f,t)|`, phase eliminated (phase-cleaning rejected as unable to remove initial offsets consistently across heterogeneous devices). Sec. 6 Limitations restates: "The dataset uses amplitude-only CSI features due to phase instability across platforms... limits exploration of calibrated phase or AoA."
- All baseline models (MLP, LSTM, ResNet-18, Transformer, ViT, PatchTST, TimeSformer-1D) train on amplitude-only tensors `X in R^{C x K x T}`.
- Preprocessing applied before release/training: segmentation (5 s windows; 10 s for breathing @ 30 Hz vs 100 Hz general), per-sample mean-std normalisation, subcarrier standardisation (fixed K via zero-pad/clip; loader default `win_len=500`, `feature_size=232` in `configs/csi_bench_local_config.json`).
- **Raw availability nuance (V12):** Kaggle header reads "Updated release with corrected data, reorganized task structure, resolved missing-data and reshaping issues, and added MAT raw CSI files." Repo layout confirms per-task `sub_Human_h5/` (amplitude H5, default loader path) **and** `sub_Human_mat/` (MAT raw) plus top-level `RawContinuousRecording/`. So: use H5 for reproduction of paper numbers; MAT exists for follow-up phase work but is not what paper tables report. Do not claim "raw complex parity" — paper numbers are amplitude-only.
- Hardware heterogeneity is the reason for the above: NXP 88W8997 (2x2, 58 SC @ 40 MHz/5 GHz), ESP32-S3 (1x1, 64 SC @ 20 MHz/2.4 GHz), Qualcomm IPQ4019/4018 (1x2, 128 SC @ 40 MHz / 256 SC @ 80 MHz), Broadcom BCM4345 (1x4, 14/28 SC grouped @ 20/40 MHz). Full table is Appendix A Table 7.

### 2.2 Tasks and environments covered

- Scale: 461+ hours effective, 35 users, 26 environments (apartments, multi-room houses, offices, hallways, open indoor public spaces), 16 device types (Qualcomm/Broadcom/Espressif/MediaTek/NXP; 1x1–2x2 and 1x4; 802.11n/ac/ax; 2.4/5 GHz; 20/40/80 MHz), LoS+NLoS, continuous recording with ambient interference ( Sec. 3.3–3.4). Table 1 total: 231.6k samples, 7 tasks.
- Single-task specialist sets (70/15/15 + easy/medium/hard):
  - Fall Detection: 2-class (fall vs non-fall), 6.7k samples, 17 users, 6 envs, 2 devices.
  - Breathing Detection: 2-class (breathing vs non-breathing during sleep, 30 Hz), 100k samples, 3 users, 3 envs, 6 devices. Note: binary presence, not respiration-rate regression.
  - Motion Source Recognition: 4-class (human / pet / robot / fan), 60.9k, 35 users, 10 envs.
  - Room-level Localisation: 6-way, 7.1k, 8 users, 6 envs, 8 devices.
- Multi-task co-labeled set (joint labels for efficient edge inference; 70/15/15 + cross-user / cross-env / cross-device OOD):
  - Human Activity Recognition: 5-class, 41.5k.
  - User Identification: 6 users, 20.3k.
  - Proximity Recognition: 4-class distance, 20.3k. Shared pool: 6 users, 6 envs, 11 devices.
- Layout (V12, `tasks/` prefix removed): `FallDetection/`, `BreathingDetection/`, `Localization/`, `MotionSourceRecognition/`, `Multitask/{HumanActivityRecognition,HumanIdentification,ProximityRecognition,sub_Human_h5,sub_Human_mat}/`, `RawContinuousRecording/`, each task with `metadata/sample_metadata.csv`, `label_mapping.json`, `splits/{train_id,val_id,test_id,test_easy,test_medium,test_hard,test_cross_device,test_cross_env,test_cross_user}.json`. Few-shot `*_p<digit>.json` files are auto-ignored by the loader.
- Metrics: accuracy + weighted F1; 3-seed mean±std in `RESULTS.md` (reproduces Tables 3–5, 8–14).

### 2.3 License and download availability

- **License: CC BY-NC-ND 4.0 International** — stated identically on Kaggle ("Attribution-NonCommercial-NoDerivatives 4.0"), GitHub README License section, and arXiv (CC BY-NC-ND 4.0 icon). Code page footer also shows an MIT tag for the repo scaffolding; treat **data as CC BY-NC-ND (no commercial use, no derivatives redistribution)** and check `LICENSE` file before re-hosting any subset.
- **Download: Kaggle Version 12, 81.52 GB, 352k files.** Requires free Kaggle account; no request gate. Expected update frequency listed as annually. S3 layout for SageMaker (`s3://YOUR-BUCKET/CSI-Bench/...`) mirrors the Kaggle root.
- Practical status: **direct download available**, version-pin to V12 (layout + numbers changed vs early releases; paper reproduction uses V12 + `RESULTS.md` 3-seed tables).

---

## 3. eHealth CSI (IEEE Access 2023) — vital-sign / activity dataset

**Primary source (verified 2026-10-01):**

- Paper: I. Galdino et al., "eHealth CSI: A Wi-Fi CSI Dataset of Human Activities", IEEE Access, vol. 11, pp. 71003–71012, 2023. DOI `10.1109/ACCESS.2023.3294429` (doc `10177905`): https://ieeexplore.ieee.org/document/10174340 (PDF: https://ieeexplore.ieee.org/iel7/6287639/10005208/10177905.pdf)
- Index records: https://colab.ws/articles/10.1109%2Faccess.2023.3294429 ; https://cris.ulima.edu.pe/en/publications/ehealth-csi-a-wi-fi-csi-dataset-of-human-activities
- Secondary characterisation (used only for hardware/ground-truth specifics absent from the abstract): PulseFi full paper https://arxiv.org/html/2510.24744v1 (Sec. VII-A2, Fig. 6) and short paper https://inrg.engineering.ucsc.edu/files/2025/05/Pulse_Fi_short_paper_iotdcoss.pdf (Sec. VI). These re-describe the same 118-participant Raspberry Pi dataset.

### 3.1 Vital-sign ground truth — answer: smartwatch HR (bpm) + phenotype ONLY; NO Polar H10, NO ECG, NO respiration ground truth

- Primary paper abstract wording (all three index records agree): "dataset includes participants' phenotype information and heartbeat rate monitoring data using a smartwatch." No mention of Polar H10, chest strap, ECG waveform, or respiratory belt/flow sensor.
- Secondary source identifies the watch as **Samsung Galaxy Watch 4** (PulseFi Sec. VII-A2: "Samsung Galaxy Watch 4 worn by participants for ground truth heart rate data"; short paper Sec. VI-B identical). Treat watch model as secondary-source attribution, not primary-paper fact.
- Cohort (PulseFi, reporting the eHealth collection): **118 participants (88 men, 30 women)**, age 18–64 (mean 22.38 y), height 152–198 cm, weight 40–116 kg. Controlled **3 m x 4 m room**; empty-room captures included as baseline.
- Protocol: **17 standardised positions/activities x 60 s each** (PulseFi Fig. 7). CoLab lists the activity vocabulary as EMPTY, LYING, SIT, SIT-DOWN, STAND, STAND-UP, WALK, FALL (deep-net HAR focus). Positions 5/7/9/11/13 use "alternate breathing" (20 s normal + 10 s breath-hold) and are reused by PulseFi as **apnea positive proxies** — i.e. apnea labels are protocol-derived, not sensor-derived.
- **Explicit negative findings (load-bearing):**
  - PulseFi Sec. VII-A2: "Due to extraction issues reported by dataset creators, only heart rate labels are present for the eHealth dataset, not breathing rate. Therefore, the eHealth dataset was used only for heart rate monitoring, and apnea detection."
  - No continuous ECG, no RR-intervals/HRV, no Polar H10. Any thesis claim requiring Polar H10 ECG or reference respiration rate **cannot** be validated on eHealth CSI.
- Consequence: eHealth supports (a) activity classification, (b) HR (bpm-level) regression from single-antenna amplitude, (c) protocol-derived apnea classification. It does **not** support respiration-rate regression or ECG-morphology comparison.

### 3.2 RF format and collection hardware

- TX: 5 GHz (channel 36) Wi-Fi router @ 80 MHz as transmitter; laptop as receiver; **Raspberry Pi 4B single-antenna with Nexmon firmware as CSI sniffer (234 subcarriers reported)**. Triangle spacing ~1 m (router–participant opposite sides, Pi equidistant).
- Sampling: Wi-Fi client pings router at 136 ms intervals (**~7.4 Hz**). This is sufficient for 0.1–3.5 Hz vital band with long windows (PulseFi optimum on eHealth is 30 s: MAE 0.17 BPM, MAPE 0.21%; 5 s MAE 0.76; 1 s MAE 6.11) but is an order of magnitude sparser than Widar (1000 Hz) or CSI-Bench (30/100 Hz) — window-length sensitivity must be reported.
- CSI is complex (Re/Im); single-antenna analyses (PulseFi) use **amplitude only** (`A = sqrt(Re^2+Im^2)`), deliberately avoiding phase (dominated by noise on single antenna). No multi-antenna phase-difference possible.
- File container specifics (per-subject/per-activity archive layout, `.mat` vs `.csv` field names) are **not** in the abstract/index records; the full IEEE PDF text fetch returned empty via the allowed fetcher. Flagged as unverified — confirm from the PDF or author README after access. Do not assert a container format in the thesis until then.

### 3.3 Access conditions and license

- **Access: upon request, not direct download.** All index records quote: "This dataset was made publicly available online to other researchers under request." No canonical Kaggle / IEEE DataPort / GitHub URL was found (distinguish from unrelated "CSI Human Activity" DataPort set and the 80 MHz Nexmon DataPort set). Contact is via the authors (MídiaCom, UFF — Galdino / Soto / Caballero / Ferreira / Ramos / Albuquerque / Muchaluat-Saade). Consent was obtained (PulseFi footnote).
- **Paper license vs data license:** IEEE Access paper is open access (IEEE Access default CC-BY for the article); the **dataset itself is request-gated** with no published redistribution license found. Default to closed/request-only, research-use, no re-hosting. Record the granted terms in the ledger when the authors reply.
- Practical status: **gated — email request required; expect phenotype + HR-bpm labels + CSI traces; do not expect ECG or respiration channels.**

---

## Summary answers to the three posed questions

1. **Widar 3.0: raw complex CSI available or BVP-only?** Raw complex CSI **is** released (Intel 5300 `.dat` per receiver, r1..r6, 1 Tx x 3 ant x 30 SC-groups, 5.825 GHz/1000 Hz) **alongside** DFS (`6x121xT`) and BVP (`20x20xT`) `.mat` files. File pattern `id-a-b-c-d-rx`; 6 links per instance in principle; frame counts differ per receiver; 7 zero-byte files are known/documented. Access: DataPort Open Access (login) + Tsinghua/Baidu mirrors; cite MobiSys19.
2. **CSI-Bench: raw vs amplitude? tasks/envs?** Paper benchmarks are **amplitude-only** (`|H|`, phase discarded; limitations section explicit). V12 Kaggle release **adds MAT raw** (`sub_Human_mat/` + `RawContinuousRecording/`) next to default H5 amplitude, but reproduction = H5 amplitude (`win_len 500`, `feat 232`). Tasks: 4 single-task (fall 6.7k, breath 100k binary, motion-source 4-class 60.9k, localisation 6-way 7.1k) + 3 co-labeled multi-task (HAR 5-class 41.5k, UID 6 users, proximity 4-class; 20.3k each for UID/prox). Coverage: 461 h, 35 users, 26 real-world envs, 16 device configs across 5 chipset vendors. License **CC BY-NC-ND 4.0**; Kaggle V12 81.52 GB direct download (account only).
3. **eHealth CSI: Polar H10/ECG vs respiration ground truth? access?** **Neither Polar H10 nor ECG nor respiration ground truth is provided.** Ground truth is **smartwatch HR in bpm (Samsung Galaxy Watch 4 per secondary source) + phenotype** for 118 participants in a 3x4 m room, 17 x 60 s positions/activities, Pi 4B Nexmon single-antenna 234 SC @ 80 MHz/5 GHz-ch36, ~7.4 Hz. Breathing-rate labels are absent (extraction issues per PulseFi); apnea is protocol-derived (breath-hold slots). Access is **upon-request only** (contact authors); no direct link; paper is open access but data is gated.

## Open verification items (do not cite as fact until closed)

- eHealth per-file container/column spec (needs PDF Sec. III–IV or author README).
- Widar exact gesture vocabulary count (6 core vs extended 22-class splits used in follow-ups) — pin to the TPAMI 2021 table before fixing thesis class counts.
- CSI-Bench `sub_Human_mat` completeness (which tasks/samples have raw MAT vs H5-only) — enumerate after Kaggle V12 download; current claim is existence, not parity.
- License file check on CSI-Bench download (`LICENSE` in ZIP) to confirm code-MIT vs data-CC-BY-NC-ND split before any redistribution.
