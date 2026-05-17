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
│   ├── 00-system/      ← schema, values, praxis (this repo)
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

# 3. create your personal branch in each repo
cd ~/code/tide && git checkout -b personal
cd ~/code/tide-private && git checkout -b personal

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
