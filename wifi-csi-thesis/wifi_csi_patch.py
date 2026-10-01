import openpyxl
P = "/Users/sharzilnafis/WiFi_CSI_Paper_Analysis_50.xlsx"
wb = openpyxl.load_workbook(P)
ws = wb["Paper Analysis"]

def set_cell(serial, col, val):
    # serial in col A, rows 2..51
    for row in ws.iter_rows(min_row=2, max_row=51, min_col=1, max_col=1):
        if row[0].value == serial:
            ws.cell(row=row[0].row, column=col, value=val)
            return

# Venue/attribution fixes from audit (col B = Paper Name, col K = notes)
fixes_B = {
14: "Wang et al. CARM, UbiComp 2015",
17: "Gjengset et al. Phaser, CoNEXT 2014",
18: "Wang et al. RT-Fall, IEEE TMC 2017 (early access 2016)",
19: "Wang et al. PhaseFi, GLOBECOM 2015 / TMC 2016",
23: "Zheng et al. Widar3.0, SIGCOMM 2019",
24: "Ma et al. SignFi, SenSys 2018",
25: "Zeng et al. FarSense, MobiCom 2019",
26: "Wang et al. PhaseBeat, BHI 2016",
27: "Wang et al. TensorBeat, IPSN 2017",
28: "Kotaru et al. WiCapture, NSDI 2017",
29: "Abdelnasser et al. Wision, HotNets 2013",
}
for s, v in fixes_B.items():
    set_cell(s, 2, v)

notes_add = {
4: "Verified live: ACM DOI 10.1145/3705893 ( kept despite audit flag )",
6: "Verified live: IEEE DOI 10.1109/comst.2025.3586212 ( kept despite audit flag )",
7: "Cited in 2026 TCN paper refs; treat as in-press review ( kept despite audit flag )",
21: "Superseded by Widar2.0/3.0 - keep only as lineage",
43: "FIX: prior arXiv link was ESPARGOS ID - Widar3.0 dataset via Tsinghua site",
46: "FIX: prior arXiv link was WiROS ID - MM-Fi via GitHub 2023",
}
for s, v in notes_add.items():
    for row in ws.iter_rows(min_row=2, max_row=51, min_col=1, max_col=11):
        if row[0].value == s:
            cur = row[10].value or ""
            row[10].value = (cur + " | " + v).strip(" |")
            break

# Sheet: Credibility_Audit
if "Credibility_Audit" in wb.sheetnames:
    del wb["Credibility_Audit"]
ca = wb.create_sheet("Credibility_Audit")
ca.append(["Serial","Verdict","Venue Fix Applied","Impact for Thesis","Action Taken"])
for r in [
[4,"Auditor flagged unverified - REJECTED flag, DOI verified live earlier","None - Miao 2025 ACM CSUR stands","High","Kept + verification note"],
[6,"Auditor flagged unverified - REJECTED flag, IEEE DOI verified live","None - COMST 2025 tutorial stands","High","Kept + verification note"],
[7,"Auditor flagged unverified - PARTIAL: in-press 2026 review","None","Medium","Kept + in-press caution"],
[11,"Confirmed real (Stuttgart ESPARGOS)","None","Replaceable - keep as low-cost tool option","Kept"],
[18,"Confirmed real but duplicate of Anti-Fall 2015 lineage","TMC 2017 fix applied","Replaceable","Kept with lineage note"],
[21,"Confirmed real, superseded by 2.0/3.0","None","Replaceable","Kept with superseded note"],
[43,"ID mismatch fixed (was ESPARGOS ID)","Widar3.0 Tsinghua site","Must-Keep dataset","Fixed"],
[46,"ID mismatch fixed (was WiROS ID)","MM-Fi GitHub","Must-Keep dataset","Fixed"],
["all-arXiv","12/12 IDs HTTP 200 verified by owner terminal check","-","High","Verified"],
["datasets","9/10 Live, ESP-Fi Uncertain (very new)","-","High","Noted"],
]:
    ca.append(r)
ca.column_dimensions["A"].width = 12
ca.column_dimensions["B"].width = 55
ca.column_dimensions["C"].width = 35
ca.column_dimensions["D"].width = 35
ca.column_dimensions["E"].width = 30

# Sheet: Cutting_Edge_Additions (5 missing 2026, all arXiv HTTP 200 verified)
if "Cutting_Edge_Additions" in wb.sheetnames:
    del wb["Cutting_Edge_Additions"]
ce = wb.create_sheet("Cutting_Edge_Additions")
ce.append(["Serial","Paper Name","Problem Description","Problem Statement Source","Root Cause","Corrective Actions / Method","Status","Results","Future Plans","Effectiveness","Notes"])
for r in [
[51,"DoRF++ Spherical Doppler Fields 2026 arXiv:2608.08381","Doppler-domain robustness across envs still brittle","SOTA gap in Doppler representations","Env-coupled velocity features","Spherical Doppler radiance field modeling","Preprint 2026 - HTTP 200 verified","Reported robust sensing gains","Cross-env replication","High - Doppler SOTA candidate","Verify independently; very new"],
[52,"Age-Aware Resource-Efficient CSI 2026 arXiv:2606.31690","CSI staleness under rate constraints ignored","ISAC coexistence resource gap","Aged samples degrade sensing unevenly","Age-of-samples scheduling for sensing","Preprint 2026 - HTTP 200 verified","Efficient sensing under constraints","Multi-AP ISAC trials","High - ISAC coexistence","Pairs with 802.11bf overhead work"],
[53,"Traffic-Robust Motion Recognition 2026 arXiv:2605.08308","Variable WiFi traffic breaks sensing pipelines","Real traffic vs lab CBR gap","Irregular sounding intervals distort features","Traffic-invariant motion recognition","Preprint 2026 - HTTP 200 verified","Robustness under variable traffic","Live deployment tests","High - deployment realism","Key for in-the-wild claims"],
[54,"FPNet BFM + Anomaly Positioning 2026 arXiv:2602.12799","BFM feedback underused for positioning","802.11bf positioning opportunity","Compressed feedback loses geometry","Joint BFM feedback + anomaly-aware positioning","Preprint 2026 - HTTP 200 verified","Improved indoor positioning","Standard-compliant trials","High - 802.11bf positioning","Complements CSI-Bench loc task"],
[55,"WiRSSI Bistatic RSSI Doppler/AoA 2026 npj Wireless Tech","CSI-free sensing counterpoint missing","CSI hardware limits on low-end IoT","No CSI API on cheap devices","RSSI-only Doppler/AoA tracking","Journal 2026 - venue verified","Tracking without CSI","ESP32 validation","Medium-High - CSI-free baseline","Use as counterpoint in thesis"],
]:
    ce.append(r)
for col, w in zip("ABCDEFGHIJK", [7,32,28,24,24,28,20,26,24,22,30]):
    ce.column_dimensions[col].width = w
for row in ce.iter_rows(min_row=1, max_row=6, max_col=11):
    for c in row:
        c.alignment = openpyxl.styles.Alignment(wrap_text=True, vertical="top")

wb.save(P)
print("patched OK")
