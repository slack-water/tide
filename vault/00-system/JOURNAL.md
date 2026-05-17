---
title: Journal
created: 2026-05-16
updated: 2026-05-16
folder: 00
type: log
status: active
importance: 3
schema-version: 1.0
---

# Journal

*A living record of the vault as a used thing. Not structural — temporal. Captures when things were added, what changed in your thinking, what the system felt like to use. The changelog records what the system is; the journal records what it was like to build it.*

*Entries go newest first. This file lives on the `personal` branch and is never merged back to `main`.*

---

## format

Each entry is a dated section. Keep it honest and brief — this is a log, not a performance.

```markdown
## YYYY-MM-DD

[What happened in the vault today. What changed in your thinking. What the system
felt like to use. Schema merges go here too — note which version landed and whether
anything needed migration.]
```

For schema merges specifically:

```markdown
## YYYY-MM-DD — schema vX.X merged

Merged schema vX.X from main. [What changed structurally.] [Any notes needing
migration, and whether they were handled.]
```

---

## example entry

## 2026-05-16 — initialization

initialized tide. two repos, two symlinks, one vault. the name came out of a long
conversation about what to call a life system that doesn't feel lifeless. slack water
is the identity; tide is the work.

the core insight that made the structure click: separate the schema from the data.
main stays clean and forkable; personal is where the actual life goes. schema changes
flow one direction only.

first real captures: the branching pattern, the ios shortcut idea for inbox, and the
realization that values belong in 00-system — not 10-self — because they're upstream
of everything, not just personal health.

---

*replace this file with your own entries on the `personal` branch.*
