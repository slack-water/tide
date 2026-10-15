---
title: YTT Knowledge Graph
created: 2026-10-15
updated: 2026-10-15
folder: 40
type: project
status: active
importance: 3
goal: see how yoga's founders, schools, texts and eras connect, as pictures, for YTT study
scope: the CSV dataset, generated diagrams, the interactive atlas, and the notion mirror — no new research until the draft is verified
tags: [yoga, teaching, ytt, visualization, notion]
related: [ytt-overview, yoga-breath-cueing]
schema-version: 1.0
ai-assisted: true
---

## Goal

one dataset of yoga history (people, lineages, events, terms) that feeds every view: the notion databases, mermaid diagrams, and an interactive map with portraits.

## Where things live

- **data/** — the CSVs, source of truth. stable ids (`T` timeline, `L` lineage, `F` founder, `A` āsana, `P` prakṛti, `G` guṇa, `V` vocab, `S` script). `yoga_founder_relations.csv` adds family / co-author links the founders file can't express. `README-source.md` is the original dataset readme.
- **build.py** — validates ids and cross-references, writes `diagrams/*.mmd`, `graph.json`, and `atlas.html` (portraits inlined).
- **fetch_images.py** — pulls free-licensed portraits from wikimedia commons into `images/`, credits in `images/credits.json`. only files wikipedia marks free; hand picks in `FILES` were checked by eye.
- **page.template.html** — the atlas page; build.py fills in the data.
- **explorer.template.html** — the clickable notion embed (my map → local graphs, "open in notion" links). built only with `--map`.
- **notion/** — payloads and page ids used for the notion import.

## Views

- [Yoga Lineage Atlas](https://claude.ai/artifact/GmnMQKiVqocJYwViegS8uK) — web, family tree and timeline; tap a person for teachers, students, schools, events. private artifact.
- notion → Home Yoga YTT Resources → Maps & Connections: Connections Map (mermaid), Founders & Teachers, Lineages & Schools, plus the merged Key Terms and Yoga History Timeline.

## Caveats

- **the whole dataset is an ai draft from memory.** every row imported to notion has `Needs verification` checked. verify against the YTT manual before teaching. the dataset's confidence sits in its own column; my own `Evidentiary Status` calls in the timeline were left alone.
- **the notion home page is published as a notion site**, so the new databases and map page are public too — including the misconduct notes on some founders.
- notion's mermaid blocks default to showing code. switch each to preview from the block's view-mode toggle (lineage tree already done).
- 11 founders have no free portrait (krishnamacharya included) and show a family-colour circle / 🧘 icon instead.

## Updating

edit the CSVs → `python3 build.py` → republish `atlas.html` to the same artifact and paste changed `.mmd` into the notion map page. notion rows aren't auto-synced; the `Dataset ID` column is the join key. `notion/page_ids.json` maps dataset ids to notion page ids.

## Refreshing "my map"

i tick **On map** on ~10 rows across Founders & Teachers, Lineages & Schools and Yoga History Timeline, then ask claude to "refresh my map". claude:

1. queries the three databases for rows with On map checked and collects their `Dataset ID`s
2. runs `python3 build.py --map <ids>` → `diagrams/my-map.mmd`, `diagrams/local/<id>.mmd`, and `explorer.html` (the clickable notion embed; must stay under notion's 200 KiB upload cap)
3. uploads `explorer.html` (notion-create-file-upload, then `curl -F file=@explorer.html` to the returned url) and swaps the `<embed>` on the Connections Map page to the new `file-upload://` source; replaces the code in the static **My map** block below it
4. for each ticked page: replaces its **Local graph** block if it has one, otherwise inserts a "## Local graph" section at the top. local graphs on unticked pages are left alone.

edges come from the CSVs, not from notion relations — a relation added only in notion won't show until it's in the CSV too.

new diagram blocks open in code view. switch each to preview once (view-mode toggle → middle option); the setting survives later refreshes because only the code inside is replaced.

## Log

### 2026-10-15

project opened. imported the downloaded dataset, added founder relations and timeline short titles, built the atlas with 31 portraits (26 founders plus 5 of their teachers; 5 hand-picked from commons), and mirrored everything into notion with real relations (teacher → student, lineage parent/branch, influence, family). merged into existing Key Terms (81 new, 6 enriched) and Yoga History Timeline (38 new, 2 tagged) without touching existing content.

later the same day: added On map checkboxes, my-map and per-page local graph diagrams, and the clickable explorer embed on the Connections Map page.
