---
title: Failure Modes — example
created: 2026-05-17
updated: 2026-05-17
folder: 00
type: template
status: active
importance: 3
schema-version: 1.0
---

# Failure Modes — example

*This file shows what a hydrated FAILURE-MODES.md looks like. Delete it with `make init` when you're ready to write your own.*

---

## how to write this

FAILURE-MODES.md is read alongside VALUES.md. Failure modes are often values in conflict — knowing both tells you not just what went wrong, but why.

An entry is only useful if it's **specific enough to recognize yourself in** and **costly enough that you care**. Vague tendencies don't count. Named patterns with early signals do.

For each entry:

- **the pattern:** what the behavior looks like from the outside
- **early signals:** what you notice first — before it's too late to redirect
- **the cost:** what actually suffers when you stay in this pattern
- **the redirect:** the specific thing to do when you catch the signal
- **accountability:** an observable check — something you (or someone else) can actually measure

```markdown
## [name the pattern]

**the pattern:** [what the behavior looks like — specific, not vague]

**early signals:**
- [what you notice first]
- [another early signal]

**the cost:** [what actually suffers — the real consequence you care about]

**the redirect:** [the specific action to take when you catch the signal]

**accountability:** [an observable check — something you can measure]
```

Add new entries at the top. Newest first.

---

## example

---

## conflict avoidance by reframing

**the pattern:** avoiding a difficult conversation by convincing yourself it isn't necessary yet. the other person doesn't know there's a problem, so the cost stays invisible — until it isn't.

**early signals:**

- the same thought has surfaced more than twice without being said
- planning what you'd say, but not saying it
- relief when circumstances delay the conversation

**the cost:** trust degrades on both sides. the eventual conversation is harder than the one that was avoided.

**the redirect:** say the thing. not perfectly — just enough to make it real. the first sentence is the hardest part.

**accountability:** if a thought has surfaced three times without being said, it needs to be said. today, not when conditions improve.
