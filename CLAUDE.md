# tide

tide is a personal decision-support engine. the vault holds values, failure modes, and life context as first-class, queryable objects. the system exists to make better decisions — not to organize information for its own sake.

---

## reasoning model

when helping with any question, decision, or task in this vault, load context in this order:

1. **`~/tide/public/00-system/VALUES.md`** — upstream of everything. if the file is a stub (no actual values written), say so and ask the user to write it before continuing.
2. **`~/tide/public/00-system/FAILURE-MODES.md`** — constraints and known patterns. if the file is a stub, note it. failure modes are often values in conflict — read them alongside values.
3. **topically relevant vault content** — search both `~/tide/public/` and `~/tide/private/` for notes relevant to the question. folder weights guide priority: `00-system` > `10-self` > `20-family` > `30-work` > `40-projects` > `50-knowledge` > `60-making` > `90-archive`.
4. **per-folder context** — if a `CLAUDE.md` exists in the relevant subfolder (e.g. `40-projects/CLAUDE.md`), read it for domain-specific values and framing. these add specificity on top of VALUES.md; they do not replace it.

apply values and failure modes as explicit lenses. surface conflicts. the goal is better decisions, not better answers.

---

## decision query template

when asked to help with a decision, follow this sequence:

1. read VALUES.md and FAILURE-MODES.md
2. find relevant vault context in both repos
3. name which values and failure modes bear on this specific decision
4. surface any conflicts — between values, or between values and failure modes
5. give a recommendation grounded in the above — not just logic, but the user's own stated priorities

---

## `/init` — setup health check

when the user runs `/init`, asks "what now?", "am i set up?", "where do i start?", or similar: check the following in order and report status.

**1. vault symlinks**
do `~/tide/public/` and `~/tide/private/` exist and resolve correctly?

- if not: run `make install` from `~/code/tide/`

**2. VALUES.md**
is `~/tide/public/00-system/VALUES.md` hydrated — does it contain actual values, or just the stub template?

- if stub: this is the first thing to write. nothing in the system works without it.

**3. FAILURE-MODES.md**
is `~/tide/public/00-system/FAILURE-MODES.md` hydrated?

- if stub: write this second, alongside or immediately after VALUES.md.

**4. personal branches**
do `personal` branches exist on both repos?

```bash
git -C ~/code/tide branch -a | grep personal
git -C ~/code/tide-private branch -a | grep personal
```

- if not: `git checkout -b personal && git push -u origin personal` in each repo

**5. `make check`**
does `make check` pass on both repos?

- run from `~/code/tide/` and `~/code/tide-private/`

**6. inbox**
does `~/tide/private/inbox.md` have unprocessed captures?

- if yes: flag as pending for the next weekly reset

report what's done, what's missing, and a single clear next action. don't celebrate what isn't finished.

---

## operational modes

### vault mode (default)

the user is working with the vault — asking questions, making decisions, writing notes, processing inbox. apply the reasoning model. match the vault's tone: lowercase, first person, honest and non-performative.

### system mode

the user is making structural changes — schema updates, new templates, PRs to `main`. follow [REPO-MANAGEMENT.md](REPO-MANAGEMENT.md). run `make check` before any PR. for schema version bumps, run `make upgrade` to tag affected notes as `needs-review`. changes to `main` require a PR and squash merge.

---

## note and frontmatter rules

- every note needs the standard frontmatter block — see [SYSTEM.md §2](vault/00-system/SYSTEM.md)
- add `ai-assisted: true` to frontmatter on any note where Claude generated the initial draft
- never silently rewrite note content — tag for review, log the change
- `make check` = lint + frontmatter validation; run before any PR to `main`
- `make init` removes example files — run once after forking, while on the `personal` branch

---

## branch rules

| branch | rule |
|--------|------|
| `main` | schema, templates, system docs only. no personal data. PR required. |
| `personal` | live working content. direct push. never merges back to `main`. |

schema updates flow one direction: `main → personal` via `git merge main --no-ff`.

---

## per-folder context pattern

as the vault grows, add a `CLAUDE.md` to any subfolder to introduce domain-specific values and framing for that area. examples:

- `vault/40-projects/CLAUDE.md` — "when reviewing projects, weight completion and scope discipline"
- `vault/30-work/CLAUDE.md` — "work decisions filter through [specific professional values]"

these files are read in addition to — never instead of — VALUES.md and FAILURE-MODES.md.

---

## vault structure

```
~/tide/
  public/  (→ ~/code/tide/vault/)
    00-system/    values, failure modes, praxis, anxieties, system spec
    40-projects/  active projects, cross-domain
    50-knowledge/ reading, research, learning
    60-making/    craft documentation
    90-archive/   completed work
  private/  (→ ~/code/tide-private/vault/)
    10-self/      health and wellbeing
    20-family/    family
    30-work/      professional context
    inbox.md      capture inbox — processed weekly
```

folder weights and importance scoring: [SYSTEM.md §4](vault/00-system/SYSTEM.md).
