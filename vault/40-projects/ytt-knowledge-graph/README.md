---
title: YTT Knowledge Graph
created: 2026-10-15
updated: 2026-10-16
folder: 40
type: project
status: active
importance: 3
goal: see how yoga's founders, schools, texts and eras connect, as pictures, for YTT study
scope: verify the dataset against the YTT manual — no new views or new research until that's done
tags: [yoga, teaching, ytt, visualization]
related: [ytt-overview, yoga-breath-cueing]
schema-version: 1.0
ai-assisted: true
---

## Goal

one dataset of yoga history (people, lineages, events, terms) that feeds a map i can open full-screen and study from.

## Where it lives now

the code, data and site moved out of the vault on 2026-10-16:

- **site:** [yoga.info-grabber.com](https://yoga.info-grabber.com) — unlisted (noindex), not access-controlled.
- **repo:** `slack-water/yoga-atlas` (private), local at `~/code/yoga-atlas`. the CSVs in `data/` are the source of truth. edit them, `make test`, push to `main`, and ci rebuilds and deploys.
- **infra:** terraform, modeled on `~/code/hoothootknow` (s3 + cloudfront + acm + route53 + github oidc). the repo's README covers setup and the edit loop.

this folder is only the pointer. the old files (build script, csvs, portraits, notion payloads) are in git history before the commit that slimmed it.

## Caveats

- **the whole dataset is an ai draft from memory.** nothing has been checked against the YTT manual yet. verify before teaching from it; add a `source_url` column as rows get checked. the site's panel only says dates are approximate and contested.
- 11 founders have no free portrait (krishnamacharya included) and show a family-colour circle instead.
- the notion mirror is retired: the Founders & Teachers and Lineages & Schools databases and the Connections Map page were trashed on 2026-10-16 (restorable from notion's trash for a while). Key Terms and Yoga History Timeline still hold the rows merged in from this project, with leftover `Dataset ID`, `On map` and `Needs verification` columns.

## Next action

verify the founders and lineages rows against the YTT manual. that's the work this project is waiting on.

## Log

### 2026-10-15

project opened. imported the downloaded dataset, added founder relations and timeline short titles, built the atlas with 31 portraits, mirrored everything into notion with real relations, merged into Key Terms (81 new, 6 enriched) and Yoga History Timeline (38 new, 2 tagged).

### 2026-10-16

moved off notion: separate repo, aws static hosting at yoga.info-grabber.com, collapsible side panel, ci deploys on push. notion mirror retired. vault copy slimmed to this note.
