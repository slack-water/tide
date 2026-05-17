# tide

> *slack water: the still moment between tides. not empty — suspended. the water isn't going nowhere; it's deciding.*
> *tide: the work that creates balance.*

A personal knowledge and life management system built on plain markdown, git, and the principle that **intent should outlast any tool**.

---

## what this is

tide is a vault structure — a set of folders, templates, and conventions for organizing the things that matter in a life. it is not an app, not a service, and not a framework that requires buying into an ecosystem. it is a folder on your computer with some agreed-upon shapes inside it.

it is designed to be:

- **readable by humans** — plain markdown, always
- **readable by AI** — structured frontmatter, consistent schema, no proprietary formats
- **portable** — if obsidian, or any other tool, disappears tomorrow, nothing is lost
- **forkable** — `main` contains no personal data. take the structure, make it yours.

---

## the core idea

most personal knowledge systems collapse the **schema** (how things are organized) and the **data** (your actual life) into the same place. this makes it hard to share the structure without sharing yourself, and hard to evolve the structure without touching your data.

tide separates them:

```
main branch     ← schema, templates, system documentation. no personal data. forkable.
personal branch ← your actual notes, entries, and life. never merges back to main.
```

schema changes flow one direction: `main → personal`. your data never touches main. the template stays clean and genuinely useful to others; your working vault evolves freely.

---

## two repos, one vault

the vault root (`~/tide/`) is not itself a git repo. it contains two symlinked subfolders, each pointing at the `vault/` subdirectory of an independent git repository. obsidian (or any editor) points at the vault root and sees everything — wikilinks work across both repos, the graph is unified, and the git boundary is invisible to the editor.

```
~/tide/
├── public  →  ~/code/tide/vault/
│   ├── 00-system/      ← schema, values, praxis, anxieties (this repo)
│   ├── 40-projects/
│   ├── 50-knowledge/
│   ├── 60-making/
│   └── 90-archive/
└── private  →  ~/code/tide-private/vault/
    ├── inbox.md        ← capture inbox
    ├── 10-self/        ← health and wellbeing
    ├── 20-family/
    └── 30-work/
```

the symlinks point to `vault/` subdirectories, not the repo roots. this keeps repo-level tooling — `Makefile`, `scripts/`, CI workflows, `SETUP.md` — out of the obsidian view entirely. obsidian sees only vault content; the editor never prompts you to open a yaml frontmatter validation script.

push each repo independently:

```bash
cd ~/code/tide && git push
cd ~/code/tide-private && git push
```

> do not use iCloud or Dropbox to sync the vault root — both handle symlinks poorly. use Obsidian Sync or rely on git alone.

---

## content split

visibility is decided by **where a file lives**, not by tagging or flags. public folders push to a public repo; private folders push to a private repo. if something in a public folder needs to be private, move it. intentionality is the system.

| content | repo | why |
|---------|------|-----|
| system spec, values, praxis, anxieties | public | living openly; safe and worth sharing |
| projects, knowledge, making, archive | public | active and completed work |
| `inbox.md` | private | raw capture; not ready for publication by definition |
| health, wellbeing | private | personal and sensitive |
| family | private | others' lives to protect |
| work | private | professional context stays bounded |

---

## frontmatter schema

every note carries a standard frontmatter block. this is what makes the vault queryable by obsidian, legible to AI, and consistent enough to migrate to any future tool.

```yaml
---
title:
created:          # YYYY-MM-DD
updated:          # YYYY-MM-DD
folder:           # top-level folder number (00, 10, 40...)
type:             # note | project | log | reference | output | template
status:           # active | incubating | complete | archived | needs-review
importance:       # 1–5 (optional, default 3)
tags: []
related: []       # [[wikilinks]]
schema-version:   # matches current version in 00-system/SCHEMA-CHANGELOG.md
---
```

`needs-review` is a special status — see [the review cascade](#the-review-cascade) below.

---

## the review cascade

this is the feature that differentiates tide from a folder layout. when the structure or frontmatter schema of a section changes, affected notes are not silently updated — they are **tagged and queued**.

the protocol:

1. **log the change** in `00-system/SCHEMA-CHANGELOG.md` — what changed, which folders are affected, and what a note needs to do to comply
2. **tag affected notes** with `status: needs-review` and add two fields:

   ```yaml
   review-reason: "schema change 2026-05-16 — added importance field"
   review-confidence: 0.8   # how likely the auto-tag is correct (0.0–1.0)
   ```

3. **prioritize the queue** by `folder-weight × importance × (1 - review-confidence)`. low-confidence tags on high-importance notes surface first.

4. **work through the queue** during the weekly reset — review, update, and clear the tag. flag, don't auto-fix.

the rule: **a change at the top trickles down**. you do not silently migrate content. you build a visible queue and work through it deliberately.

> this system is intentionally lightweight until the vault has 100+ notes and schema changes have actually happened. do not build automation for it prematurely.

---

## values weighting

folder importance weights are defined in `00-system/SYSTEM.md §4` and are used to calculate a note's default importance when no explicit `importance` is set.

| folder | weight | rationale |
|--------|--------|-----------|
| 00-system | 1.0 | holds VALUES.md — values are upstream of everything |
| 20-family | 0.95 | core relationships and responsibilities |
| 10-self | 0.85 | health and wellbeing |
| 40-projects | 0.7 | active work; varies by project |
| 30-work | 0.65 | important but bounded |
| 60-making | 0.6 | identity-adjacent; high intrinsic value |
| 50-knowledge | 0.55 | feeds everything; low urgency |
| 90-archive | 0.2 | historical; rarely needs review |

**effective importance** (for review queue prioritization) = `folder-weight × note-importance`

these weights are a starting point. revisit them after `VALUES.md` is written.

---

## versioning

| branch | tag format | purpose |
|--------|-----------|---------|
| `main` | `v1.0`, `v1.1` | schema and structural releases — for forkers |
| `personal` | `2026-05-16` | dated snapshots of the live vault |

semantic versioning on `main`: patch for clarifications, minor for additive changes (new folder, new template field), major for breaking schema changes requiring migration.

---

## forking this

```bash
# 1. fork slack-water/tide on github, then clone both repos
git clone https://github.com/your-handle/tide ~/code/tide
# create your-handle/tide-private on github, then:
git clone https://github.com/your-handle/tide-private ~/code/tide-private

# 2. create the vault root and symlinks
mkdir ~/tide
ln -s ~/code/tide/vault ~/tide/public
ln -s ~/code/tide-private/vault ~/tide/private

# 3. create and push your personal branch in each repo
cd ~/code/tide && git checkout -b personal && git push -u origin personal
cd ~/code/tide-private && git checkout -b personal && git push -u origin personal

# 4. open ~/tide as your obsidian vault and start with values
```

once initialized, your daily work happens on `personal`. structural changes (new folders, schema updates, template revisions) go to `main` first, then merge down:

```bash
git checkout personal
git merge main --no-ff -m "merge: schema vX.X into personal (YYYY-MM-DD)"
```

---

## local development

requires Node.js (markdownlint via npx) and Python 3 (frontmatter validation). no `npm install` needed — tools resolve on first run.

```bash
make check   # lint + frontmatter validation — run before opening a PR
make all     # also runs broken link check and spell check
```

---

## reference docs

| document | purpose |
|----------|---------|
| [`SETUP.md`](SETUP.md) | full bootstrap: on-disk layout, git setup, symlinks, gitignore |
| [`REPO-MANAGEMENT.md`](REPO-MANAGEMENT.md) | repo hygiene: PR workflow, branch naming, CI, changelog, releases |
| [`vault/00-system/SYSTEM.md`](vault/00-system/SYSTEM.md) | full system spec: principles, schema, folder weights, weekly ritual, AI protocol |
| [`vault/00-system/GUIDE.md`](vault/00-system/GUIDE.md) | day-to-day operating guide: capturing, inbox, projects, wikilinks |
| [`vault/00-system/PRAXIS.md`](vault/00-system/PRAXIS.md) | how you operate: agency, decision-making, known failure modes |
| [`vault/00-system/ANXIETIES.md`](vault/00-system/ANXIETIES.md) | anxiety tracker: structured challenge questions and resolution log |
| [`vault/00-system/JOURNAL.md`](vault/00-system/JOURNAL.md) | temporal log of the vault as a lived thing — personal branch only |
| [`vault/00-system/SCHEMA-CHANGELOG.md`](vault/00-system/SCHEMA-CHANGELOG.md) | schema version history; referenced when merging main into personal |

**three changelogs, three purposes:**

- `CHANGELOG.md` (repo root) — structural changes to the repo: folders added, CI updated, tooling changed. what a developer expects from a changelog.
- `vault/00-system/SCHEMA-CHANGELOG.md` — frontmatter schema version history. the source of truth for `schema-version` in every note. what you reference when merging main into personal to understand what migrated.
- `vault/00-system/JOURNAL.md` — not a changelog. the lived experience: what the system felt like to build, when things were added, what changed in your thinking. temporal and personal; never merges back to main.

---

## roadmap

these patterns are designed but not yet implemented as working tooling:

**capture from anywhere** — an iOS Shortcut that writes directly to `inbox.md` in the private repo via the GitHub Contents API. no app required; a shortcut shares text → it commits to the `personal` branch. see [tide-private issue #4](https://github.com/slack-water/tide-private/issues/4).

**selective publication** — a `public: true` frontmatter field combined with a GitHub Action that copies tagged notes from the private repo into the public one on push. one field decides what surfaces. see [tide-private issue #5](https://github.com/slack-water/tide-private/issues/5).

---

## philosophy

**markdown is the contract.** the app is a viewport, not the system. obsidian, vs code, ia writer, a text editor — none of them matter as long as the files are readable. optimize for the files, not the app.

**intent before implementation.** every system document and template starts with what you want, not how to achieve it. the how changes; the what is stable.

**visibility is a decision, not a default.** public and private are folder-level choices made once, deliberately. nothing is accidentally public; nothing is unnecessarily private.

**the system should cost less than it saves.** if maintaining the structure takes more energy than it returns in clarity, simplify. the weekly reset is the pressure valve. the inbox is the permission to be imperfect.

**values are upstream of everything.** folder importance weights, project prioritization, and the review queue all derive from defined personal values. write `00-system/VALUES.md` before you write anything else.

---

## license

[CC BY 4.0](LICENSE) — open sharing with attribution.
