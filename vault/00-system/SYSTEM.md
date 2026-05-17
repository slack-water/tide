---
title: tide — system definition
created: 2026-05-16
updated: 2026-05-16
folder: 00
type: reference
status: active
importance: 5
schema-version: 1.0
---

# tide — system definition

> *slack water: the still moment between tides. not empty — suspended. the water isn't going nowhere; it's deciding.*
> *tide: the work that creates balance.*

> **purpose:** a single source of truth for how this vault is structured, why it's structured that way, and how changes to the structure propagate. a change at this level is a schema change. schema changes trigger a review cascade.

---

## 0. Core Principles

1. **Markdown is the contract.** All content lives in `.md` files. The app (Obsidian, VS Code, anything else) is a viewport, not the system. If the app disappears, the system survives.
2. **The folder is the address, the frontmatter is the metadata.** Navigation happens by folder. Querying, filtering, and AI-readability happen via YAML frontmatter.
3. **Schema changes trickle down.** When the structure or frontmatter schema of a section changes, affected notes are tagged `#needs-review` with a confidence score and an importance score. Review is a deliberate act, not an interruption.
4. **One inbox, zero ambiguity.** New captures go to `inbox.md` in the private vault. Nothing lives in inbox permanently.
5. **Values are upstream of everything.** Folder importance weights are derived from proximity to defined personal values. A note's importance score is a function of its folder weight and its explicit `importance` frontmatter field.
6. **Simplicity over completeness.** A note that exists and is imperfect is better than a perfect note that was never written. Resist the urge to build the system instead of using it.

---

## 1. Folder Structure

### 1a. on-disk layout

The Obsidian vault root (`~/tide/`) is not itself a git repo. It contains two symlinked subfolders, each pointing at the `vault/` subdirectory of an independent git repository. This keeps repo tooling (Makefile, CI, scripts) out of the Obsidian view while maintaining a unified editing and linking experience.

```
~/tide/                       ← Obsidian vault root (not a git repo)
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

Repos:

- `slack-water/tide` — public GitHub repo
- `slack-water/tide-private` — private GitHub repo

Pushing:

```bash
cd ~/code/tide && git push
cd ~/code/tide-private && git push
```

Wikilinks work across both repos because Obsidian sees the full vault. The symlink boundary is invisible to the editor.

> **note:** do not use iCloud or Dropbox to sync the vault root — both handle symlinks poorly. use Obsidian Sync or rely on git alone.

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
| inbox.md | private | raw capture; processed weekly, not for publication |

visibility is decided by **where you save the file**, not by tagging or flags. if something in a public folder needs to be private, move it. intentionality is the system.

### 1c. content structure

```
public/ (→ ~/code/tide/vault/)
├── 00-system/              ← meta layer. the vault's brain.
│   ├── SYSTEM.md           ← this file.
│   ├── GUIDE.md            ← day-to-day operating manual.
│   ├── PRAXIS.md           ← how i operate. what i believe about my own agency.
│   ├── ANXIETIES.md        ← anxiety tracker and challenger.
│   ├── VALUES.md           ← personal values definition (output of values project).
│   └── SCHEMA-CHANGELOG.md ← log of all schema changes and their cascade scope.
│
├── 40-projects/            ← active, time-bounded work. cross-domain.
│   │                         each project gets a folder with a README.md.
│   └── _template/          ← project template. copy, don't modify.
│
├── 50-knowledge/           ← reading, research, ideation, learning log.
│   ├── reading/
│   │   ├── current.md
│   │   ├── archive.md
│   │   └── queue.md
│   └── research/           ← topics being thought about, studied, or incubated.
│
├── 60-making/              ← ceramics, 3d printing, woodworking, CAD, design.
│   ├── ceramics/
│   ├── 3d-printing/
│   ├── woodworking/
│   └── cad/
│
└── 90-archive/             ← completed projects, closed contexts, past versions.

private/ (→ ~/code/tide-private/vault/)
├── inbox.md                ← capture inbox. processed on weekly reset.
│
├── 10-self/                ← health and wellbeing. (values live in 00-system.)
│   ├── health/
│   └── wellbeing/
│
├── 20-family/              ← erin, ben, household, shared finances.
│   ├── erin/
│   ├── ben/                ← rent system, adulting framework, launch support.
│   └── household/
│
└── 30-work/                ← BNSF, career arc, professional development.
    ├── bnsf/
    └── career/
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
related:        # optional — [[wikilinks]] to related notes
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
| `output` | A finished artifact produced by a project (e.g. VALUES.md, a document, a decision) |
| `template` | A copy-before-use file; never modify the original |

---

## 3. Schema Change Protocol

When the structure of a section, a folder, or this frontmatter schema changes:

1. **Log the change** in `00-system/SCHEMA-CHANGELOG.md` with:
   - Date
   - What changed
   - Scope (which folders/note types are affected)
   - Migration instructions (what a note needs to do to comply)

2. **Tag affected notes** with `#needs-review` and add a frontmatter field:

   ```yaml
   review-reason: "Schema change YYYY-MM-DD — [brief description]"
   review-confidence: 0.0–1.0   # how likely auto-tag is correct
   ```

3. **Prioritize the review queue** by `importance` × `review-confidence`. High-importance notes with low confidence should be reviewed first.

4. **AI-assisted migration:** When using Claude Code or any AI to apply a schema change, instruct it to: tag, score, and add `review-reason`, but NOT to silently rewrite content. Flag, don't fix.

> **Design note:** The review system is intentionally lightweight. The goal is a visible queue, not automated enforcement. A weekly reset pass through `#needs-review` is sufficient. Do not build infrastructure for this until the vault has 100+ notes and schema changes have actually happened.

---

## 4. Values Weighting

Folder importance weights are defined here and used to calculate a note's default importance when no explicit `importance` is set.

> These weights are a starting point. They should be reviewed after `00-system/VALUES.md` is completed and updated to reflect actual values priority.

| Folder | Weight | Rationale |
|--------|--------|-----------|
| 00-system | 1.0 | Holds VALUES.md — values are upstream of everything |
| 20-family | 0.95 | Core relationships and responsibilities |
| 10-self | 0.85 | Health and wellbeing — important but narrower than values |
| 40-projects | 0.7 | Active work; importance varies by project |
| 30-work | 0.65 | Important but bounded to professional context |
| 60-making | 0.6 | Identity-adjacent; high intrinsic value |
| 50-knowledge | 0.55 | Feeds everything; low urgency |
| 90-archive | 0.2 | Historical; rarely needs review |

**Effective importance** (for review prioritization) = `folder-weight × note-importance`

---

## 5. Key System Files

### 00-system/PRAXIS.md

*How I operate.* Not aspirational — descriptive and honest.

- What I believe about agency, decision-making, and follow-through
- Known failure modes and their early signals
- How I make decisions under uncertainty
- This is a living `output`-type note, updated when self-understanding shifts

### 00-system/ANXIETIES.md

*Anxiety tracker and challenger. Each entry is a structured block, newest first.*

```markdown
## [title] — YYYY-MM-DD

**the anxiety:** [what you're worried about, in plain language]
**category:** decision-paralysis | relationship | health | financial | existential | other
**triggered by:** [what surfaced it]

**challenge questions:**

- what is the realistic cost of reversing this decision?
- what is the cost of *not* deciding?
- what is the worst realistic outcome, and can i survive it?
- what would i tell a trusted friend in this situation?
- is this a real risk or a story i'm telling myself?

**resolution/update:** [leave blank until something shifts]
**status:** open | resolved | reframed
```

### 00-system/JOURNAL.md

*A living record of the vault as a used thing. Not structural — temporal. Captures when things were added, what changed in your thinking, what the system felt like to use. The changelog records what the system is; the journal records what it was like to build it.*

Lives on the `personal` branch. Never merges back to `main`. Entries newest first.

### 00-system/SCHEMA-CHANGELOG.md

*Schema version history.* Append-only. Covers structural changes as they land in the vault — not a narrative, a technical record.

```markdown
## v1.0 — 2026-05-16
Initial schema. See SYSTEM.md §2 for frontmatter definition.
Scope: all notes.
```

### 50-knowledge/reading/

Three files. Keep them simple — a table is enough.

**current.md** — what you're actively reading
**queue.md** — want to read, with a one-line reason why
**archive.md** — finished reads with a 1–3 sentence review and a 1–5 rating

### 40-projects/_template/README.md

```yaml
---
title:
created:
updated:
folder: 40
type: project
status: active
importance: 3
goal:         # one sentence: what done looks like
scope:        # what's in and what's out
tags: []
related: []
schema-version: 1.0
---
```

```markdown
## Goal
[One sentence.]

## Scope
**In:** 
**Out:** 

## Done looks like
[Concrete, observable outcome.]

## Next action
- [ ] 

## Log
### YYYY-MM-DD
[Updates go here, newest first.]
```

---

## 6. Weekly Reset Ritual

A lightweight pass, not a planning session. Run once per week.

1. Process `inbox.md` — every item either moves to its folder or gets deleted
2. Review `#needs-review` queue — work through highest-priority items first
3. Update `status` on active projects — is anything stale?
4. Add to reading/research logs if anything was consumed or captured that week
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

Two repos, one vault. See §1a for the full on-disk layout. See §7a for the branch model.

```bash
# create the repo directories
mkdir -p ~/code/tide
mkdir -p ~/code/tide-private

# initialize each as a git repo
cd ~/code/tide && git init
cd ~/code/tide-private && git init

# create the vault root and symlinks
# symlinks point to vault/ subdirs so Obsidian doesn't see repo tooling
mkdir ~/tide
ln -s ~/code/tide/vault ~/tide/public
ln -s ~/code/tide-private/vault ~/tide/private

# add remotes (after creating repos on GitHub)
cd ~/code/tide
git remote add origin https://github.com/slack-water/tide.git

cd ~/code/tide-private
git remote add origin https://github.com/slack-water/tide-private.git
```

Point Obsidian at `~/tide/` as the vault root.

### 7c. github account migration

1. ~~check `github.com/slack-water` — if 404, the handle is available~~
2. ~~open an incognito window, create a placeholder account with your old handle (`davidcolinsmith`) using a throwaway email — this prevents redirect breakage~~
3. ~~rename your main account: `settings → account → change username → slack-water`~~
4. ~~update any local repo remotes: `git remote set-url origin <new-url>`~~
5. after 30–60 days with nothing broken, delete the placeholder account

> ✓ migration complete as of 2026-05-16. steps 1–4 done.

### 7d. commit hygiene

- no credentials, account numbers, or sensitive personal data in plaintext — ever
- commit messages should be meaningful (`add: ben rent system v1` not `update notes`)
- commit the `.obsidian/` config folder (preserves plugins, themes, hotkeys)
- exclude workspace and cache files

`.gitignore` for both repos:

```
.obsidian/workspace
.obsidian/cache
.DS_Store
```

- if a specific note ever needs encryption, use `git-crypt` scoped to that file or folder — the rest of the repo remains readable

---

## 8. AI Interaction Protocol

When using Claude, Claude Code, or any AI against this vault:

- Always pass `SYSTEM.md` as context for structural or schema-related tasks
- For schema changes: instruct AI to tag and log, not silently rewrite
- For content generation: AI produces drafts; human approves before commit
- AI-generated notes should include `ai-assisted: true` in frontmatter
- The AI is a collaborator on the *content*; the human owns the *structure*

---

## 9. Open Questions (parking lot)

*Things to resolve once the vault has been lived in for a while.*

- [ ] Should projects in `40-projects` ever live in domain folders (e.g. `20-family/projects/`)? Decision: revisit after first 5 projects are created.
- [ ] What's the right granularity for health notes — daily log vs. topic-based reference?
- [ ] Does making (60) deserve its own project subfolder, or do making projects live in 40-projects?
- [ ] Formal values weighting: complete after VALUES.md is written.

---

*schema version: 1.0 — initial definition*
*last updated: see git log*
