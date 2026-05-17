# tide — AI context and prompt architecture

This file tells Claude how to work with this vault. Read it before anything else.

---

## what this system is

tide is a **decision-support engine**. it is not a life OS or a PKM system. the vault is structured so that your values, failure modes, and decision-making framework are first-class, queryable objects that an AI can reason about.

the two upstream documents are:

- [`vault/00-system/VALUES.md`](vault/00-system/VALUES.md) — what you actually optimize for
- [`vault/00-system/FAILURE-MODES.md`](vault/00-system/FAILURE-MODES.md) — where you get stuck

**always read both before doing anything else.**

---

## decision-support prompt

use this pattern when the human asks for help thinking through a decision:

```
1. here are my values [VALUES.md — read it]
2. here are my known failure modes [FAILURE-MODES.md — read it]
3. here is the decision i'm facing [the human's current context]
4. here is relevant history [related notes, past decisions — if provided]
given all that, help me think through this.
```

**the job is to reason about the decision through the lens of the human's actual values**, not to give generic advice. if VALUES.md is empty or thin, say so — the answer will only be as good as what's there.

when a failure mode is directly relevant to the decision at hand, name it explicitly. don't be subtle about it.

---

## structure

the vault schema is defined in [`vault/00-system/SYSTEM.md`](vault/00-system/SYSTEM.md). for any structural or schema-related task, read that first.

key rules:

- all content lives in `.md` files with valid YAML frontmatter
- `status: needs-review` is how schema changes propagate — tag, don't rewrite
- AI-assisted notes should include `ai-assisted: true` in frontmatter
- content generation: produce drafts, human approves before commit

---

## working with this vault

**for a decision:** read VALUES.md and FAILURE-MODES.md, then apply the prompt architecture above.

**for a schema change:** read SYSTEM.md §3, log the change in SCHEMA-CHANGELOG.md, run `scripts/schema-upgrade.py` to tag affected notes, do not silently rewrite content.

**for content work:** follow the frontmatter schema in SYSTEM.md §2. run `make check` before opening a PR.

**for anything structural:** human owns the structure. AI flags and proposes; human decides.
