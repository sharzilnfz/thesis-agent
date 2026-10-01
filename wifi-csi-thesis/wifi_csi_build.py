import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = "/Users/sharzilnafis/WiFi_CSI_Paper_Analysis_50.xlsx"

HEADERS = ["Serial","Paper Name","Problem Description","Problem Statement Source","Root Cause Identification","Corrective Actions / Method","Status","Follow-up & Review (Results)","Future Plans","Effectiveness Assessment","Additional Notes"]

ROWS = [
[1,"Ma et al. 2019 CSI Survey, ACM CSUR","Fragmented CSI sensing lacks unified taxonomy and models","Intro: ubiquitous sensing gap, CSI underused","RSSI coarse, CSI potential unsystematized, no pipeline standard","Taxonomy of detection, recognition, estimation methods","Completed - Published Survey","Organized 100+ works, clarified CSI advantages","Robust multi-user, through-wall sensing","High - foundational reference","Baseline for later surveys"],
[2,"Liu et al. 2019 Wireless Sensing Survey, IEEE COMST","No comprehensive signal-metric comparison for sensing","Intro: device-free sensing needs across metrics","RSS/CSI/FMCW/Doppler diverse, never compared fairly","Compared RSS, CSI, FMCW, Doppler across tasks","Completed - Published Survey","CSI best resolution-cost tradeoff shown","Deep learning and multimodal fusion","High - broad comparative guide","Covers RFID/acoustic beyond WiFi"],
[3,"Chen et al. 2023 Cross-Domain Survey, ACM CSUR","Models fail across environments, users, devices","Intro: domain-shift collapse in deployment","Env/hardware variations distort CSI fingerprints","Surveyed transfer, adversarial, disentanglement methods","Completed - Published Survey","Categorized generalization methods + benchmarks","Domain-invariant foundation models needed","High - cross-domain design core","Focus HAR, localization, estimation"],
[4,"Miao et al. 2025 HAR Survey, ACM CSUR","HAR lacks standardized pipeline and datasets","Intro: HAR fragmentation","Inconsistent preprocessing, models, eval protocols","Unified framework sampling to classification","Completed - Published Survey","Compared datasets, features, deep models","Real-time edge and open-set HAR","High - HAR systematization","Segmentation + benchmarks emphasis"],
[5,"Wang et al. 2025 Generalizability Survey, COMST arXiv:2503.08008","Poor cross-domain generalization limits deployment","Intro: reproducibility crisis","Overfitting to lab data, no standard benchmarks","Reviewed theory, methods, datasets; SDP platform","Completed - Preprint Survey","Mapped physical-data and algorithmic fixes","Standardized eval, causal models","High - timely synthesis","Flags dataset scarcity/leakage"],
[6,"SSL for WiFi Sensing Tutorial, IEEE COMST 2025","Labeled CSI data scarce and costly","Intro: annotation bottleneck","Manual labeling impractical across domains","Tutorial on contrastive, generative, masked SSL","Completed - Published Tutorial","SSL matches supervised with few labels","Multimodal, theory-grounded SSL","High - practical SSL guide","Includes pipelines/code guidance"],
[7,"Sai et al. 2026 ML Review, IEEE IoT-J","ML model selection for WiFi sensing unclear","Intro: ML proliferation confusion","Many models, no comparative guidance","Reviewed supervised, deep, hybrid ML","Completed - Published Review","Benchmarked accuracy/complexity/robustness","Lightweight edge, federated learning","Medium-High - practitioner guide","Covers vitals + security"],
[8,"Halperin et al. 2011 CSI Tool","No accessible 802.11n CSI for research","Closed firmware hid subcarrier data","NICs hid channel measurements from researchers","Modified Intel 5300 firmware/driver/utilities","Completed - Tool Released","30-subcarrier CSI on commodity laptops","Wider bandwidth, more platforms","High - sparked field","Sparked modern CSI wave"],
[9,"Nexmon CSI 2017-2019 (Gringoli/Schulz)","Broadcom devices lacked CSI extraction","Smartphone sensing barrier","Closed firmware, no CSI APIs","Patched Broadcom firmware for CSI","Completed - Open Source","Phone/Raspberry Pi CSI capture","Higher bandwidth, stability","High - mobile enabler","80 MHz multi-device setups"],
[10,"PicoScenes 2020-2022","Tools inflexible across protocols","Fragmented single-NIC tools","Single-protocol tools restrict research","Unified multi-NIC SDR-like middleware + plugins","Completed - Maintained","WiFi/LTE/BT support, sync measurements","UWB, mmWave, real-time","High - unified platform","High-rate sync measurements"],
[11,"ESPARGOS Phase-Coherent CSI 2024 arXiv:2408.16377","Commodity CSI lacks cross-antenna phase coherence","Hardware limitation discussion","Independent PLLs/RF chains desync phases","ESP32 multi-antenna coherent array + calibration","Completed - Validated + Open","Coherent AoA gains over Intel 5300","Scale array, ML pipelines","High - cheap coherent research","Thesis-grade experiment enabler"],
[12,"Adib & Katabi See Through Walls SIGCOMM 2013","Detect moving humans behind walls, device-free","Through-wall tracking need","Wall attenuation + multipath obscure reflections","MIMO nulling of static clutter + Doppler tracking","Completed - Prototype","Tracked up to 3 people through walls","Activity recognition, multi-room imaging","High - launched field","Foundation for device-free/fall"],
[13,"Wang et al. E-eyes MobiCom 2014","Daily in-home activity recognition device-free","Need without wearables","Activity CSI profiles vary with env; RSSI coarse","Multi-link CSI histogram fingerprints + joint classification","Completed - 2 homes","Nine activities ~96% same-env","Env change, continuous activities","Medium - accurate but env-sensitive","Pre-deep-learning histograms"],
[14,"Wang et al. CARM MobiCom 2015","HAR breaks across locations/persons","Location/person-dependent CSI variation","Amplitude fingerprints couple activity + geometry","CSI-speed Doppler-power model + location-independent features","Completed - multi-room","~96% across unseen locations","Larger vocab, real-time","High - first model-based cross-location","Bridge fingerprints to physics"],
[15,"Kotaru et al. SpotFi SIGCOMM 2015","Commodity AoA localization coarse","Indoor accuracy limits","Few antennas, noisy phase, multipath, STO","Joint AoA-ToF MUSIC + smoothing + likelihood fusion","Completed - Intel 5300","Median 40cm, beats ArrayTrack/Ubicarse","Outdoor, 3D tracking","High - standard baseline","Reused MUSIC pipeline"],
[16,"Xiong & Jamieson ArrayTrack NSDI 2013","APs cannot locate clients accurately, few antennas","MIMO AP localization need","Small arrays wide beams, false AoA peaks","Modified MUSIC + spatial smoothing + multi-AP triangulation","Completed - WARP testbed","Median 23cm LOS office","NLOS robustness, NIC porting","High for its time","Precursor to SpotFi"],
[17,"Gjengset et al. Phaser MobiCom 2014","Distributed antenna calibration costly","Phased-array calibration cost","CFO/SFO across radios kill coherence","Shared-antenna handoff sync across Intel 5300","Completed - Prototype","Decimeter without dedicated calibration","Large-scale, mobility","Medium - superseded later","Low-cost phased-array idea"],
[18,"Wang et al. RT-Fall TMC 2016","Real-time fall vs daily-activity separation","Elderly fall monitoring gap","Falls resemble sitting/lying in amplitude","Segmentation on CSI phase difference + SVM","Completed - lab + home","~91% sensitivity, low false alarms","Multi-person, NLOS homes","High - practical detector","Thesis fall baseline"],
[19,"PhaseFi / CSI Fingerprinting Deep 2015-2016","Raw CSI phase unusable; handcrafted fails cross-env","Calibrated phase + deep features need","STO/SFO/CFO randomize phase","Linear sanitization + autoencoder/LSTM classifiers","Completed - Intel 5300 sets","Meter-to-decimeter gains over RSSI","Cross-site, lighter models","Medium - still site-bound","Shift to learned features"],
[20,"Vasisht et al. Chronos NSDI 2016","Single-AP narrowband cannot do sub-meter","Single-AP decimeter need","20-40 MHz poor ToF resolution","Multi-band CSI hopping synthesizes wideband ToF","Completed - Prototype","Median 65cm single-AP","Mobility, power, real-time hopping","High - single-AP wideband","Complements AoA/SpotFi"],
[21,"Qian et al. Widar MobiCom 2017","Passive tracking lacked accuracy without training","Statistical learning too deployment-heavy","No geometric CSI-Doppler-location model","Doppler-location-velocity model + trajectory recovery","Completed - Intel 5300","Median 25cm, velocity err ~13%","Multiperson 3D, richer sensing","High - no per-site training","Single-target 2D office eval"],
[22,"Qian et al. Widar2.0 MobiSys 2018","Joint gesture+tracking hurt by offsets/ambiguity","Widar single-person, no semantics","SFO/STO + multipath corrupt Doppler-AoA","Multicarrier calibration + joint Doppler-AoA + segmentation","Completed - Prototype","Submeter tracking, high gesture accuracy","Dense multiperson, continuous activities","High - unified framework","Adds vocab + sync"],
[23,"Zheng et al. Widar3.0 MobiSys 2019","Gesture accuracy collapses cross-domain","Primitive DFS features domain-dependent","Env-coupled features, weak spatial resolution","Body-coordinate velocity profile BVP + CNN-GRU","Completed - 258K 75-domain set","92.7% in-domain, 82.6-92.4% zero-effort cross","Gait, fall, larger vocab","High - explainable generalization","Multi-link BVP + deep classifier"],
[24,"Ma et al. SignFi IMWUT 2018","Prior work under 25 hand-only gestures","Need full sign language coverage","Small vocabs + noisy CSI + weak classifiers","Preprocessed CSI to 9-layer CNN","Completed - Public data + code","98.0% lab, 94.8% combined, 86.7% multiuser","Cross-user, sentence-level signing","High single-user; medium multiuser","276 signs, 8280 instances"],
[25,"Zeng et al. FarSense NSDI 2019","Respiration sensing failed at distance/through-wall","Single-AP home far-field need","Single-antenna noise + amplitude blind spots","Dual-antenna CSI ratio + amplitude-phase fusion","Completed - Real-time prototype","Reliable to 8m, through-wall","Heart rate, multitarget","High - range breakthrough","First through-wall respiration COTS"],
[26,"Wang et al. PhaseBeat MobiCom 2016","Contactless breathing/heart via cheap WiFi","Wearables/radar costly or inconvenient","Unstable phase offsets, weak heartbeat in multipath","Inter-antenna phase difference + DWT/FFT","Completed + journal ext.","0.25 bpm breath, 1.19 bpm heart median","Mobile, exercise, clinical validation","High - breathing; good heart","~400 Hz sampling used"],
[27,"Wang et al. TensorBeat IPSN 2016","Simultaneous multiperson breathing unsolved","Mixed chest reflections inseparable","Overlapping weak signals in time/freq/multipath","Phase-difference tensor + CP decomposition","Completed - multiperson tests","2-4 persons, beats FFT baselines","Scale count, motion, sleep monitoring","High - separation demo","30 subcarriers, antenna pairs"],
[28,"Kotaru et al. WiCapture MobiCom 2017","Fine VR tracking without cameras","Outside-in rigs cumbersome","Multipath AoD errors + Tx-Rx offset","Per-path AoD change tracking + offset compensation","Completed - vs Oculus truth","0.88cm trajectory (vs 132cm SpotFi)","Full 3D, controllers, outdoor","High - subcentimeter on APs","Office/occlusion/outdoor eval"],
[29,"Li et al. Wision NSDI 2014","Imaging with narrowband WiFi deemed infeasible","Can WiFi form camera-like images?","20 MHz + mixed multipath, no radar resolution","Multi-antenna 2D FFT angle imaging + beamforming","Completed - USRP N210 2.4GHz","26cm human, 15cm metal LOS/NLOS","Resolution, arrays, material ID","Medium - feasibility proof","1D/2D arrays, untagged targets"],
[30,"WiROS Toolbox 2023 arXiv:2305.13418","Robots lacked real-time CSI integration","Outdated offline/RSSI-only ROS tools","Phase errors, no calibrated ROS pipeline","ROS CSI node on Nexmon 802.11ac + calibration + AoA","Completed - Open source","Real-time topics, sub-500ms switching","AX platforms, SLAM benchmarks","High - research-to-robotics bridge","Asus RT-AC86U / RPi tested"],
[31,"Yousefi et al. 2017 Behavior Recognition IEEE Comm Mag","Device-free recognition without wearables","Vision/wearable limits in smart homes","Handcrafted features, multipath variability","Survey + LSTM on CSI amplitude statistics","Completed - Survey + tests","High on fall/daily testbed","Multi-user, real homes","Medium - early deep baseline","Tutorial-style, widely cited"],
[32,"Chen et al. 2018 Attention BLSTM TMC","Passive HAR from noisy CSI series","Healthcare contactless monitoring need","Equal time-step weighting obscures motion","Attention Bi-LSTM over informative frames","Completed - Peer reviewed","~95%, beats SVM/HMM/plain LSTM","Cross-subject, elderly real-time","High - interpretable sequences","A*STAR 6-activity set"],
[33,"Yang et al. SenseFi Patterns 2022 arXiv:2207.07859","No reproducible benchmark/zoo","Fragmented sets, inconsistent eval","Heterogeneous HW/preprocessing/models","Open library: data + preprocessing + baselines","Completed - Open benchmark","CNN/GRU/Transformer on UT-HAR/Widar/NTU-Fi","Multimodal, larger multi-env","High - reproducibility","PyTorch HAR/fall/gesture"],
[34,"Yang et al. AutoFi IoT-J 2022","Manual labeling + poor CSI block auto setup","Costly calibration in new envs","Scarce labels + noisy amplitude/phase","Geometric SSL pretrain + few-shot calibration","Completed - Published","Strong few-shot gesture/HAR","Multi-user multi-room auto deploy","High - label efficiency","SSL generalization core ref"],
[35,"Yang et al. EfficientFi IoT-J 2022 arXiv:2204.04138","CSI transmission/compute block large-scale edge","Cloud-edge bandwidth bottleneck","Raw CSI streaming overwhelms uplink","Quantized autoencoder at edge + joint classification","Completed - Prototype","High compression, near-original accuracy","Ultra-low-bit, on-device inference","High - efficiency-accuracy tradeoff","Joint codec + classifier"],
[36,"WiFlexFormer 2024 arXiv:2411.04224","Heavy models unsuitable for person-centric edge","Latency/param limits of Transformers","Generic archs ignore CSI time-freq structure","Compact Transformer + stem downsampling","Completed - Multi-dataset","Competitive accuracy, far fewer params","Cross-HW, through-wall real-time","High - efficient edge","Widar3.0/NTU-Fi/through-wall"],
[37,"MORIC Delay-Doppler 2025 arXiv:2506.12997","Poor cross-user/orientation generalization","Env/body Doppler distortion","Time-freq entanglement, user sensitivity","Delay-Doppler decomposition + motion encoding","Preprint - Ablated","Better cross-user, lower variance","802.11bf, live multi-AP","Medium-High - needs replication","Physics-inspired, interpretable"],
[38,"Physics-Guided Lightweight TCN 2026 arXiv:2606.01834","Accurate yet edge-efficient + interpretable HAR","Black-box heavy models ignore physics","Data-only TCN misses velocity priors","Lightweight TCN + Doppler attention","Preprint - Limited validation","High accuracy, tiny params, fast","Cross-env, HW implementation","Medium-High - provisional","Treat as provisional (2026)"],
[39,"Jiang et al. EI Adversarial MobiCom 2018","Env change collapses HAR accuracy","Env-dependent fingerprints","Train-test shift couples gesture + room","Adversarial env discriminator for invariant features","Completed - Conference","High in unseen rooms vs baselines","Multi-user, continuous, open-set","High - seminal invariance","CNN + adversarial, Widar-style"],
[40,"Zhang et al. CrossSense UbiComp 2019","Gesture models fail across sites","Costly per-site collection","Site multipath shifts distributions","Cross-site CSI translation + site-independent classifier","Completed - Multi-site","Large cross-site gain with virtual samples","Hetero devices, larger vocab","High - transfer foundation","100+ locations, SDR CSI"],
[41,"Data Augmentation Cross-Domain 2024 arXiv:2401.00964","Cross-domain HAR drops on unseen users/envs","Domain-shift failures","Limited diverse CSI, overfitting","Physics-informed augmentation + invariant features","Preprint - Validated","Improved cross-domain gesture","Larger envs, real-time","High - low-cost gain","Augmentation thesis baseline"],
[42,"Transformer Hetero Env 2022 arXiv:2209.11750","CSI fails across hetero layouts/devices","Env variability setup","Handcrafted miss time-freq deps","Transformer time-freq tokens","Published - Benchmarked","Higher robust HAR","Lightweight edge deploy","High but compute-heavy","Transformer direction support"],
[43,"Widar3.0 Public Dataset 2021","No large cross-domain gesture benchmark","Need public reproducible data","Small lab sets block generalization study","17 users, 3 rooms, DFS/BVP open corpus","Released - Widely cited","Enables cross-domain benchmarks","More actions/modalities","High - community resource","Core thesis eval set"],
[44,"WiMANS ECCV 2024 arXiv:2402.09430","No multi-user multi-activity benchmark","Crowded real scenes ignored","Single-person sets ignore interference","Synced video-CSI multi-user annotation","Published - Open","Multi-person HAR/localization support","More users, through-wall","High but complex","Multi-user tests"],
[45,"XRF55 RF Action Corpus 2024","Single-RF narrow action coverage","Modality gaps","Narrowband single setup, low diversity","55 actions multi-RF synced corpus","Released - Baselined","Action-recognition baselines","More envs, continuous","High - broad benchmark","Complements Widar/WiMANS"],
[46,"MM-Fi Multimodal 2023","Single modality fails occlusion/viewpoint","Robust HAR need","CSI alone lacks spatial context","WiFi+LiDAR+RGB+depth aligned + baselines","Released - Benchmarked","Multimodal beats unimodal","Real homes, continual learning","High - fusion demo","Multimodal chapter support"],
[47,"CSI-Bench NeurIPS 2025 arXiv:2505.21866","Small fragmented sets block foundation models","Scale gap vs vision/RF","Inconsistent HW formats block pretraining","461h, 35 users, 26 envs unified benchmark","Published - Large-scale","Pretraining boosts few-shot HAR","More tasks/devices","High - scaling proof","Key 2025 large benchmark"],
[48,"Sensors 2026 Baseline + ESP-Fi HAR 2026","Modern baselines missing cheap ESP32 validation","Low-cost HW eval gap","Old models untested on ESP32 noise","Systematic ML/DL + ESP-Fi prototype","Published 2026","Competitive low-cost results","Larger deployments, energy opt","High - reproducible baseline","Low-cost thesis claim"],
[49,"Du 802.11bf Overview COMST 2024 + 802.11bf-2025","No unified sensing standard survey","Need 802.11bf clarity","Proprietary sensing blocks interop","MAC/PHY sensing procedures review","Published + Standard Sept 2025","Interoperable sensing enabled","Channel access, multi-AP","High - normative impact","Standards foundation section"],
[50,"Path Diversity ISAC 2026 + MilaGro + NIST 2026","Sub-7GHz resolution vs coverage tradeoff","Diversity/multiband gap","Single band blockage/ambiguity","Multiband fusion testbed + NIST framework","Preprints 2025-26 emerging","Better robustness/accuracy","Standard-compliant ISAC trials","Medium-High - frontier","Future-work closer"],
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Paper Analysis"
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0

hdr_fill = PatternFill("solid", fgColor="1F4E78")
hdr_font = Font(bold=True, color="FFFFFF", size=10)
thin = Side(style="thin", color="B0B0B0")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")

widths = [7,26,28,24,26,26,14,26,24,24,26]
for i, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

ws.append(HEADERS)
for c in ws[1]:
    c.fill = hdr_fill; c.font = hdr_font; c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
ws.row_dimensions[1].height = 30
ws.freeze_panes = "B2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{len(ROWS)+1}"

for r in ROWS:
    ws.append(r)
for row in ws.iter_rows(min_row=2, max_row=len(ROWS)+1, max_col=len(HEADERS)):
    h = 52
    for c in row:
        c.alignment = wrap
        c.border = border
        c.font = Font(size=9)
        if c.column == 1:
            c.alignment = Alignment(horizontal="center", vertical="top")
            c.font = Font(size=9, bold=True)
    ws.row_dimensions[c.row].height = h

# Status sheet
ws2 = wb.create_sheet("Status Key")
ws2["A1"] = "Status values used in column G"
ws2["A1"].font = Font(bold=True, size=12)
for i, s in enumerate(["Completed - Published Survey/Tutorial/Review","Completed - Prototype Validated","Completed - Tool Released / Open Source","Completed - Benchmark Released","Preprint - Validated but limited peer review","Published Standard"], start=3):
    ws2.cell(row=i, column=1, value=s)
ws2.column_dimensions["A"].width = 55

# Cover sheet
ws0 = wb.create_sheet("Cover", 0)
ws0["A1"] = "Wi-Fi CSI Sensing - 50-Paper Analysis Report"
ws0["A1"].font = Font(bold=True, size=16, color="1F4E78")
ws0["A2"] = "Columns: Serial | Paper Name | Problem Description | Problem Statement Source | Root Cause | Corrective Actions | Status | Follow-up Results | Future Plans | Effectiveness | Notes"
ws0["A2"].font = Font(size=10, italic=True)
ws0["A3"] = "Built from 5 parallel batches (1-10, 11-20, 21-30, 31-40, 41-50). 2026 items flagged provisional where peer review pending."
ws0["A3"].font = Font(size=10)
ws0.column_dimensions["A"].width = 150
ws0.sheet_properties.tabColor = "1F4E78"

wb.save(OUT)
print(f"saved:{OUT} rows:{len(ROWS)}")
