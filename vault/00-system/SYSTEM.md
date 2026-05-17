---
title: tide — system definition
created: 2026-05-16
updated: 2026-05-17
folder: 00
type: reference
status: active
importance: 5
schema-version: 1.0
---

# tide — system definition

> **purpose:** a single source of truth for how this vault is structured, why it's structured that way, and how changes to the structure propagate. a change at this level is a schema change. schema changes trigger a review cascade.

---

## 0. Core Principles

See [PHILOSOPHY.md](../../PHILOSOPHY.md) for the full reasoning behind these principles.

1. **Markdown is the contract.** All content lives in `.md` files. The editor is a viewport, not the system.
2. **The folder is the address, the frontmatter is the metadata.** Navigation happens by folder. Querying, filtering, and AI-readability happen via YAML frontmatter.
3. **Schema changes trickle down.** When the structure or frontmatter schema of a section changes, affected notes are tagged `#needs-review`. Review is a deliberate act, not an interruption.
4. **One inbox, zero ambiguity.** New captures go to `inbox.md` in the private vault. Nothing lives in inbox permanently.
5. **Values are upstream of everything.** Folder importance weights are derived from proximity to defined personal values. A note's importance score is a function of its folder weight and its explicit `importance` frontmatter field.
6. **Simplicity over completeness.** A note that exists and is imperfect is better than a perfect note that was never written.

---

## 1. Folder Structure

### 1a. on-disk layout

The vault root (`~/tide/`) is not itself a git repo. It contains two symlinked subfolders, each pointing at the `vault/` subdirectory of an independent git repository. This keeps repo tooling (Makefile, CI, scripts) out of the editor view while maintaining a unified editing and linking experience.

```
~/tide/                       ← vault root (not a git repo)
├── public -> ~/code/tide/vault/
│   ├── 00-system/
│   ├── 40-projects/
│   ├── 50-knowledge/
│   ├── 60-making/
│   └── 90-archive/
└── private -> ~/code/tide-private/vault/
    ├── 10-self/
    ├── 20-family/
    ├── 30-work/
    └── inbox.md

~/code/tide/                  ← public git repo (slack-water/tide)
├── vault/                    ← symlink target for ~/tide/public
└── [Makefile, CI, scripts, etc.]

~/code/tide-private/          ← private git repo (slack-water/tide-private)
├── vault/                    ← symlink target for ~/tide/private
└── [Makefile, CI, scripts, etc.]
```

Pushing:

```bash
cd ~/code/tide && git push
cd ~/code/tide-private && git push
```

Wikilinks work across both repos because the editor sees the full vault. The symlink boundary is invisible.

> **note:** do not use iCloud or Dropbox to sync the vault root — both handle symlinks poorly. use a sync tool that respects symlinks, or rely on git alone.

### 1b. visibility defaults

| Folder | Repo | Rationale |
|--------|------|-----------|
| 00-system | public | system definition, values, praxis — live openly |
| 10-self | private | health, wellbeing — personal and sensitive |
| 20-family | private | others' lives; not yours to publish |
| 30-work | private | professional context |
| 40-projects | public | work in progress, openly shared |
| 50-knowledge | public | reading, research, ideation |
| 60-making | public | craft documentation |
| 90-archive | public | completed work |
| inbox.md | private | raw capture; processed on reset, not for publication |

Visibility is decided by **where you save the file**, not by tagging or flags. If something in a public folder needs to be private, move it.

### 1c. content structure

```
public/ (→ ~/code/tide/vault/)
├── 00-system/              ← meta layer. the vault's brain.
│   ├── SYSTEM.md           ← this file.
│   ├── GUIDE.md            ← day-to-day operating manual.
│   ├── PRAXIS.md           ← how you operate. what you believe about your own agency.
│   ├── ANXIETIES.md        ← anxiety tracker and challenger.
│   ├── VALUES.md           ← personal values definition.
│   └── SCHEMA-CHANGELOG.md ← log of all schema changes and their cascade scope.
│
├── 40-projects/            ← active, time-bounded work. cross-domain.
│   └── _template/          ← project template. copy, don't modify.
│
├── 50-knowledge/           ← reading, research, ideation, learning log.
│   ├── reading/
│   │   ├── current.md
│   │   ├── archive.md
│   │   └── queue.md
│   └── research/
│
├── 60-making/              ← craft documentation.
│
└── 90-archive/             ← completed projects, closed contexts, past versions.

private/ (→ ~/code/tide-private/vault/)
├── inbox.md                ← capture inbox. processed on reset.
├── 10-self/                ← health and wellbeing.
├── 20-family/
└── 30-work/
```

---

## 2. Frontmatter Schema (Standard)

Every note should include this block at the top. Fields marked `required` must be present. Fields marked `optional` can be omitted but are preferred.

```yaml
---
title:          # required — human-readable title
created:        # required — YYYY-MM-DD
updated:        # required — YYYY-MM-DD (update on every meaningful edit)
folder:         # required — top-level folder number (e.g. 10, 40)
type:           # required — note | project | log | reference | output | template
status:         # required — active | incubating | complete | archived | needs-review
importance:     # optional — 1–5 (5 = most important; default 3)
                #   importance is weighted by folder proximity to values (see §4)
tags:           # optional — list of tags
related:        # optional — wikilinks to related notes
schema-version: # required — matches current version in SCHEMA-CHANGELOG.md
---
```

### Type Definitions

| Type | Meaning |
|------|---------|
| `note` | Freeform capture, reflection, or reference |
| `project` | Has a goal, a scope, and a done condition |
| `log` | Dated entries; append-only |
| `reference` | Stable facts, definitions, templates, or reference material |
| `output` | A finished artifact produced by a project |
| `template` | A copy-before-use file; never modify the original |

---

## 3. Schema Change Protocol

When the structure of a section, a folder, or this frontmatter schema changes:

1. **Log the change** in `00-system/SCHEMA-CHANGELOG.md` with:
   - Date
   - What changed
   - Scope (which folders/note types are affected)
   - Migration instructions (what a note needs to do to comply)

2. **Tag affected notes** with `status: needs-review` and add:

   ```yaml
   review-reason: "schema change YYYY-MM-DD — [brief description]"
   review-confidence: 0.0–1.0   # how likely the auto-tag is correct
   ```

3. **Prioritize the review queue** by `folder-weight × importance × review-confidence`. High-confidence tags on high-importance notes surface first.

4. **AI-assisted migration:** Instruct AI to tag, score, and add `review-reason` — but not to silently rewrite content. Flag, don't fix.

> The review system is intentionally lightweight. A weekly reset pass through `#needs-review` is sufficient. Do not build automation for this until the vault has 100+ notes.

---

## 4. Values Weighting

Folder importance weights are used to calculate a note's default importance when no explicit `importance` is set.

> These weights are a starting point. Revisit after `VALUES.md` is written.

| Folder | Weight | Rationale |
|--------|--------|-----------|
| 00-system | 1.0 | Holds VALUES.md — values are upstream of everything |
| 20-family | 0.95 | Core relationships and responsibilities |
| 10-self | 0.85 | Health and wellbeing |
| 40-projects | 0.7 | Active work; importance varies by project |
| 30-work | 0.65 | Important but bounded to professional context |
| 60-making | 0.6 | Identity-adjacent; high intrinsic value |
| 50-knowledge | 0.55 | Feeds everything; low urgency |
| 90-archive | 0.2 | Historical; rarely needs review |

**Effective importance** (for review prioritization) = `folder-weight × note-importance`

---

## 5. Key System Files

Each file below has an example file alongside it showing what a hydrated version looks like and how to fill it in. Run `make init` to remove example files once you're ready to write your own.

### PRAXIS.md

*A living description of how you operate.* Not aspirational — honest and descriptive. Updated when self-understanding shifts. See [PRAXIS_example.md](PRAXIS_example.md).

### ANXIETIES.md

*Anxiety tracker and challenger.* Each entry is a structured block with challenge questions and a resolution field. Newest first. See [ANXIETIES_example.md](ANXIETIES_example.md).

### VALUES.md

*Your personal values definition.* The output of deliberate reflection — what you actually care about, not what you think you should care about. Shapes folder weights and review priority. Write this first. See [VALUES_example.md](VALUES_example.md).

### JOURNAL.md

*Temporal log of the vault as a lived thing.* Not structural — captures when things were added, what changed in your thinking, what the system felt like to use. Lives on the `personal` branch; never merges back to `main`. Entries newest first.

### SCHEMA-CHANGELOG.md

*Schema version history.* Append-only. Referenced when merging `main` into `personal` to understand what migrated and why.

### GUIDE.md

*Day-to-day operating manual.* How to capture, process the inbox, create a project, commit, and use wikilinks. Start here after setup.

---

## 6. Weekly Reset Ritual

A lightweight pass, not a planning session.

1. Process `inbox.md` — every item either moves to its folder or gets deleted
2. Review `#needs-review` queue — work through highest-priority items first
3. Update `status` on active projects — is anything stale?
4. Add to reading/research logs if anything was consumed or captured
5. Check ANXIETIES.md — are any open anxieties ready to be resolved or reframed?

---

## 7. git & version control

### 7a. branch model

Two branches per repo:

| Branch | Purpose |
|--------|---------|
| `main` | Clean schema, templates, and system documentation. No personal data. Forkable. |
| `personal` | Live working branch. Your actual notes, entries, and life. Never merges back to main. |

Schema changes flow one direction: `main → personal`. Tag `main` with semantic versions (`v1.0`, `v1.1`). Tag `personal` with dates (`2026-05-16`).

To pull a schema update from main into your personal branch:

```bash
git checkout personal
git merge main --no-ff -m "merge: schema vX.X into personal (YYYY-MM-DD)"
```

Log the merge in `00-system/SCHEMA-CHANGELOG.md`.

### 7b. repository setup

See [SETUP.md](../../SETUP.md) for the full bootstrap walkthrough.

### 7c. commit hygiene

- No credentials, account numbers, or sensitive personal data in plaintext — ever
- Commit messages should be meaningful (`add: ben rent system v1` not `update notes`)
- Commit your editor's config folder if it stores plugins, themes, and hotkeys there
- Exclude workspace and cache files

`.gitignore` for both repos:

```
.obsidian/workspace
.obsidian/cache
.DS_Store
__pycache__/
node_modules/
```

- If a specific note ever needs encryption, use `git-crypt` scoped to that file or folder

---

## 8. AI Interaction Protocol

When using Claude, Claude Code, or any AI against this vault:

- Always pass `SYSTEM.md` as context for structural or schema-related tasks
- For schema changes: instruct AI to tag and log, not silently rewrite
- For content generation: AI produces drafts; human approves before commit
- AI-generated notes should include `ai-assisted: true` in frontmatter
- The AI is a collaborator on the *content*; the human owns the *structure*

---

*schema version: 1.0 — initial definition*
*last updated: see git log*
