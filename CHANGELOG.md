# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

## [2026-05-16]

### Added

- Initial folder structure: `vault/40-projects`, `vault/50-knowledge`, `vault/60-making`, `vault/90-archive`
- `vault/00-system/` — system spec, values, praxis, anxieties, schema changelog, guide, journal;
  moved from `tide-private` so system documentation lives in the public core
- `vault/00-system/VALUES.md` — moved from `tide-private/10-self/`; values are system-wide
- `vault/00-system/JOURNAL.md` — log of the vault as a lived thing; placeholder with format
  examples and an initialization entry; hydrated on the `personal` branch
- Project template at `vault/40-projects/_template/README.md`
- Reading lists (`current.md`, `queue.md`, `archive.md`) in `vault/50-knowledge/reading/`
- `REPO-MANAGEMENT.md` at repo root — repo hygiene conventions (not a vault note)
- `SETUP.md` at repo root — bootstrap and setup reference (not a vault note)
- Makefile with `lint`, `validate`, `links`, `spell`, `check`, and `all` targets (requires Node.js + Python 3)
- Frontmatter validation script (`scripts/validate-frontmatter.py`)
- GitHub Actions CI on PRs: markdown lint and frontmatter validation via npx
- GitHub Actions link check on push to main
- PR template, markdownlint config (`.markdownlint.json`), link-check config (`.mlc-config.json`)
- LICENSE (CC BY 4.0)
- Branching model: `main` holds clean schema and templates (forkable, no personal data);
  `personal` is the live working branch; schema changes flow `main → personal`, never back

### Changed

- All vault content moved into `vault/` subdirectory so repo tooling stays out of the Obsidian view
- Symlink target updated: `~/tide/public → ~/code/tide/vault` (not repo root)
- README.md: forker-oriented framing — system intent, main/personal branch separation, two-repo
  structure, frontmatter schema reference, versioning table, fork instructions, philosophy section
- SETUP.md: updated layout diagram, visibility table, content structure, symlink commands, and
  VALUES.md path to reflect current vault structure
- REPO-MANAGEMENT.md: directive 12 updated — tide-private now requires a README
- `scripts/validate-frontmatter.py`: skip `.github/`, `REPO-MANAGEMENT.md`, `SETUP.md`
- CI lint job switched from markdownlint-cli2-action to npx to match Makefile exactly
- markdownlint config tuned for prose vault: disabled line-length, duplicate headings,
  first-line-h1, blockquote blank lines, unlabeled fences, table pipe spacing,
  and front-matter title double-counting
- `PRAXIS.md`, `ANXIETIES.md`, `VALUES.md`: rewritten as example-driven placeholders with
  lowercase tone consistent with JOURNAL.md; guides the `personal` branch voice
