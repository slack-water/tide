# repo management directives

Applies to both `slack-water/tide` (public) and `slack-water/tide-private` (private) unless noted.

---

## 1. branch protection

Configure in GitHub → Settings → Branches → Branch protection rules for `main`:

- Require a pull request before merging
- Require status checks to pass before merging (see §6)
- Require branches to be up to date before merging
- Do not allow bypassing the above settings
- No force pushes to `main`
- No deletion of `main`

---

## 2. pull request workflow

### scoping

A PR should represent one coherent unit of change. Preferred scopes:

- A single folder's updates (`50-knowledge`, `30-work/bnsf`, etc.)
- A single project's full lifecycle entry (create, update, or close)
- A schema or system change

When changes accumulate across folders without a natural grouping, use a cadence PR (see below).

### cadence

If no scoped PR has been opened in the current month, open a cadence PR by the last Friday of the month. Quarterly is acceptable for slow periods, but monthly is preferred. Cadence PRs collect all uncommitted changes across the repo.

### requirements

Every PR must:

- [ ] Describe the scope and summary of changes in the PR description
- [ ] Update `CHANGELOG.md` with an entry under the appropriate section
- [ ] Update the repo `README.md` if the change affects structure, setup, or usage

---

## 3. branch naming

```
add/[folder]-[topic]        # new content or folder
update/[folder]-[topic]     # changes to existing content
fix/[topic]                 # corrections, broken links, frontmatter errors
system/[topic]              # schema changes, system file updates
cadence/YYYY-MM             # monthly or quarterly catchall
```

Examples: `add/40-projects-tide-setup`, `update/50-knowledge-reading`, `cadence/2026-05`

---

## 4. commit messages

Follow the convention established in SYSTEM.md §7c:

```
add: [what was added]
update: [what changed and why]
fix: [what was corrected]
system: [schema or structural change]
```

One subject line. No period. Keep it under 72 characters.

---

## 5. merging

- **Strategy:** squash merge only. The PR description becomes the commit message.
- **Branch cleanup:** delete branch automatically after merge (configure in repo settings).
- **Draft PRs:** use draft status for work-in-progress; only mark ready when the checklist in §2 is complete.

---

## 6. github actions

Both repos use GH Actions to enforce merge requirements. Workflows live in `.github/workflows/`.

### `ci.yml` — runs on every PR

```yaml
- markdown lint (markdownlint-cli2)
- frontmatter validation (required fields present, valid type/status values)
```

Both checks must pass before merge is allowed.

### `links.yml` — runs on push to main

```yaml
- broken link check (markdown-link-check)
```

Runs post-merge to catch dead links without blocking PRs on transient network issues.

---

## 7. makefile

The `Makefile` provides local equivalents of CI checks so you can validate before pushing.

```makefile
lint        # markdownlint on all .md files
validate    # frontmatter schema check (required fields, valid enum values)
links       # broken link scan
spell       # spell check (cspell)
check       # runs lint + validate (mirrors CI exactly)
all         # runs lint + validate + links + spell
```

Run `make check` before opening a PR. CI runs the same command.

---

## 8. changelog format

Follow [Keep a Changelog](https://keepachangelog.com) conventions. File lives at `CHANGELOG.md` in each repo root.

```markdown
## [Unreleased]

## [YYYY-MM-DD]

### Added

### Changed

### Removed
```

Entries go under `[Unreleased]` during development. At release/tag time, replace with the date.

---

## 9. releases and tags

Tag quarterly snapshots on `main` after the cadence PR merges:

```
YYYY-Q1    YYYY-Q2    YYYY-Q3    YYYY-Q4
```

Tag with an annotated tag and a one-line description of the quarter's notable changes. This is a lightweight snapshot, not a software release — no assets needed.

```bash
git tag -a 2026-Q2 -m "Q2 2026: tide setup, initial projects scaffolded"
git push origin 2026-Q2
```

---

## 10. pr template

Lives at `.github/pull_request_template.md` in each repo.

```markdown
## Scope

[Which folder(s) or project does this PR touch?]

## Summary

[What changed and why?]

## Checklist

- [ ] CHANGELOG.md updated
- [ ] README.md updated (if structure or setup changed)
- [ ] `make check` passes locally
```

---

## 11. licenses

| Repo | License | Rationale |
|------|---------|-----------|
| `tide` (public) | CC BY 4.0 | Open sharing with attribution; appropriate for notes, research, and making docs |
| `tide-private` (private) | All Rights Reserved | Default copyright; personal and family content is not for redistribution |

`LICENSE` file lives at each repo root. The private repo's LICENSE file contains: `Copyright (c) [year] Colin Smith. All rights reserved.`

---

## 12. readme

`tide` (public) requires a `README.md` at the repo root explaining what the vault is, how it's structured, and how the two-repo system works (link to SYSTEM.md for detail).

`tide-private` does not need a README — SYSTEM.md serves that purpose.
