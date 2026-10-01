import openpyxl, urllib.parse
P = "/Users/sharzilnafis/WiFi_CSI_Paper_Analysis_50.xlsx"
wb = openpyxl.load_workbook(P)
ws = wb["Paper Analysis"]

def scholar(title):
    return "https://scholar.google.com/scholar?q=" + urllib.parse.quote_plus(title)

AR = lambda i: f"https://arxiv.org/abs/{i}"
LINKS = {
1: scholar("WiFi Sensing with Channel State Information: A Survey Ma 2019 ACM Computing Surveys"),
2: scholar("Wireless Sensing for Human Activity: A Survey Liu 2019 IEEE Communications Surveys"),
3: scholar("Cross-Domain WiFi Sensing with Channel State Information: A Survey Chen 2023"),
4: "https://dl.acm.org/doi/10.1145/3705893",
5: AR("2503.08008"),
6: "https://doi.org/10.1109/comst.2025.3586212",
7: scholar("Machine Learning Techniques for Wi-Fi CSI-based Recognition and Sensing Sai 2026 IEEE IoT"),
8: "https://github.com/dhalperi/linux-80211n-csitool",
9: "https://github.com/seemoo-lab/nexmon_csi",
10: "https://github.com/wifisensing/PicoScenes",
11: AR("2408.16377"),
12: scholar("See Through Walls with WiFi Adib Katabi SIGCOMM 2013"),
13: scholar("E-eyes device-free location-oriented activity identification MobiCom 2014"),
14: scholar("CARM CSI-based human Activity Recognition and Monitoring UbiComp 2015"),
15: "https://dl.acm.org/doi/10.1145/2785956.2787487",
16: scholar("ArrayTrack fine-grained indoor location Xiong Jamieson NSDI 2013"),
17: scholar("Phaser enabling phased array signal processing commodity wifi Gjengset CoNEXT 2014"),
18: scholar("RT-Fall real-time contactless fall detection commodity WiFi TMC 2017"),
19: scholar("PhaseFi phase fingerprinting indoor localization deep learning GLOBECOM 2015"),
20: scholar("Chronos single-antenna ToF localization Vasisht NSDI 2016"),
21: scholar("Widar decimeter tracking Qian MobiCom 2017"),
22: scholar("Widar2.0 multi-person tracking Qian MobiCom 2018"),
23: scholar("Widar3.0 zero-effort cross-domain gesture recognition Zheng SIGCOMM 2019"),
24: scholar("SignFi sign language CSI CNN Ma SenSys 2018"),
25: AR("1907.03994"),
26: scholar("PhaseBeat breathing heartbeat Wang BHI 2016"),
27: scholar("TensorBeat multi-person breathing Wang IPSN 2017"),
28: scholar("WiCapture VR tracking commodity WiFi Kotaru NSDI 2017"),
29: scholar("Wision imaging Abdelnasser HotNets 2013"),
30: AR("2305.13418"),
31: scholar("Behavior Recognition Using WiFi CSI Yousefi IEEE Communications Magazine 2017"),
32: scholar("WiFi CSI passive HAR attention BLSTM Chen TMC 2018"),
33: AR("2207.07859"),
34: scholar("AutoFi automatic WiFi sensing geometric self-supervised Yang IoT-J 2022"),
35: AR("2204.04138"),
36: AR("2411.04224"),
37: AR("2506.12997"),
38: AR("2606.01834"),
39: scholar("EI adversarial environment-independent activity recognition Jiang MobiCom 2018"),
40: scholar("CrossSense roaming models Zhang UbiComp 2019"),
41: AR("2401.00964"),
42: AR("2209.11750"),
43: "https://tns.thss.tsinghua.edu.cn/widar3.0/",
44: AR("2402.09430"),
45: scholar("XRF55 RF action corpus 2024"),
46: scholar("MM-Fi multimodal WiFi LiDAR RGB 2023"),
47: AR("2505.21866"),
48: scholar("ESP-Fi HAR low-power WiFi CSI Ad Hoc Networks 2026"),
49: AR("2310.17661"),
50: AR("2601.12980"),
}
# Header col L
from copy import copy
HDR_FILL = copy(ws["A1"].fill); HDR_FONT = copy(ws["A1"].font)
HDR_AL = copy(ws["A1"].alignment); HDR_BD = copy(ws["A1"].border)
ws.cell(row=1, column=12, value="Link").fill = HDR_FILL
ws.cell(row=1, column=12).font = HDR_FONT
ws.cell(row=1, column=12).alignment = HDR_AL
ws.cell(row=1, column=12).border = HDR_BD
ws.column_dimensions["L"].width = 42
for row in ws.iter_rows(min_row=2, max_row=51, min_col=1, max_col=1):
    s = row[0].value
    url = LINKS.get(s, "")
    c = ws.cell(row=row[0].row, column=12, value=url)
    c.hyperlink = url
    c.style = "Hyperlink"
    c.alignment = openpyxl.styles.Alignment(wrap_text=True, vertical="top")
    c.border = copy(ws.cell(row=row[0].row, column=11).border)
ws.auto_filter.ref = f"A1:L{ws.max_row}"

# Links for Cutting_Edge_Additions too (col L)
ce = wb["Cutting_Edge_Additions"]
if ce.max_column < 12:
    ce.cell(row=1, column=12, value="Link")
    ce.column_dimensions["L"].width = 42
CE_LINKS = {51: AR("2608.08381"), 52: AR("2606.31690"), 53: AR("2605.08308"), 54: AR("2602.12799"),
            55: scholar("WiRSSI bistatic RSSI-only Doppler AoA tracking npj Wireless 2026")}
for row in ce.iter_rows(min_row=2, max_col=1):
    s = row[0].value
    url = CE_LINKS.get(s, "")
    c = ce.cell(row=row[0].row, column=12, value=url)
    if url:
        c.hyperlink = url
        c.style = "Hyperlink"

wb.save(P)
print("links added")
