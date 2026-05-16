# tide

> *tide: the work that creates balance.*

A personal knowledge management system built on plain markdown. Content lives in files; Obsidian (or any editor) is just a viewport. If the app disappears, the system survives.

This is the public repo. It holds the system's core — the schema, operating principles, values, and active public work. A companion private repo ([`tide-private`](https://github.com/slack-water/tide-private)) holds personal and sensitive content. Together they form a single vault that Obsidian sees as one unified space.

---

## what's in this repo

`vault/00-system/` is the heart of the system — the spec, the values, the praxis. It's public because living openly is a design decision.

The rest is active work, organized by domain:

| Folder | Contents |
|--------|----------|
| `vault/00-system/` | System spec, values, praxis, anxieties, schema changelog |
| `vault/40-projects/` | Active, time-bounded work (cross-domain) |
| `vault/50-knowledge/` | Reading lists, research, ideation |
| `vault/60-making/` | Ceramics, 3d printing, woodworking, CAD |
| `vault/90-archive/` | Completed work, closed contexts |

All Obsidian content lives under `vault/` so repo tooling (Makefile, CI, scripts) stays invisible to the editor.

---

## full vault structure

Obsidian is pointed at `~/tide/`, which symlinks into both repos' `vault/` subdirectories:

```
~/tide/
├── public  →  ~/code/tide/vault/
│   ├── 00-system/          ← system spec, values, praxis (this repo)
│   ├── 40-projects/
│   ├── 50-knowledge/
│   ├── 60-making/
│   └── 90-archive/
└── private  →  ~/code/tide-private/vault/
    ├── inbox.md            ← capture inbox; raw and unfiltered
    ├── 10-self/            ← health and wellbeing
    ├── 20-family/          ← others' lives; not for publication
    └── 30-work/            ← professional context
```

Visibility is decided by **where a file lives**, not by tagging or flags. If something in a public folder needs to be private, move it. Intentionality is the system.

---

## content split rationale

| Content | Repo | Why |
|---------|------|-----|
| System spec, values, praxis, anxieties | public | Living openly; these are safe and worth sharing |
| Projects, knowledge, making, archive | public | Work in progress and completed work |
| `inbox.md` | private | Raw capture; not ready for publication by definition |
| Health, wellbeing | private | Personal and sensitive |
| Family | private | Others' lives to protect |
| Professional context | private | Work content stays bounded |

---

## getting started

For the full bootstrap walkthrough, see [`SETUP.md`](SETUP.md). The short version:

```bash
# clone both repos
git clone https://github.com/slack-water/tide.git ~/code/tide
git clone https://github.com/slack-water/tide-private.git ~/code/tide-private

# create the vault root and symlinks
mkdir ~/tide
ln -s ~/code/tide/vault ~/tide/public
ln -s ~/code/tide-private/vault ~/tide/private
```

Point Obsidian at `~/tide/` as the vault root. Wikilinks work across both repos because Obsidian sees the full vault — the symlink boundary is invisible to the editor.

> Do not use iCloud or Dropbox to sync the vault root — both handle symlinks poorly. Use Obsidian Sync or rely on git alone.

---

## local development

Requires Node.js (markdownlint via npx) and Python 3 (frontmatter validation). No `npm install` needed — tools resolve on first run.

```bash
make check   # lint + frontmatter validation — run before opening a PR
make all     # also runs broken link check and spell check
```

---

## reference docs

| Document | Purpose |
|----------|---------|
| [`SETUP.md`](SETUP.md) | Full bootstrap: on-disk layout, git setup, symlinks, gitignore |
| [`REPO-MANAGEMENT.md`](REPO-MANAGEMENT.md) | Repo hygiene: PR workflow, branch naming, CI, changelog, releases |
| [`vault/00-system/SYSTEM.md`](vault/00-system/SYSTEM.md) | Full system spec: principles, schema, folder weights, weekly ritual, AI protocol |
| [`vault/00-system/GUIDE.md`](vault/00-system/GUIDE.md) | Day-to-day operating guide: capturing, inbox, projects, wikilinks |

---

## repo policy

See [`REPO-MANAGEMENT.md`](REPO-MANAGEMENT.md) for the full conventions. In brief:

- **Branches:** PRs required; no direct push to `main`
- **CI:** markdown lint + frontmatter validation must pass before merge
- **Merges:** squash only, branch deleted after merge
- **Branch names:** `add/`, `update/`, `fix/`, `system/`, `cadence/YYYY-MM`
- **Tags:** quarterly snapshots (`2026-Q1`, etc.)

---

## license

[CC BY 4.0](LICENSE) — open sharing with attribution.
