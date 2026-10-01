#!/usr/bin/env python3
"""Build thesis_dashboard.html (self-contained, stdlib only)."""
import json
import html
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def norm(s):
    return "".join(c.lower() for c in s if c.isalnum())


def trim(s, n=600):
    s = (s or "").strip().replace("\n", " ")
    return s[:n] + ("..." if len(s) > n else "")


def main():
    papers = load("papers.json")
    corpus = load("corpus_summary.json")
    ledger = load("evidence_ledger.json")
    gaps = load("gaps.json")
    bench = load("benchmark_provenance_manifest.json")
    sim = load("simulated_split_evaluation_results.json")
    hw = load("hardware_capability_matrix.json")
    edge = load("tinyml_edge_profiling_results.json")

    # bibtex_key -> paper title / id
    key_to_title, key_to_id = {}, {}
    for pid, p in papers.items():
        k = p.get("bibtex_key", "")
        if k and k not in key_to_title:
            key_to_title[k] = p.get("title", k)
            key_to_id[k] = pid

    # corpus notes keyed by normalized title for why-it-matters lookup
    notes = {}
    for c in corpus:
        n = c.get("expanded_notes") or {}
        why = " ".join(x for x in [n.get("did", ""), n.get("results", "")] if x).strip()
        if not why:
            why = (n.get("problem", "") or "").strip()
        notes[norm(c.get("title", ""))] = {
            "why": trim(why, 500),
            "problem": trim(n.get("problem", ""), 400),
            "category": c.get("category", ""),
            "pages": c.get("pages", ""),
            "filename": c.get("filename", ""),
        }

    # slim papers for embedding
    slim = []
    for pid, p in papers.items():
        m = notes.get(norm(p.get("title", "")), {})
        slim.append({
            "id": pid, "title": p.get("title", ""), "year": p.get("year", ""),
            "venue": p.get("venue", ""), "bib": p.get("bibtex_key", ""),
            "pdf": bool(p.get("pdf_path")), "status": p.get("screening_status", ""),
            "abstract": trim(p.get("abstract", ""), 1200),
            "why": m.get("why", ""), "cat": p.get("category", "") or m.get("category", ""),
        })

    # slim ledger
    lev = ledger.values() if isinstance(ledger, dict) else ledger
    slim_ledger = [{
        "id": v.get("evidence_id", i), "claim": v.get("claim", ""),
        "bib": v.get("bibtex_key", ""),
        "src": key_to_title.get(v.get("bibtex_key", ""), v.get("bibtex_key", "")),
        "page": v.get("page_number", ""), "quote": trim(v.get("exact_passage", ""), 600),
    } for i, v in enumerate(lev)]

    # slim gaps
    slim_gaps = [{
        "id": g.get("gap_id", i), "naive": g.get("naive_claim", ""),
        "verdict": g.get("audit_verdict", ""),
        "fix": g.get("scientific_replacement", ""),
        "check": g.get("validation_requirement", ""),
        "bibs": g.get("cross_referenced_bib_keys", []) or [],
    } for i, g in enumerate(gaps)]

    # 8 anchors: top ledger keys by count -> paper ids, fill with surveys
    cnt = Counter(v.get("bibtex_key", "") for v in (ledger.values() if isinstance(ledger, dict) else ledger))
    anchors = []
    for k, _ in cnt.most_common():
        if k in key_to_id and key_to_id[k] not in anchors:
            anchors.append(key_to_id[k])
        if len(anchors) == 8:
            break
    if len(anchors) < 8:
        for pid, p in papers.items():
            if pid not in anchors and ("survey" in (p.get("venue", "") + p.get("title", "")).lower()
                                       or p.get("category", "") == "Survey"):
                anchors.append(pid)
            if len(anchors) == 8:
                break
    if len(anchors) < 8:
        for pid in papers:
            if pid not in anchors:
                anchors.append(pid)
            if len(anchors) == 8:
                break
    anchor_reasons = {pid: ("most-cited in Key Facts" if papers[pid].get("bibtex_key") in [k for k, _ in cnt.most_common(8)] else "foundational survey / starting point") for pid in anchors}

    data_js = ("const PAPERS=" + json.dumps(slim, ensure_ascii=False)
               + ";\nconst LEDGER=" + json.dumps(slim_ledger, ensure_ascii=False)
               + ";\nconst GAPS=" + json.dumps(slim_gaps, ensure_ascii=False)
               + ";\nconst BENCH=" + json.dumps(bench, ensure_ascii=False)
               + ";\nconst SIM=" + json.dumps(sim, ensure_ascii=False)
               + ";\nconst HW=" + json.dumps(hw, ensure_ascii=False)
               + ";\nconst EDGE=" + json.dumps(edge, ensure_ascii=False)
               + ";\nconst ANCHORS=" + json.dumps([{"id": a, "reason": anchor_reasons[a]} for a in anchors], ensure_ascii=False) + ";")

    np, nc, nl, ng = len(papers), len(corpus), len(slim_ledger), len(slim_gaps)

    h = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Thesis Dashboard — WiFi Sensing</title>
<style>
:root{--bg:#f6f7fb;--card:#fff;--ink:#1a2333;--muted:#5b6b82;--line:#e5e9f2;--accent:#2563eb;--accent-d:#1d4ed8;--ok:#16a34a;--ok-bg:#dcfce7;--bad:#dc2626;--bad-bg:#fee2e2;--warn-bg:#fef9c3;--warn-bd:#ca8a04;--rad:14px;--sh:0 1px 2px rgba(16,24,40,.06),0 4px 16px rgba(16,24,40,.07)}
*{box-sizing:border-box}body{font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;max-width:1140px;margin:0 auto;padding:0 20px 64px;color:var(--ink);background:var(--bg);line-height:1.6;font-size:16px}
h1{font-size:2rem;letter-spacing:-.02em;margin:28px 0 8px}h2{font-size:1.35rem;letter-spacing:-.01em;margin:40px 0 12px;padding-top:8px;border-top:1px solid var(--line);padding-top:20px}h3{font-size:1.05rem;margin:22px 0 8px}
p,li{color:#2a3650}nav{position:sticky;top:0;z-index:50;background:rgba(17,24,39,.86);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);margin:0 -20px;padding:12px 20px;display:flex;flex-wrap:wrap;gap:4px 16px;box-shadow:0 2px 12px rgba(0,0,0,.18)}
nav a{color:#e5e7eb;text-decoration:none;font-size:14px;font-weight:600;padding:4px 2px;border-bottom:2px solid transparent}nav a:hover{color:#fff;border-bottom-color:var(--accent)}
.counts{background:linear-gradient(135deg,#1e3a8a,#2563eb);color:#fff;padding:12px 18px;border-radius:var(--rad);font-weight:600;margin-top:16px;box-shadow:var(--sh)}
.warn{background:#fffbeb;border:1.5px solid var(--warn-bd);border-left-width:6px;padding:14px 16px;border-radius:10px;margin:16px 0}
#factCards,#gapCards{display:grid;grid-template-columns:1fr;gap:12px}@media(min-width:820px){#factCards,#gapCards{grid-template-columns:1fr 1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:14px 16px;margin:0;box-shadow:var(--sh);transition:transform .12s ease,box-shadow .12s ease,border-color .12s ease}
div.card:hover,label.card:hover{transform:translateY(-1px);box-shadow:0 2px 4px rgba(16,24,40,.08),0 10px 24px rgba(16,24,40,.1);border-color:#c7d2fe}
.card.hl{border:2px solid var(--bad);background:#fff7f7;box-shadow:0 0 0 3px rgba(220,38,38,.15)}
.claim{font-size:1.02rem;font-weight:650;line-height:1.45}
.myth{border-left:4px solid #c00;background:#fff5f5;padding:8px 10px;border-radius:0 8px 8px 0;font-weight:600}
.fix{border-left:4px solid #0a0;background:#f5fff5;padding:8px 10px;border-radius:0 8px 8px 0;margin-top:8px}
.gapbadge{display:inline-block;font-size:12px;font-weight:700;background:#333;color:#fff;padding:2px 8px;border-radius:10px;margin-bottom:6px}
.badge{display:inline-block;font-size:11.5px;font-weight:700;letter-spacing:.04em;padding:2px 10px;border-radius:999px;margin:2px;text-transform:uppercase}
.real{background:var(--ok-bg);color:#166534;border:1px solid #86efac}.sim{background:var(--bad-bg);color:#991b1b;border:1px solid #fca5a5}.est{background:var(--warn-bg);color:#854d0e;border:1px solid #fde047}
table{width:100%;border-collapse:separate;border-spacing:0;font-size:14px;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:var(--sh)}
thead th{position:sticky;top:52px;background:#111827;color:#f9fafb;text-align:left;padding:10px 12px;font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;z-index:5}
tbody td{border-top:1px solid var(--line);padding:9px 12px;vertical-align:top}
tbody tr:nth-child(even) td{background:#f8fafc}tbody tr:hover td{background:#eff6ff}tr.hl td{background:#fef2f2}
input[type=text]{width:100%;padding:10px 14px;margin:8px 0 14px;box-sizing:border-box;border:1.5px solid var(--line);border-radius:10px;font-size:15px;background:#fff}input[type=text]:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px rgba(37,99,235,.18)}
.detail{display:none;margin-top:8px;font-size:14px;color:#334155;background:#f8fafc;border-radius:8px;padding:10px 12px}.open .detail{display:block}
.gloss{background:var(--card);border:1px solid var(--line);padding:14px 18px;border-radius:var(--rad);box-shadow:var(--sh)}
.gloss dt{font-weight:700;color:#111827}.gloss dd{margin:0 0 8px 0;color:var(--muted)}
#planBox{display:grid;gap:10px}label.card{cursor:pointer;display:block}label.card input{margin-right:8px;accent-color:var(--accent);width:16px;height:16px}
#prog{font-weight:700;margin-top:10px;color:var(--accent-d)}
a{color:var(--accent)}a:hover{color:var(--accent-d)}
#benchBox ul{display:grid;gap:6px;padding-left:20px}ol li{margin-bottom:6px}
</style></head><body>
<nav><a href="#start">Start Here</a><a href="#papers">Papers</a><a href="#facts">Key Facts</a>
<a href="#gaps">Gaps To Avoid</a><a href="#data">Datasets &amp; Hardware</a><a href="#plan">Reading Plan</a></nav>
<div class="counts">COUNTS — papers: __COUNT_PAPERS__ papers &middot; summaries: __COUNT_CORPUS__ &middot; facts: __COUNT_LEDGER__ &middot; gaps: __COUNT_GAPS__</div>
<h1 id="start">WiFi Sensing Thesis Dashboard</h1>
<h2>Start Here — the thesis question in 3 sentences</h2>
<p><b>1.</b> Everyday WiFi signals bounce off people, so they can sense movement and breathing without wearables
(wearables means devices you must wear on your body). <b>2.</b> The hard part is that accuracy drops in a new room,
with a new person, or on new hardware, because the signal patterns change. <b>3.</b> This thesis asks which training
and testing methods make WiFi sensing honestly reliable across unseen people, rooms, and devices.</p>
<h3>5-step reading order</h3>
<ol><li>Read one survey anchor below to learn the pipeline (pipeline means the steps from signal to result).</li>
<li>Skim the Papers table; open 2–3 abstracts in your topic area.</li>
<li>Read the 23 Key Facts cards — these are the only claims safe to cite.</li>
<li>Read the gaps so you do not repeat debunked claims.</li>
<li>Check Datasets &amp; Hardware before any experiment; note what is simulated.</li></ol>
<div class="gloss"><h3>Glossary (each in 10 words or fewer)</h3><dl>
<dt>CSI</dt><dd>Channel State Information: WiFi signal measurements per antenna.</dd>
<dt>LOSO</dt><dd>Leave-One-Subject-Out: test on a person never trained on.</dd>
<dt>LOEO</dt><dd>Leave-One-Environment-Out: test in a room never trained on.</dd>
<dt>BVP</dt><dd>Body-coordinate Velocity Profile: movement map independent of location.</dd>
<dt>DFS</dt><dd>Doppler Frequency Shift: frequency change caused by moving bodies.</dd>
<dt>open-set</dt><dd>Handling strangers: system admits people it never saw before.</dd>
</dl></div>
<h2 id="papers">Papers (__COUNT_PAPERS__)</h2>
<input type="text" id="qPapers" placeholder="Search papers by title, venue, year, status...">
<table><thead><tr><th>Title</th><th>Year</th><th>Venue</th><th>PDF</th><th>Status</th></tr></thead>
<tbody id="paperRows"></tbody></table>
<h2 id="facts">Key Facts (__COUNT_LEDGER__ citable claims)</h2>
<input type="text" id="qFacts" placeholder="Search facts by claim, source, or quote...">
<div id="factCards"></div>
<h2 id="gaps">Gaps — Audited Mistakes To Avoid (__COUNT_GAPS__)</h2>
<p>Each gap is one audit finding. It names a risky claim, the verdict on it, what to use instead, and how to validate it.</p>
<input type="text" id="qGaps" placeholder="Search gaps by keyword...">
<div id="gapCards"></div>
<h2 id="data">Datasets &amp; Hardware</h2>
<div class="warn"><b>WARNING — estimates, not measurements:</b> simulated data splits
(random vs LOSO vs LOEO scores) and edge latency figures are <b>simulated / estimated</b>,
not lab measurements. Do not report them as measured results. Real datasets carry a
<span class="badge real">REAL</span> badge; anything simulated carries
<span class="badge sim">SIMULATED</span> and latency figures carry <span class="badge est">ESTIMATE</span>.</div>
<div id="benchBox"></div>
<h2 id="plan">Reading Plan — 8 anchor papers</h2>
<p>Check off papers as you read. Progress is saved in this browser (localStorage).</p>
<div id="planBox"></div>
<div id="prog"></div>
<script>
__DATA_JS__
</script>
<script>
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function bibTitle(b){var p=PAPERS.find(function(x){return x.bib===b});return p?p.title:b}
function highlight(bib){document.querySelectorAll("[data-bib]").forEach(function(el){
  var hit=el.getAttribute("data-bib")===bib||(el.getAttribute("data-bibs")||"").split(",").indexOf(bib)>=0;
  el.classList.toggle("hl",hit);});}
// papers
function renderPapers(f){var tb=document.getElementById("paperRows");tb.innerHTML="";
PAPERS.filter(function(p){return !f||(p.title+" "+p.venue+" "+p.year+" "+p.status+" "+p.bib).toLowerCase().indexOf(f)>=0})
.forEach(function(p){var tr=document.createElement("tr");tr.setAttribute("data-bib",p.bib);
tr.innerHTML="<td><a href='#' data-open>"+esc(p.title)+"</a><div class='detail'><p><b>Abstract:</b> "+esc(p.abstract||"—")+"</p><p><b>Why it matters:</b> "+esc(p.why||"No plain-English summary yet.")+"</p><p><b>Key:</b> "+esc(p.bib)+"</p></div></td><td>"+esc(p.year)+"</td><td>"+esc(p.venue)+"</td><td>"+(p.pdf?"yes":"—")+"</td><td>"+esc(p.status)+"</td>";
tr.querySelector("[data-open]").onclick=function(e){e.preventDefault();tr.classList.toggle("open");highlight(p.bib)};
tb.appendChild(tr);});}
// facts
function renderFacts(f){var box=document.getElementById("factCards");box.innerHTML="";
LEDGER.filter(function(c){return !f||(c.claim+" "+c.src+" "+c.quote+" "+c.bib).toLowerCase().indexOf(f)>=0})
.forEach(function(c){var d=document.createElement("div");d.className="card";d.setAttribute("data-bib",c.bib);
d.innerHTML="<div class='claim'>"+esc(c.claim)+"</div><p>Source: <b>"+esc(c.src)+"</b> ("+esc(c.bib)+", p. "+esc(c.page)+")</p><p><i>&ldquo;"+esc(c.quote)+"&rdquo;</i></p>";
d.onclick=function(){highlight(c.bib)};box.appendChild(d);});}
// gaps
function renderGaps(f){var box=document.getElementById("gapCards");box.innerHTML="";
GAPS.filter(function(g){return !f||(g.naive+" "+g.fix+" "+g.check+" "+g.verdict).toLowerCase().indexOf(f)>=0})
.forEach(function(g){var d=document.createElement("div");d.className="card";d.setAttribute("data-bibs",g.bibs.join(","));
d.innerHTML="<div class='gapbadge'>"+esc(g.id)+"</div><div class='myth'>Risky claim (do not use): "+esc(g.naive)+"</div><p><b>Audit verdict:</b> "+esc(g.verdict)+"</p><div class='fix'>Use instead: "+esc(g.fix)+"</div><p><b>How to validate:</b> "+esc(g.check)+"</p>";
d.onclick=function(){if(g.bibs[0])highlight(g.bibs[0])};box.appendChild(d);});}
// bench/hw
(function(){var b=document.getElementById("benchBox"),s="";
s+="<h3>Datasets <span class='badge real'>REAL</span></h3><ul>";
Object.keys(BENCH).forEach(function(k){s+="<li><b>"+esc(k)+"</b>: "+esc((BENCH[k].dataset_name||BENCH[k].name||""))+"</li>"});
s+="</ul><h3>Split evaluation <span class='badge sim'>SIMULATED</span></h3><ul>";
var pr=(SIM.protocols||SIM);Object.keys(pr).forEach(function(k){var v=pr[k]||{};
s+="<li>"+esc(k)+": acc "+esc(v.accuracy!=null?v.accuracy:"?")+" — "+esc(v.evaluation_verdict||"simulated estimate")+"</li>"});
s+="</ul><h3>Edge hardware <span class='badge est'>ESTIMATE</span></h3><ul>";
Object.keys(HW).forEach(function(k){var v=HW[k]||{};s+="<li><b>"+esc(k)+"</b>: "+esc(v.platform_name||v.name||"")+"</li>"});
var pf=((EDGE.platforms||EDGE));Object.keys(pf).forEach(function(k){s+="<li>"+esc(k)+" latency: "+esc((pf[k]||{}).int8_latency_ms||"?")+" ms (estimate)</li>"});
s+="</ul>";b.innerHTML=s;})();
// reading plan
(function(){var box=document.getElementById("planBox");var done={};
try{done=JSON.parse(localStorage.getItem("thesis_progress")||"{}")}catch(e){done={}}
ANCHORS.forEach(function(a){var p=PAPERS.find(function(x){return x.id===a.id})||{title:a.id,bib:"",year:"",venue:""};
var l=document.createElement("label");l.className="card";l.style.display="block";l.setAttribute("data-bib",p.bib||"");
var c=document.createElement("input");c.type="checkbox";c.checked=!!done[a.id];
c.onchange=function(){done[a.id]=c.checked;try{localStorage.setItem("thesis_progress",JSON.stringify(done))}catch(e){}prog()};
l.appendChild(c);l.appendChild(document.createTextNode(" "+p.title+" ("+p.year+", "+p.venue+") — "+a.reason));
l.onclick=function(){highlight(p.bib)};box.appendChild(l);});
window.prog=function(){var n=ANCHORS.filter(function(a){return done[a.id]}).length;
document.getElementById("prog").textContent="Progress: "+n+" / "+ANCHORS.length};prog();})();
document.getElementById("qPapers").oninput=function(e){renderPapers(e.target.value.toLowerCase())};
document.getElementById("qFacts").oninput=function(e){renderFacts(e.target.value.toLowerCase())};
document.getElementById("qGaps").oninput=function(e){renderGaps(e.target.value.toLowerCase())};
renderPapers("");renderFacts("");renderGaps("");
</script></body></html>"""

    h = h.replace("__COUNT_PAPERS__", str(np)).replace("__COUNT_CORPUS__", str(nc)).replace("__COUNT_LEDGER__", str(nl)).replace("__COUNT_GAPS__", str(ng)).replace("__DATA_JS__", data_js)
    out = ROOT / "thesis_dashboard.html"
    out.write_text(h, encoding="utf-8")
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
