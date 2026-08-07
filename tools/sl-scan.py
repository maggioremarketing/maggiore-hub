#!/usr/bin/env python3
"""Escáner incremental de estudios SL en la Clients Folder (Combe/SIA).

Agrupa archivos en "estudios" (carpeta de proyecto COMBEMAGxxxx o nombre
normalizado), elige la ÚLTIMA versión de cada uno sin borrar nada, y compara
contra el registro para detectar estudios nuevos o versiones nuevas.

Salidas (en tools/sl-data/):
  registry.json  — estado conocido: key -> {file, stamp, study_id}
  pending.json   — estudios nuevos/actualizados que requieren resumen (Claude)
studies.json (curado, mismo dir) NO se toca aquí: lo edita Claude al resumir.
"""
import os, re, json, sys, unicodedata
from datetime import datetime

SIA = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-SharedLibraries-Maggiore/"
    "João-Franco Maggi - CLIENT'S FOLDERS/Combe/SIA")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "tools", "sl-data")
os.makedirs(DATA, exist_ok=True)

BRANDS = {"Astroglide": "Astroglide", "Just For Men": "Just For Men", "Vagisil": "Vagisil"}
CODE_RE = re.compile(r"(COMBEMAG\d{4})", re.I)
DATE_RES = [
    (re.compile(r"(20\d{2})[.\-_](\d{1,2})[.\-_](\d{1,2})"), "ymd"),
    (re.compile(r"(\d{1,2})[.\-_](\d{1,2})[.\-_](20\d{2})"), "dmy_or_mdy"),
    (re.compile(r"(\d{1,2})\.(\d{1,2})\.(\d{2})\b"), "mdy2"),
]
NOISE = re.compile(
    r"\b(final|share|v\d+|copy|draft|rev\w*|20\d{2}|slmaggiore|maggiore|combe|x)\b"
    r"|\(\d+\)|[\d.\-_]{6,}", re.I)


def name_date(fn):
    """Fecha embebida en el nombre, si existe (datetime) — la señal más confiable."""
    for rx, kind in DATE_RES:
        m = rx.search(fn)
        if not m:
            continue
        a, b, c = (int(x) for x in m.groups())
        try:
            if kind == "ymd":
                return datetime(a, b, c)
            if kind == "mdy2":
                return datetime(2000 + c, a, b)
            # dmy o mdy: si el primer campo > 12 es día
            if a > 12:
                return datetime(c, b, a)
            return datetime(c, a, b)
        except ValueError:
            continue
    return None


def norm_key(fn):
    """Nombre normalizado para agrupar versiones del mismo estudio suelto."""
    base = os.path.splitext(fn)[0]
    base = unicodedata.normalize("NFKD", base)
    base = base.replace("_", " ").replace("-", " ")
    base = re.sub(r"(?i)v\d+\b", " ", base)
    base = NOISE.sub(" ", base)
    words = re.findall(r"[a-zA-Z]{2,}", base.lower())
    return "-".join(words[:6]) or base.lower()


def scan():
    units = {}  # key -> {brand, files: [(path, stamp)]}
    for brand_dir, brand in BRANDS.items():
        broot = os.path.join(SIA, brand_dir)
        if not os.path.isdir(broot):
            continue
        for dirpath, dirnames, filenames in os.walk(broot):
            # excluir material del cliente / insumos
            dirnames[:] = [d for d in dirnames if d.lower() not in ("input", "inputs", "assets", "data")]
            for fn in filenames:
                if not fn.lower().endswith(".pptx") or fn.startswith("~$"):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path, broot)
                # unidad: código de proyecto (en carpeta o nombre) > nombre normalizado
                m = CODE_RE.search(rel)
                # código + nombre normalizado: un proyecto puede tener varios entregables
                nk = norm_key(fn)
                key = f"{brand}:{m.group(1).upper()}:{nk}" if m else f"{brand}:{nk}"
                nd = name_date(fn)
                mt = datetime.fromtimestamp(os.path.getmtime(path))
                stamp = (nd or mt).strftime("%Y-%m-%d")
                units.setdefault(key, {"brand": brand, "files": []})
                units[key]["files"].append({"path": path, "stamp": stamp, "name_dated": bool(nd)})
    # última versión por unidad: primero por fecha-en-nombre, luego mtime
    out = {}
    for key, u in units.items():
        files = sorted(u["files"], key=lambda f: (f["stamp"], f["name_dated"]))
        latest = files[-1]
        out[key] = {"brand": u["brand"], "file": latest["path"], "stamp": latest["stamp"],
                    "versions": len(files)}
    return out


def main():
    reg_path = os.path.join(DATA, "registry.json")
    registry = json.load(open(reg_path)) if os.path.exists(reg_path) else {}
    current = scan()

    pending = []
    for key, cur in sorted(current.items()):
        known = registry.get(key)
        if known is None:
            pending.append({"key": key, "reason": "nuevo", **cur})
        elif known.get("file") != cur["file"]:
            pending.append({"key": key, "reason": "nueva versión", **cur})

    json.dump(current, open(os.path.join(DATA, "scan-latest.json"), "w"),
              ensure_ascii=False, indent=1)
    json.dump(pending, open(os.path.join(DATA, "pending.json"), "w"),
              ensure_ascii=False, indent=1)

    print(f"estudios detectados: {len(current)} · pendientes de procesar: {len(pending)}")
    for p in pending:
        print(f"  [{p['reason']}] {p['key']} -> {os.path.basename(p['file'])} ({p['stamp']}, {p['versions']} versiones)")

    if "--commit-registry" in sys.argv:
        json.dump(current, open(reg_path, "w"), ensure_ascii=False, indent=1)
        print("registro actualizado")


if __name__ == "__main__":
    main()
