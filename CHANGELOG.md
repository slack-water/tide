# Changelog

All notable changes to this repository are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

## [2026-05-16]

### Added

- Initial folder structure: 40-projects, 50-knowledge, 60-making, 90-archive
- Project template at 40-projects/_template/README.md
- Reading lists (current, queue, archive) in 50-knowledge/reading/
- Makefile with lint, validate, links, spell, and check targets (requires Node.js + Python 3)
- Frontmatter validation script (scripts/validate-frontmatter.py)
- GitHub Actions CI on PRs: markdown lint and frontmatter validation via npx
- GitHub Actions link check on push to main
- PR template, markdownlint config (.markdownlint.json), link-check config (.mlc-config.json)
- LICENSE (CC BY 4.0)
- README with structure overview, local dev setup, and repo policy summary

### Changed

- CI lint job switched from markdownlint-cli2-action to npx to match Makefile exactly
- markdownlint config tuned for prose vault: disabled line-length, duplicate headings,
  first-line-h1, blockquote blank lines, unlabeled fences, table pipe spacing,
  and front-matter title double-counting
