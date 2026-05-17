# tide — setup guide

Everything here is about getting the system running. For the principles behind these decisions, see [PHILOSOPHY.md](PHILOSOPHY.md). For the full system spec, see [SYSTEM.md](vault/00-system/SYSTEM.md).

---

## 0. prerequisites

- **git** — for version control
- **Python 3** — frontmatter validation (`scripts/validate-frontmatter.py`)
- **Node.js** — markdown lint via npx (no install needed; tools resolve on first run)
- **a markdown editor** — anything works. VS Code, Obsidian, iA Writer, a terminal.

---

## 1. repository setup

tide uses two repositories: one public, one private.

```bash
# clone (after forking on GitHub)
git clone https://github.com/your-handle/tide ~/code/tide
git clone https://github.com/your-handle/tide-private ~/code/tide-private

# create your personal branch in each
cd ~/code/tide && git checkout -b personal && git push -u origin personal
cd ~/code/tide-private && git checkout -b personal && git push -u origin personal
```

Your daily work lives on `personal`. Structural changes (new folders, schema updates) go to `main` via PR, then merge down into `personal`. See [SYSTEM.md §7](vault/00-system/SYSTEM.md) for the full branch model.

---

## 2. vault root and symlinks

The vault root is a plain directory — not a git repo. It contains two symlinks pointing at the `vault/` subdirectory of each repo. Your editor sees everything as one unified space; the git boundary is invisible.

```bash
mkdir ~/tide
ln -s ~/code/tide/vault ~/tide/public
ln -s ~/code/tide-private/vault ~/tide/private
```

The symlinks point to `vault/` subdirs, not the repo roots. This keeps tooling files (Makefile, scripts, CI) out of your editor's view.

> Do not use iCloud or Dropbox to sync the vault root — both handle symlinks poorly. Use a sync tool that respects symlinks, or rely on git alone.

Open `~/tide` as your vault root in your editor of choice.

---

## 3. tooling

```bash
make check   # markdown lint + frontmatter validation
make all     # also runs broken link check and spell check
```

Run `make check` before opening a PR against `main`.

---

## 4. first steps

```bash
make init    # removes example files — run once after forking
```

Then open the vault and start with [`VALUES.md`](vault/00-system/VALUES.md). The example files (`*_example.md` in `00-system/`) show you what each key file looks like when hydrated and walk you through filling them in. Remove them with `make init` when you're ready to write your own.

Order of operations after setup:

1. `make init` — clear the examples
2. Write `VALUES.md` — values shape everything else
3. Write `PRAXIS.md` — how you operate, honestly
4. Write `ANXIETIES.md` — open with whatever's on your mind
5. Start your `personal` branch and push — this is your vault now

---

## 5. frontmatter schema

Every note carries a standard frontmatter block. The schema is defined in [SYSTEM.md §2](vault/00-system/SYSTEM.md) — that's the source of truth. A brief reference:

```yaml
---
title:
created:          # YYYY-MM-DD
updated:          # YYYY-MM-DD
folder:           # top-level folder number (00, 10, 40...)
type:             # note | project | log | reference | output | template
status:           # active | incubating | complete | archived | needs-review
importance:       # 1–5 (optional, default 3)
schema-version:   # matches current version in SCHEMA-CHANGELOG.md
---
```

---

## 6. version control hygiene

`.gitignore` for both repos:

```
.obsidian/workspace
.obsidian/cache
.DS_Store
__pycache__/
node_modules/
```

- No credentials, account numbers, or sensitive personal data in plaintext — ever
- Commit messages should be meaningful: `add: ben rent system v1`, not `update notes`
- Commit your editor's config folder if it stores plugins, themes, or hotkeys
- If a specific note needs encryption, use `git-crypt` scoped to that file
