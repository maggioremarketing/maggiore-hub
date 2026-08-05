#!/usr/bin/env python3
"""Ensambla IEP V2: transforma experimentos v1 al esquema narrativo v2,
mezcla con los JSON narrativos nuevos y reinyecta el bloque en combe/index.html."""
import json, re, sys

S = "/private/tmp/claude-501/-Users-maggiorejosemi-Claude-Projects-Virutex/899d02db-861a-4553-b4d1-0ed22ffc07ac/scratchpad"
HTML = S + "/hub-combe-src/repo/combe/index.html"
BLOCK = S + "/iepv2-block2.html"

def v1_to_v2(e):
    """Convierte un experimento del esquema v1 (results planos) al esquema narrativo v2."""
    out = {
        "brand": e["brand"], "experiment_id": e["experiment_id"], "name": e["name"],
        "category": e.get("category"), "status": e.get("status", "completed"),
        "headline": e["name"], "subtitle": "Learning Journey",
        "background": None,
        "objective": e.get("learning_objective"),
        "hypothesis": e.get("hypothesis"),
        "success_criteria": (e["rounds"][0].get("success_criteria") if e.get("rounds") else None),
        "methodology": {"platform": "Iterative Experiment Platform (IEP)", "format": None,
                        "field": "Meta", "kpi": None, "benchmarks": []},
        "audiences": [], "rounds": [], "learnings": [], "recommendations": [],
    }
    bms = {}
    for r in e.get("rounds", []):
        rbms = r.get("benchmarks") or ([r["benchmark"]] if r.get("benchmark") else [])
        if r.get("benchmark_closing"): rbms.append(r["benchmark_closing"])
        for b in rbms: bms[b["metric"]] = b
        charts = []
        res = r.get("results", [])
        stop = [x for x in res if x.get("stopping_power") is not None]
        close = [x for x in res if x.get("closing_power") is not None]
        bm_s = next((b for b in rbms if b["metric"] == "stopping"), None)
        bm_c = next((b for b in rbms if b["metric"] == "closing"), None)
        def row(x, metric):
            val = x["stopping_power"] if metric == "stopping" else x["closing_power"]
            extra = []
            if x.get("reach") is not None: extra.append(f"Reach {x['reach']:,} · Clicks {x['clicks']:,}")
            if x.get("lp_visits") is not None: extra.append(f"LP visits {x['lp_visits']:,} · Add to cart {x['add_to_cart']:,}")
            return {"label": x["claim"], "ref": x.get("ref"), "group": x.get("group"),
                    "value": val, "extra": " · ".join(extra) or None,
                    "better_than": x.get("better_than"),
                    "winner": (r.get("winner") == x["claim"])}
        if stop:
            charts.append({"title": "Stopping Power by claim", "metric": "stopping",
                           "audience": None, "benchmark": ({"lo": bm_s["lo"], "hi": bm_s["hi"]} if bm_s else None),
                           "rows": [row(x, "stopping") for x in stop], "insight": None})
        if close:
            charts.append({"title": "Closing Power by claim", "metric": "closing",
                           "audience": None, "benchmark": ({"lo": bm_c["lo"], "hi": bm_c["hi"]} if bm_c else None),
                           "rows": [row(x, "closing") for x in close], "insight": None})
        if r.get("group_closing"):
            charts.append({"title": "Closing Power by claim group", "metric": "closing",
                           "audience": None, "benchmark": ({"lo": bm_c["lo"], "hi": bm_c["hi"]} if bm_c else None),
                           "rows": [{"label": g["group"], "ref": None, "group": None, "value": g["closing_power"],
                                     "extra": f"LP visits {g['lp_visits']:,} · Add to cart {g['add_to_cart']:,}",
                                     "better_than": g.get("better_than"), "winner": False} for g in r["group_closing"]],
                           "insight": None})
        if not charts and res:
            charts.append({"title": "Concepts in field", "metric": "stopping", "audience": None,
                           "benchmark": None,
                           "rows": [{"label": x["claim"], "ref": x.get("ref"), "group": x.get("group"),
                                     "value": None, "extra": None, "better_than": None, "winner": False} for x in res],
                           "insight": None})
        out["rounds"].append({"round": r.get("round"), "dates": r.get("dates"),
                              "charts": charts, "narrative": [], "outcome": r.get("outcome")})
    out["methodology"]["benchmarks"] = list(bms.values())
    return out

def finalize(e):
    """Precalcula campos de tarjeta."""
    labels = set()
    from collections import Counter
    wins = Counter()
    for r in e.get("rounds", []):
        for ch in r.get("charts", []):
            for x in ch.get("rows", []):
                labels.add(x["label"])
                if x.get("winner") and x.get("value") is not None:
                    wins[x["label"]] += 1
    e["claims_count"] = len(labels)
    e["card_winner"] = (wins.most_common(1)[0][0] if wins else None)
    return e

# ---- cargar datos ----
v1 = json.load(open(S + "/data-jfm1.json", encoding="utf-8"))          # E01, E02, E03 (v1)
new_jfm = json.load(open(S + "/data2-jfm45.json", encoding="utf-8"))   # E04, E05 (v2 narrativo)
new_vag = json.load(open(S + "/data2-vagisil.json", encoding="utf-8")) # Vag E01, E02 (v2 narrativo)

data = [finalize(v1_to_v2(e)) for e in v1] + [finalize(e) for e in new_jfm] + [finalize(e) for e in new_vag]

# limpieza: quitar frases de leyenda de deck que no aplican al gráfico web
def clean_insight(t):
    if not t: return t
    t = re.sub(r"Dashed lines? = [^·.]*·\s*", "", t)
    t = re.sub(r"\s*Crops show the buy section[^.]*\.", "", t)
    return t.strip()
for e in data:
    for r in e["rounds"]:
        for ch in r.get("charts", []):
            ch["insight"] = clean_insight(ch.get("insight"))

# ---- reinyectar ----
html = open(HTML, encoding="utf-8").read()
marker = "<!-- ===== IEP V2 STYLES ===== -->"
start = html.index(marker)
end = html.index("</body>")
block = open(BLOCK, encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=True).replace("</", "<\\/")
assert block.count("/*__IEPV2_DATA__*/[]") == 1
block = block.replace("/*__IEPV2_DATA__*/[]", payload)
html = html[:start] + block + "\n" + html[end:]
open(HTML, "w", encoding="utf-8").write(html)
n_charts = sum(len(r.get("charts", [])) for e in data for r in e["rounds"])
print(f"OK · {len(data)} experimentos · {n_charts} gráficos · html {len(html):,} chars")
