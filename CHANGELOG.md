# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

## [2026-05-20]

### Added

- `make install` target — creates `~/tide/` vault root, both repo symlinks (`public/`, `private/`),
  and `~/tide/CLAUDE.md` symlink so Claude Code loads instructions at the vault root

### Changed

- `CLAUDE.md` — extended with `/init` health check, per-folder context pattern, vault structure
  map, and `make upgrade` reference in system mode; `make install` now referenced for setup
- `SETUP.md` §2 — vault root setup now leads with `make install`
- `scripts/validate-skip.json` — `PRIORITIES.md` added to frontmatter skip list

## [2026-05-17]

### Added

- `vault/00-system/FAILURE-MODES.md` — second upstream document alongside `VALUES.md`; pre-populated
  with the over-optimization spiral entry; read by AI alongside values for every decision
- `vault/00-system/FAILURE-MODES_example.md` — worked example showing the entry format; removed by
  `make init`
- `CLAUDE.md` at repo root — AI context file encoding the decision-support prompt architecture;
  Claude reads `VALUES.md` and `FAILURE-MODES.md` before assisting with any decision or schema task
- `scripts/schema-upgrade.py` — tags notes with outdated `schema-version` as `needs-review`, adding
  `review-reason` and `review-confidence` fields; supports `--dry-run` and `--version` flags
- `make upgrade` target — runs schema upgrade script

### Changed

- `PHILOSOPHY.md` — full rewrite around the decision support engine framing: defines values and
  failure modes plainly, explains frontmatter, includes the decision prompt, notes the scalability
  observation as incidental rather than primary
- `README.md` — leads with decision support framing; nav labels updated to philosophy · infrastructure
  · usage · configuration
- `vault/00-system/SYSTEM.md` — renamed heading to "infrastructure"; added orientation line pointing
  to PHILOSOPHY.md for the reasoning layer; surfaced `FAILURE-MODES.md` in §1c and §5
- `vault/00-system/GUIDE.md` — renamed heading to "usage"
- `SETUP.md` — renamed heading to "configuration"
- `Makefile` — `FAILURE-MODES_example.md` added to `make init`
- `scripts/validate-skip.json` — `CLAUDE.md` exempted from frontmatter validation

### Planned

- **Capture from anywhere (iOS Shortcut)** — iOS Shortcut that appends to `vault/inbox.md` in the
  private repo via the GitHub Contents API; commits directly to the `personal` branch with no app
  required. See [tide-private #4](https://github.com/slack-water/tide-private/issues/4).
- **Selective publication (`public: true`)** — GitHub Action that copies notes with `public: true`
  frontmatter from the private repo into the public repo on push. Visibility stays a frontmatter
  decision; no manual file moves required. See [tide-private #5](https://github.com/slack-water/tide-private/issues/5).

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
