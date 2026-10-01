import openpyxl, sys
sys.path.insert(0, "/Users/sharzilnafis/Projects/wifi-csi-thesis")
from data_expanded_1 import BATCH1
from data_expanded_2 import BATCH2
from data_expanded_3 import BATCH3
from data_expanded_4 import BATCH4
from copy import copy

OLD = "/Users/sharzilnafis/Projects/wifi-csi-thesis/WiFi_CSI_Paper_Analysis_50.xlsx"
OUT = "/Users/sharzilnafis/Projects/wifi-csi-thesis/WiFi_CSI_Research_Report_55.xlsx"
old = openpyxl.load_workbook(OLD)
ws_old = old["Paper Analysis"]
ce_old = old["Cutting_Edge_Additions"]
old_names = {}
old_links = {}
for r in ws_old.iter_rows(min_row=2, values_only=True):
    if r[0]:
        old_names[r[0]] = r[1]
        old_links[r[0]] = r[11] if len(r) > 11 else ""
ce_links = {}
for r in ce_old.iter_rows(min_row=2, values_only=True):
    if r and r[0]:
        ce_links[r[0]] = r[11] if len(r) > 11 else ""

ANCHOR = {1:"Ma et al., 2019, ACM Computing Surveys",2:"Liu et al., 2019, IEEE COMST",3:"Chen et al., 2023, ACM Computing Surveys",4:"Miao et al., 2025, ACM Computing Surveys",5:"Wang et al., 2025, IEEE COMST (arXiv:2503.08008)",6:"SSL Tutorial, 2025, IEEE COMST",7:"Sai et al., 2026, IEEE IoT-J",8:"Halperin et al., 2011, ACM CCR (tool)",9:"Nexmon team, 2017-2019, open firmware",10:"PicoScenes team, 2020-2022, open platform",11:"ESPARGOS team, 2024, arXiv:2408.16377",12:"Adib & Katabi, 2013, ACM SIGCOMM",13:"Wang et al. (E-eyes), 2014, ACM MobiCom",14:"Wang et al. (CARM), 2015, ACM UbiComp",15:"Kotaru et al., 2015, ACM SIGCOMM",16:"Xiong & Jamieson, 2013, USENIX NSDI",17:"Gjengset et al., 2014, ACM CoNEXT",18:"Wang et al. (RT-Fall), 2017, IEEE TMC",19:"Wang et al. (PhaseFi), 2015-16, GLOBECOM/TMC",20:"Vasisht et al., 2016, USENIX NSDI",21:"Qian et al. (Widar), 2017, ACM MobiCom",22:"Qian et al. (Widar2.0), 2018, ACM MobiCom",23:"Zheng et al. (Widar3.0), 2019, ACM MobiSys",24:"Ma et al. (SignFi), 2018, ACM SenSys",25:"Zeng et al. (FarSense), 2019, ACM MobiCom",26:"Wang et al. (PhaseBeat), 2016, IEEE BHI",27:"Wang et al. (TensorBeat), 2017, ACM IPSN",28:"Kotaru et al. (WiCapture), 2017, USENIX NSDI",29:"Abdelnasser et al. (Wision), 2013, ACM HotNets",30:"WiROS team, 2023, arXiv:2305.13418",31:"Yousefi et al., 2017, IEEE Comm. Magazine",32:"Chen et al., 2018, IEEE TMC",33:"Yang et al. (SenseFi), 2022, Patterns (arXiv:2207.07859)",34:"Yang et al. (AutoFi), 2022, IEEE IoT-J",35:"Yang et al. (EfficientFi), 2022, IEEE IoT-J",36:"WiFlexFormer, 2024, arXiv:2411.04224",37:"MORIC, 2025, arXiv:2506.12997",38:"Physics-TCN, 2026, arXiv:2606.01834 (preprint)",39:"Jiang et al. (EI), 2018, ACM MobiCom",40:"Zhang et al. (CrossSense), 2019, ACM UbiComp",41:"Augmentation study, 2024, arXiv:2401.00964",42:"Hetero Transformer, 2022, arXiv:2209.11750",43:"Widar3.0 dataset, 2021, Tsinghua release",44:"WiMANS, 2024, ECCV (arXiv:2402.09430)",45:"XRF55, 2024, multi-RF corpus",46:"MM-Fi, 2023, multimodal benchmark",47:"CSI-Bench, 2025, NeurIPS (arXiv:2505.21866)",48:"ESP-Fi HAR + Sensors baseline, 2026",49:"Du et al. + IEEE 802.11bf-2025 standard",50:"ISAC primer + MilaGro, 2025-26",51:"DoRF++, 2026, arXiv:2608.08381 (preprint)",52:"Age-aware sensing, 2026, arXiv:2606.31690 (preprint)",53:"Traffic-robust, 2026, arXiv:2605.08308 (preprint)",54:"FPNet, 2026, arXiv:2602.12799 (preprint)",55:"WiRSSI, 2026, npj Wireless Technology"}
HW = {1:"Survey only",2:"Survey only",3:"Survey only",4:"Survey only",5:"Survey only",6:"Survey/tutorial + code tips",7:"Review only",8:"Intel 5300 NIC, 30 subcarriers",9:"Broadcom phones/RPi, 80 MHz",10:"Intel/Qualcomm multi-node, 20-160 MHz",11:"8-ch ESPARGOS array",12:"USRP wideband prototype",13:"Intel 5300, single link",14:"Intel 5300, multi-room",15:"Intel 5300, 1-2 APs",16:"WARP many-antenna AP",17:"Atheros cards, shared clock",18:"Intel 5300, home trials",19:"Intel 5300, fingerprint map",20:"Commodity cards, band hopping",21:"Intel 5300, classrooms",22:"Intel 5300, multi-room",23:"Intel 5300 + Atheros, 3 envs",24:"Intel 5300, 276 signs",25:"Intel 5300, long rooms",26:"Intel 5300 + wearables truth",27:"Intel 5300, 2-5 people",28:"Intel 5300 + motion capture",29:"USRP N210 2.4 GHz",30:"Asus RT-AC86U/RPi + ROS",31:"Survey only",32:"A*STAR 6-activity set",33:"UT-HAR/Widar/NTU-Fi + code",34:"Few-shot CSI sets",35:"Edge-cloud prototype",36:"Widar3.0/NTU-Fi/through-wall",37:"Masked CSI benchmarks",38:"TCN benchmarks (provisional)",39:"Widar-style CSI + adversarial",40:"SDR CSI, 100+ locations",41:"Public gesture/activity sets + code",42:"Mixed-device CSI sets",43:"Widar3.0 open corpus",44:"WiMANS open multi-person set",45:"XRF55 open multi-RF set",46:"MM-Fi open multimodal set",47:"CSI-Bench open (pin Kaggle v12)",48:"ESP32 links + RPi gateway",49:"Standard docs + overview paper",50:"mmWave + sub-7 GHz testbed",51:"Widar3.0/XRF55/MM-Fi scripts",52:"Age-stratified CSI (pending release)",53:"Traffic-controlled testbed scripts",54:"Multi-day fingerprint sets + code",55:"Multi-link RSSI home captures + code"}
REL = {1:"Ch2 definitions + pre-2019 gap",2:"Ch2 radio choice justification",3:"Ch2 domain-shift framing",4:"Ch2 HAR datasets + baselines",5:"Ch2 robustness test plan",6:"Ch3 SSL method justification",7:"Ch2 model selection",8:"Ch3 Intel data provenance",9:"Ch3 phone/RPi collection",10:"Ch3 multi-node capture rigor",11:"Ch4 array/angle extension",12:"Ch1 motivation (through-wall)",13:"Ch2 home-activity baseline",14:"Ch3 Doppler feature justification",15:"Ch2 localization baseline",16:"Ch2 antenna-scaling history",17:"Ch3 phase calibration background",18:"Ch2 fall-detection baseline",19:"Ch2 phase-fingerprint baseline",20:"Ch2 bandwidth-limit discussion",21:"Ch2 tracking lineage (1 line)",22:"Ch2 cross-room tracking baseline",23:"Ch4 main gesture baseline + data",24:"Ch4 sign baseline + data",25:"Ch3 CSI-ratio justification",26:"Ch2 vital-sign pipeline",27:"Ch4 multi-person vitals framing",28:"Ch4 fine-tracking accuracy bar",29:"Ch1 motivation (imaging dream)",30:"Ch3 collection platform",31:"Ch2 review + gap picking",32:"Ch4 classic deep baseline",33:"Ch4 fair-benchmark protocol",34:"Ch3 few-shot/label-saving method",35:"Ch5 edge-efficiency story",36:"Ch4 multi-device backbone",37:"Ch4 robustness chapter",38:"Ch4 novelty + cross-room claim",39:"Ch4 domain-invariance baseline",40:"Ch4 transfer-learning chapter",41:"Ch4 augmentation ablations",42:"Ch4 mixed-device design",43:"Ch4 cross-domain eval data",44:"Ch5 multi-person eval data",45:"Ch5 fusion eval data",46:"Ch5 multimodal eval data",47:"Ch4/5 main benchmark + pretraining",48:"Ch5 low-cost validation",49:"Ch2 standards section",50:"Ch6 future work (ISAC/multiband)",51:"Ch4 Doppler-feature baseline",52:"Ch5 fairness/safety discussion",53:"Ch4 traffic-robustness tests",54:"Ch4 localization maintenance",55:"Ch2 RSSI lower-bound baseline"}

ALL = BATCH1 + BATCH2 + BATCH3 + BATCH4
assert len(ALL) == 55, len(ALL)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Paper Analysis"
HEAD = ["Serial","Paper Title","Authors-Year-Venue","Problem Addressed","Why Hard","What They Did","Key Results","Status","Effectiveness for Thesis","Future Work","Dataset-Hardware","Relevance to Thesis","Link"]
ws.append(HEAD)
for (s, prob, hard, did, res, status, eff, fut) in ALL:
    link = old_links.get(s, "") or ce_links.get(s, "")
    ws.append([s, old_names.get(s, ANCHOR.get(s, "")), ANCHOR.get(s, ""), prob, hard, did, res, status, eff, fut, HW.get(s, ""), REL.get(s, ""), link])

from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
hdr_fill = PatternFill("solid", fgColor="1F4E78"); hdr_font = Font(bold=True, color="FFFFFF", size=10)
thin = Side(style="thin", color="B0B0B0"); bd = Border(left=thin, right=thin, top=thin, bottom=thin)
widths = [7,30,26,44,36,44,40,16,40,34,24,28,30]
from openpyxl.utils import get_column_letter
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w
for c in ws[1]:
    c.fill = copy(hdr_fill); c.font = copy(hdr_font)
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = copy(bd)
ws.row_dimensions[1].height = 32
ws.freeze_panes = "C2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(HEAD))}{ws.max_row}"
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_setup.orientation = "landscape"; ws.page_setup.paperSize = ws.PAPERSIZE_A3
ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
ws.print_title_rows = "1:1"
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=len(HEAD)):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = copy(bd); c.font = Font(size=9)
        if c.column == 13 and c.value:
            c.hyperlink = c.value; c.style = "Hyperlink"
    ws.row_dimensions[row[0].row].height = 150

# Cover
cv = wb.create_sheet("Cover", 0)
cv["A1"] = "Wi-Fi CSI Sensing - Research Report (55 papers, expanded plain-language edition)"
cv["A1"].font = Font(bold=True, size=15, color="1F4E78")
cv["A2"] = "Main sheet: 12 content columns + Link. Start at Cover, then How to Use, then Paper Analysis rows 1-55 in order."
cv["A3"] = "Corrections applied: Widar3.0 = MobiSys 2019 (DOI 10.1145/3307334.3326081); CARM = UbiComp 2015; Phaser = CoNEXT 2014; RT-Fall = TMC 2017; PhaseFi = GLOBECOM 2015; SignFi = SenSys 2018; FarSense = MobiCom 2019; PhaseBeat = BHI 2016; TensorBeat = IPSN 2017; WiCapture = NSDI 2017; Wision = HotNets 2013."
cv["A4"] = "2026 preprints (38, 51-54) flagged provisional - re-verify before citing as established fact. CSI-Bench: pin Kaggle v12."
for r in range(1, 5):
    cv.row_dimensions[r].height = 28 if r == 1 else 40
cv.column_dimensions["A"].width = 170

hu = wb.create_sheet("How to Use", 1)
hu.append(["Step","What to do","Rows to read"])
for r in [[1,"Learn basics: surveys + tools","1-11"],[2,"Pick baselines: localization/HAR/gesture","12-25"],[3,"Pick method: deep/efficient/transfer","31-42"],[4,"Pick data: benchmarks","33, 43-48"],[5,"Write future work: 802.11bf/ISAC/2026","47-55"],[6,"Build plan: Cover -> proposal (ask agent)","-"]]:
    hu.append(r)
hu.column_dimensions["A"].width = 8; hu.column_dimensions["B"].width = 60; hu.column_dimensions["C"].width = 30

ca = wb.create_sheet("Credibility_Audit")
ca.append(["Check","Result","Action"])
for r in [["Widar3.0 venue","MobiSys 2019 confirmed via ACM DOI 10.1145/3307334.3326081 (479 cites)","Reverted wrong SIGCOMM label"],
["16 arXiv IDs","All HTTP 200 (12 prior + 4 new 2026)","Verified by terminal"],
["Miao 2025 / SSL tutorial / Sai 2026","DOI/IEEE live pages found; Sai DOI 10.1109/JIOT.2026.3657341","Kept with verification notes"],
["Datasets","9/10 live; ESP-Fi uncertain (very new)","Caution noted in row 48"],
["Preprints","Rows 37, 38, 51-54 provisional","Flagged on Cover"]]:
    ca.append(r)
ca.column_dimensions["A"].width = 24; ca.column_dimensions["B"].width = 80; ca.column_dimensions["C"].width = 40

wb.save(OUT)
print("saved", OUT, "rows:", ws.max_row - 1)
