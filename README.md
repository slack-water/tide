# tide

Public knowledge vault. Projects, research, making, and archive.

This is the public half of a two-repo Obsidian vault system. The private half (`tide-private`) holds personal content — system documentation, values, family, and work. Together they form a single vault that Obsidian sees as one unified space.

## structure

```
40-projects/    active, time-bounded work
50-knowledge/   reading, research, ideation
60-making/      ceramics, 3d printing, woodworking, cad
90-archive/     completed work
```

Each note follows a standard YAML frontmatter schema. The full system definition — principles, schema, folder weights, weekly ritual, and AI interaction protocol — lives in `SYSTEM.md` in the private repo.

## local development

Requires Node.js (for markdownlint via npx) and Python 3 (for frontmatter validation).

```bash
make check   # lint + frontmatter validation — run before opening a PR
make all     # also runs broken link check and spell check
```

No `npm install` needed — tools are invoked via `npx` and resolved on first run.

## repo

- Branch: `main`
- Merges: squash only, branch deleted after merge
- PRs: required; CI (markdown lint + frontmatter validation) must pass
- Cadence: monthly or per-project PRs
- License: CC BY 4.0
