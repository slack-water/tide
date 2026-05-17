# philosophy

tide is a **decision support engine**. not a life OS, not a productivity system, not a note-taking app.

the problem it solves: most decisions go wrong not because of missing information, but because the reasoning frame is wrong. you optimize for the wrong thing, or you follow a known pattern you didn't catch in time. tide addresses both.

---

## how it works

**values** are what you actually optimize for when you make decisions — including when you don't realize you're making one. not aspirational statements. the real things. specific enough that you could make a decision with them.

**failure modes** are the patterns where you get stuck, spiral, or self-sabotage. not character flaws — behavioral patterns with early signals and known costs. the over-optimization spiral (building the system instead of using it) is a common one. conflict avoidance, urgency bias, and analysis paralysis are others. yours are specific to you.

these two documents are upstream of everything else in the vault. everything else is context. context is useful; it is subordinate to values and failure modes.

---

## the decision prompt

when you face a real decision:

1. here are my values
2. here are my known failure modes
3. here is the decision i'm facing
4. here is relevant context

*given all that, help me think through this.*

the goal is not to make decisions for you. it is to make sure that when you decide, you're deciding as the person you actually want to be — not the one your habits or anxieties are pulling you toward.

---

## the files

everything in tide is plain markdown — text files with light formatting. no proprietary format, no lock-in. when the tools change (and they will), the files remain.

every note carries **frontmatter**: a small block of structured metadata at the top of each file. it looks like this:

```yaml
---
title: My Note
created: 2026-05-01
type: note
status: active
importance: 3
schema-version: 1.0
---
```

frontmatter is what makes notes queryable. an AI can read it and understand which notes are most relevant to a decision without you having to curate the whole vault by hand. it also makes the system inspectable: you can see exactly what the system knows about a note.

---

## on scale

at the personal level this is three files and a prompt. the same architecture scales — governance principles replacing values, institutional failure patterns replacing personal ones — but that is not the primary goal. the primary goal is to be useful to one person on one real decision. the architecture just happens to compose.

---

**markdown is the contract.** the app is a viewport. optimize for the files, not the tool that opens them.
