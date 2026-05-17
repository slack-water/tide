---
title: System Guide
created: 2026-05-16
updated: 2026-05-16
folder: 00
type: reference
status: active
importance: 4
schema-version: 1.0
---

# System Guide

*Day-to-day operating manual. How to use the system, not how it is defined. For the schema and structural spec, see [[SYSTEM]].*

---

## Capturing a new note

1. Drop a quick capture in `inbox.md` (private vault) with a one-line description and today's date
2. If you already know where it belongs, create the file directly in the right folder
3. Every note gets the standard frontmatter block — copy from an existing note or the template below
4. Set `status: incubating` if the note is a stub; `status: active` once it has real content

Minimum viable note:

```yaml
---
title: My Note
created: YYYY-MM-DD
updated: YYYY-MM-DD
folder: 50
type: note
status: incubating
schema-version: 1.0
---
```

---

## Processing the inbox

Run once per week during the weekly reset (see §6 of SYSTEM.md).

- Each item in `inbox.md` either gets a real home or gets deleted
- Move the item to its folder, add full frontmatter, and remove the line from inbox
- If the item spawns a project, create a folder under `40-projects/` using `_template/README.md`
- Inbox is empty at the end of reset — not "mostly empty"

---

## Creating a new project

1. Copy `40-projects/_template/README.md` into a new folder: `40-projects/[project-name]/README.md`
2. Fill in `title`, `created`, `goal`, and `scope` in the frontmatter
3. Set `status: active`
4. Write the Goal, Scope, Done looks like, and first Next action
5. Commit and push to `personal`

Projects live in `40-projects/` regardless of domain (work, family, making). If a project is private it belongs in the private repo — move it if it ends up in the wrong place.

---

## Writing a note for a specific folder

| You want to capture... | Folder | Repo |
|------------------------|--------|------|
| System, values, praxis, anxieties | 00-system/ | public |
| Active project | 40-projects/ | public |
| Something you read / are reading | 50-knowledge/reading/ | public |
| Research or a topic you're thinking about | 50-knowledge/research/ | public |
| Ceramics, 3d printing, woodworking, CAD | 60-making/ | public |
| Completed work | 90-archive/ | public |
| Health or wellbeing | 10-self/ | private |
| Family — Erin, Ben, household | 20-family/ | private |
| BNSF, career | 30-work/ | private |
| Quick capture / unsorted | inbox.md | private |

---

## Using wikilinks

Obsidian sees both repos as a single vault via the `~/tide/public` and `~/tide/private` symlinks. Wikilinks work across the boundary:

```
[[SYSTEM]]               links to 00-system/SYSTEM.md
[[VALUES]]               links to 00-system/VALUES.md
[[current]]              links to 50-knowledge/reading/current.md
```

Use the filename without path or extension. If two files share a name, use the relative path: `[[30-work/bnsf/some-note]]`.

---

## Choosing a note type

| Type | Use when... |
|------|-------------|
| `note` | Freeform capture, reflection, or reference without a completion condition |
| `project` | There's a goal, a scope, and a concrete done condition |
| `log` | Append-only entries (ANXIETIES.md, reading archive, SCHEMA-CHANGELOG.md) |
| `reference` | Stable, reusable facts or definitions you'll look up repeatedly |
| `output` | A finished artifact — the result of a project (VALUES.md, a decision doc) |
| `template` | Copy-before-use; never edit the original |

When in doubt, use `note`.

---

## Committing changes

Daily work lives on the `personal` branch and pushes directly — no PR needed:

```bash
git add -A
git commit -m "add: Q2 reading queue entries"
git push origin personal
```

Changes to `main` (schema updates, new templates, structural changes) go via a feature branch and PR:

```bash
git checkout main
git checkout -b system/new-folder
# make your changes
make check                          # lint + validate before pushing
git add -A
git commit -m "system: add dev-environment folder to 60-making"
git push -u origin system/new-folder
# open a PR targeting main
```

Branch naming for main-bound changes: `add/`, `update/`, `fix/`, `system/`, or `cadence/YYYY-MM`. See REPO-MANAGEMENT.md for the full convention.

---

## Using AI with this vault

Pass `SYSTEM.md` as context for any structural or schema question. For content work, the AI drafts — you approve and commit.

Always add `ai-assisted: true` to frontmatter on notes where AI generated the initial draft:

```yaml
ai-assisted: true
```

AI may tag notes for schema review but should not silently rewrite content. If you ask Claude Code to apply a schema change, tell it explicitly: tag and log, don't fix.
