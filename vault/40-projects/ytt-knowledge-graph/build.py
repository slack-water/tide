#!/usr/bin/env python3
"""validate the yoga CSVs and generate mermaid diagrams + graph.json.

usage: python3 build.py                     (from this folder)
       python3 build.py --map F009,L011,T025  (also writes my-map.mmd + one local graph per id)
outputs: diagrams/*.mmd, graph.json, atlas.html (interactive page, images inlined)
"""
import base64
import csv
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"
OUT = HERE / "diagrams"

# free-text names in founders.teachers that refer to another founder row
TEACHER_ALIASES = {
    "t. krishnamacharya": "F009",
    "lahiri mahasaya": "F001",
    "sri yukteswar giri": "F004",
    "swami sivananda": "F008",
    "k. pattabhi jois": "F010",
    "swami kripalvananda": "F023",
    "bishnu charan ghosh": "F020",
    "paulie zink": "F032",
}


def load(name):
    with open(DATA / f"yoga_{name}.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ids(field):
    return [x.strip() for x in (field or "").split(";") if x.strip()]


def esc(s):
    """safe text for a quoted mermaid flowchart label."""
    return s.replace('"', "#quot;")


def bare(s):
    """safe text for mermaid timeline/mindmap, which have no quoting."""
    return re.sub(r"[()\[\]{}:\"#]", "", s).strip()


def validate(t):
    errors = []
    known = set()
    for name, rows in t.items():
        seen = set()
        for r in rows:
            if r["id"] in seen:
                errors.append(f"{name}: duplicate id {r['id']}")
            seen.add(r["id"])
        known |= seen
    refs = [
        ("lineages", "parent_id"), ("lineages", "secondary_parent_ids"),
        ("lineages", "key_founder_ids"), ("founders", "lineage_ids"),
        ("prakriti_gunas", "parent_id"), ("gunas", "parent_id"),
        ("vocab", "related_ids"), ("teaching_scripts", "pose_ref"),
        ("teaching_scripts", "vocab_refs"),
        ("founder_relations", "from_id"), ("founder_relations", "to_id"),
    ]
    for table, col in refs:
        for r in t[table]:
            for ref in ids(r[col]):
                if ref not in known:
                    errors.append(f"{table} {r['id']}.{col}: unknown id {ref}")
    return errors


def teacher_edges(founders):
    """(teacher_key, student_id, label, traditional) — teacher_key is a founder id or 'X:name'."""
    edges = []
    for f in founders:
        for raw in ids(f["teachers"]):
            traditional = "traditional account" in raw
            name = re.sub(r"\s*\(.*?\)", "", raw).strip()
            key = TEACHER_ALIASES.get(name.lower(), "X:" + name)
            edges.append((key, f["id"], name, traditional))
    return edges


def short(name):
    return re.sub(r"\s*\(.*?\)", "", name).strip()


def mmd_lineages(lineages):
    out = ["flowchart TD"]
    for l in lineages:
        out.append(f'  {l["id"]}["{esc(l["name"])}"]')
    for l in lineages:
        if l["parent_id"]:
            out.append(f'  {l["parent_id"]} --> {l["id"]}')
        for p in ids(l["secondary_parent_ids"]):
            out.append(f'  {p} -.-> {l["id"]}')
    out += ["  classDef era fill:#f4ead5,stroke:#8a6d3b,color:#1f2430",
            "  classDef studio fill:#e3eef7,stroke:#4a7aa0,color:#1f2430"]
    out.append("  class " + ",".join(l["id"] for l in lineages if l["type"] in ("era", "root")) + " era")
    out.append("  class " + ",".join(l["id"] for l in lineages if l["type"] == "style") + " studio")
    return out


def mmd_founders(founders, lineages, relations):
    """teacher → student flowchart, founders grouped into subgraphs by lineage."""
    by_id = {f["id"]: f for f in founders}
    lname = {l["id"]: l["name"] for l in lineages}
    out = ["flowchart LR"]
    groups = {}
    for f in founders:
        groups.setdefault(ids(f["lineage_ids"])[0], []).append(f)
    for lid, fs in groups.items():
        out.append(f'  subgraph {lid}_g["{esc(short(lname[lid]))}"]')
        for f in fs:
            years = f"{f['birth_year']}–{f['death_year']}" if f["birth_year"] else ""
            label = esc(short(f["name"])) + (f"<br/>{years}" if years else "")
            out.append(f'    {f["id"]}["{label}"]')
        out.append("  end")
    externals = {}
    for key, student, name, trad in teacher_edges(founders):
        if key.startswith("X:"):
            node = "X" + str(len(externals) + 1) if key not in externals else externals[key]
            if key not in externals:
                externals[key] = node
                out.append(f'  {node}(["{esc(name)}"]):::ext')
            key = node
        out.append(f"  {key} {'-.->' if trad else '-->'} {student}")
    for r in relations:
        out.append(f'  {r["from_id"]} -. {r["type"]} .- {r["to_id"]}')
    out.append("  classDef ext fill:#eee,stroke:#999,color:#555")
    return out


def mmd_timeline(timeline, title):
    """one section per era, eras ordered by their earliest event."""
    rows = sorted(timeline, key=lambda r: int(r["start_year"]))
    eras = list(dict.fromkeys(r["era"] for r in rows))
    out = ["timeline", f"  title {title}"]
    for era in eras:
        out.append(f"  section {bare(era)}")
        for t in (r for r in rows if r["era"] == era):
            out.append(f"    {bare(t['display_date'])} : {bare(t['short_title'])}")
    return out


def mmd_prakriti(tree, gunas):
    out = ["flowchart TD"]
    for p in tree + gunas:
        label = esc(p["name_iast"]) + "<br/>" + esc(p.get("name_english") or p["english_gloss"])
        out.append(f'  {p["id"]}["{label}"]')
    for p in tree + gunas:
        if p["parent_id"]:
            out.append(f'  {p["parent_id"]} --> {p["id"]}')
    out.append("  P001 -. saṃyoga .- P002")
    return out


def mmd_asana(asanas, key):
    out = ["mindmap", "  root((āsana names))"]
    groups = {}
    for a in asanas:
        groups.setdefault(a[key].split("/")[0] if key == "category" else a[key], []).append(a)
    for g, rows in sorted(groups.items()):
        out.append(f"    {bare(g) or 'other'}")
        for a in rows:
            out.append(f"      {bare(a['asana_iast'])} — {bare(a['common_english'].split(';')[0])}")
    return out


def graph_json(t):
    """nodes + edges for the interactive page."""
    nodes, edges = [], []
    for f in t["founders"]:
        nodes.append({"id": f["id"], "kind": "founder", "label": short(f["name"]),
                      "name": f["name"], "role": f["role"], "born": f["birth_year"],
                      "died": f["death_year"], "region": f["region"],
                      "year": f["first_notable_year"] or f["birth_year"],
                      "lineages": ids(f["lineage_ids"]), "known_for": f["known_for"],
                      "works": f["key_works"], "notes": f["notes"], "confidence": f["confidence"]})
        for lid in ids(f["lineage_ids"]):
            edges.append({"s": f["id"], "t": lid, "kind": "lineage"})
    for l in t["lineages"]:
        nodes.append({"id": l["id"], "kind": "lineage", "type": l["type"], "label": short(l["name"]),
                      "name": l["name"], "year": l["start_year"], "emphasis": l["emphasis"],
                      "notes": l["notes"]})
        if l["parent_id"]:
            edges.append({"s": l["parent_id"], "t": l["id"], "kind": "branch"})
        for p in ids(l["secondary_parent_ids"]):
            edges.append({"s": p, "t": l["id"], "kind": "influence"})
    seen = set()
    for key, student, name, trad in teacher_edges(t["founders"]):
        if key.startswith("X:"):
            nid = "X_" + re.sub(r"\W+", "_", name)
            if nid not in seen:
                seen.add(nid)
                nodes.append({"id": nid, "kind": "teacher", "label": name, "name": name,
                              "notes": "teacher outside this dataset" + (" (traditional account)" if trad else "")})
            key = nid
        edges.append({"s": key, "t": student, "kind": "teacher", "traditional": trad})
    for r in t["founder_relations"]:
        edges.append({"s": r["from_id"], "t": r["to_id"], "kind": r["type"], "notes": r["notes"]})
    # timeline events link to founders named in key_figures
    names = {short(f["name"]).lower(): f["id"] for f in t["founders"]}
    names.update(TEACHER_ALIASES)
    names.update({"sharon gannon": "F026", "david life": "F026"})
    for ev in t["timeline"]:
        nodes.append({"id": ev["id"], "kind": "event", "label": ev["display_date"], "title": ev["short_title"], "name": ev["event"],
                      "era": ev["era"], "category": ev["category"], "year": ev["start_year"],
                      "end": ev["end_year"], "texts": ev["texts"], "notes": ev["significance"],
                      "confidence": ev["confidence"]})
        for fig in ids(ev["key_figures"]):
            fid = names.get(short(fig).lower())
            if fid and {"s": ev["id"], "t": fid, "kind": "event"} not in edges:
                edges.append({"s": ev["id"], "t": fid, "kind": "event"})
    return {"nodes": nodes, "edges": edges}


# how each edge kind reads, from source to target
EDGE_LABEL = {"teacher": "taught", "branch": "branch", "influence": "influenced", "lineage": "school",
              "event": "involved", "sibling": "sibling", "parent": "parent of", "co-author": "co-author"}


def node_label(n):
    if n["kind"] == "founder":
        years = f"{n['born']}–{n['died']}" if n.get("born") else ""
        return n["label"] + (f"<br>{years}" if years else "")
    if n["kind"] == "event":
        return f"{n['title']}<br>{n['label']}"
    return n["label"]


def mmd_subgraph(g, node_ids, edges, focus=None, selected=()):
    """flowchart of the given nodes and edges. node ids are aliased (teacher ids aren't mermaid-safe)."""
    by_id = {n["id"]: n for n in g["nodes"]}
    alias = {nid: f"n{i}" for i, nid in enumerate(node_ids)}
    out = ["flowchart LR"]
    for nid in node_ids:
        n = by_id[nid]
        shape = ('(["', '"])') if n["kind"] == "teacher" else ('{{"', '"}}') if n["kind"] == "event" else ('["', '"]')
        out.append(f'  {alias[nid]}{shape[0]}{esc(node_label(n))}{shape[1]}')
    for e in edges:
        arrow = "-.->" if e.get("traditional") or e["kind"] == "influence" else "-->"
        if e["kind"] in ("sibling", "co-author"):
            arrow = "-.-"
        out.append(f'  {alias[e["s"]]} {arrow}|{EDGE_LABEL[e["kind"]]}| {alias[e["t"]]}')
    out += ["  classDef founder fill:#fdf3e1,stroke:#c98a12,color:#1f2430",
            "  classDef lineage fill:#e8ecf7,stroke:#2f3f7a,color:#1f2430",
            "  classDef event fill:#f2f2ee,stroke:#7a6a50,color:#1f2430",
            "  classDef teacher fill:#eee,stroke:#999,color:#555",
            "  classDef focus stroke-width:4px"]
    for kind in ("founder", "lineage", "event", "teacher"):
        members = [alias[i] for i in node_ids if by_id[i]["kind"] == kind]
        if members:
            out.append(f"  class {','.join(members)} {kind}")
    if focus:
        out.append(f"  class {alias[focus]} focus")
    return out


def mmd_my_map(g, ids):
    """the selected nodes and every edge between them."""
    edges = [e for e in g["edges"] if e["s"] in ids and e["t"] in ids]
    return mmd_subgraph(g, list(ids), edges)


def mmd_local(g, nid):
    """one node and everything one step away."""
    edges = [e for e in g["edges"] if nid in (e["s"], e["t"])]
    nodes = list(dict.fromkeys([nid] + [x for e in edges for x in (e["s"], e["t"])]))
    return mmd_subgraph(g, nodes, edges, focus=nid)


def portrait_uris(size=112, quality=82):
    """square, top-weighted crops as data URIs (faces sit high in portraits)."""
    try:
        from PIL import Image
    except ImportError:
        print("pillow not installed: atlas.html will use initials only")
        return {}
    uris = {}
    for f in sorted((HERE / "images").glob("*.jpg")):
        im = Image.open(f).convert("RGB")
        side = min(im.size)
        left, top = (im.width - side) // 2, int((im.height - side) * 0.15)
        im = im.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=quality)
        uris[f.stem] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return uris


def write_page(g):
    credits_path = HERE / "images" / "credits.json"
    credits = json.loads(credits_path.read_text()) if credits_path.exists() else {}
    page = (HERE / "page.template.html").read_text(encoding="utf-8")
    for marker, value in (("/*GRAPH*/null", g), ("/*IMAGES*/{}", portrait_uris()), ("/*CREDITS*/{}", credits)):
        page = page.replace(marker, json.dumps(value, ensure_ascii=False))
    (HERE / "atlas.html").write_text(page, encoding="utf-8")


def write_explorer(g, ids):
    """notion embed: my map + click-through local graphs. notion caps uploads at 200 KiB."""
    pages_path = HERE / "notion" / "page_ids.json"
    pages = json.loads(pages_path.read_text()) if pages_path.exists() else {}
    compact = lambda v: json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    page = (HERE / "explorer.template.html").read_text(encoding="utf-8")
    for marker, value in (("/*GRAPH*/null", g), ("/*IMAGES*/{}", portrait_uris(72, 72)),
                          ("/*SELECTED*/[]", ids), ("/*PAGES*/{}", pages)):
        page = page.replace(marker, compact(value))
    size = len(page.encode("utf-8"))
    if size > 200 * 1024:
        sys.exit(f"explorer.html is {size // 1024} KiB; notion's limit is 200")
    (HERE / "explorer.html").write_text(page, encoding="utf-8")
    print(f"explorer.html: {size // 1024} KiB")


def main():
    tables = ["timeline", "lineages", "founders", "asana_etymology", "prakriti_gunas",
              "gunas", "vocab", "teaching_scripts", "founder_relations"]
    t = {name: load(name) for name in tables}
    errors = validate(t)
    for e in errors:
        print("ERROR", e)
    if errors:
        sys.exit(1)
    OUT.mkdir(exist_ok=True)
    diagrams = {
        "lineages": mmd_lineages(t["lineages"]),
        "founders": mmd_founders(t["founders"], t["lineages"], t["founder_relations"]),
        "timeline-premodern": mmd_timeline([r for r in t["timeline"] if int(r["start_year"]) < 1800],
                                           "Premodern yoga (dates approximate; verify)"),
        "timeline-modern": mmd_timeline([r for r in t["timeline"] if int(r["start_year"]) >= 1800],
                                        "Modern yoga 1875–present (verify)"),
        "prakriti": mmd_prakriti(t["prakriti_gunas"], t["gunas"]),
        "asana-by-category": mmd_asana(t["asana_etymology"], "category"),
        "asana-by-root": mmd_asana(t["asana_etymology"], "root_or_stem"),
    }
    for name, lines in diagrams.items():
        (OUT / f"{name}.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
    g = graph_json(t)
    (HERE / "graph.json").write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")
    write_page(g)
    if "--map" in sys.argv:
        ids = [x.strip() for x in sys.argv[sys.argv.index("--map") + 1].split(",") if x.strip()]
        known = {n["id"] for n in g["nodes"]}
        missing = [x for x in ids if x not in known]
        if missing:
            sys.exit(f"unknown ids: {missing}")
        (OUT / "my-map.mmd").write_text("\n".join(mmd_my_map(g, ids)) + "\n", encoding="utf-8")
        (OUT / "local").mkdir(exist_ok=True)
        for nid in ids:
            (OUT / "local" / f"{nid}.mmd").write_text("\n".join(mmd_local(g, nid)) + "\n", encoding="utf-8")
        write_explorer(g, ids)
        print(f"map: {len(ids)} nodes")
    print(f"ok: {len(diagrams)} diagrams, {len(g['nodes'])} nodes, {len(g['edges'])} edges")


if __name__ == "__main__":
    main()
