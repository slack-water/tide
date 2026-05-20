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

FAILURE-MODES.md is the second document Claude reads when helping you with a decision, after VALUES.md. Together they form the upstream context for everything else.

A failure mode is a named, recurring pattern — a place where you consistently get stuck, spiral, or self-sabotage. It is not a character flaw and not aspirational. It is an observation about how you actually behave under specific conditions.

**A failure mode is only useful if it's specific enough to recognize in the moment.** "I procrastinate" is not useful. "When a project feels underspecified, I research adjacent tools instead of asking for clarity" is useful.

Each entry needs four things to be protective:

1. **Visible** — you can see yourself in it *before* it's too late. The early signals are the most important part of the entry.
2. **Costly** — ignoring it has a real consequence you care about. Name the cost specifically.
3. **Redirectable** — there is a concrete alternative action when you spot the signal.
4. **Accountable** — there is a mechanism to enforce the redirect, not just an intention.

**Failure modes are often values in conflict.** When you notice a pattern, ask: which two values are pulling in opposite directions here? Naming the conflict is often more useful than describing the behavior alone.

**Relationship to PRAXIS.md:** PRAXIS.md has a "known failure modes" section. Keep that as a brief summary and point here for the full structured treatment.

Use this template for each entry:

```markdown
## [failure mode name]

**the pattern:** [what it looks like when it's fully activated]
**early signals:** [observable signs you can catch before it's too late — be specific]
**the cost:** [what this actually costs you — name it concretely]
**redirect:** [the specific alternative action to take when you spot a signal]
**accountability:** [how you enforce the redirect — a rule, a person, a trigger]
**values in conflict:** [which values are pulling against each other here]
```

---

## example entries

---

## the over-optimization spiral

**the pattern:** i spend time improving the system that's supposed to help me do the thing, instead of doing the thing. the system becomes the project. this happens with productivity tools, note-taking setups, workflows, and code architecture.

**early signals:**

- i've opened a config file or settings panel more than twice in a session
- the last several commits are to infrastructure, not content
- i'm excited about a refactor no one asked for
- i've spent more time on the inbox than processing what's in it

**the cost:** the actual work doesn't happen. the system grows, the output doesn't. i mistake motion for progress and feel productive while producing nothing.

**redirect:** close the tool. open the document, the conversation, or the task the system was built to support. do one unit of real output before returning to configuration.

**accountability:** if i catch the signal, i owe myself 25 minutes of real output before any system work. no exceptions logged as "just a quick fix."

**values in conflict:** craft (the system should be right) vs. output (the work should ship). craft loses when it consumes the output it was supposed to serve.

---

## avoidance via reframing

**the pattern:** i avoid difficult conversations — with colleagues, collaborators, family — by convincing myself the moment isn't right yet. i reframe the avoidance as patience, strategic timing, or "waiting for more information." the conversation never quite becomes necessary enough to have.

**early signals:**

- i've had the same thought about needing to say something more than twice
- i'm framing a hard thing as "not yet urgent"
- i'm researching how to have the conversation instead of having it
- i feel relief when circumstances delay the opportunity

**the cost:** the thing that needed to be said compounds. small misalignments become structural problems. relationships drift. i also lose trust in myself as someone who acts on what i know.

**redirect:** name it out loud or in writing: "i am avoiding [specific conversation] because [actual reason]." once named, set a specific window — not "soon," but "before [date/event]."

**accountability:** if i've caught myself in this pattern, i tell one person i trust what i'm avoiding and when i've committed to doing it. the commitment is the mechanism, not the intention.

**values in conflict:** honesty (say the true thing) vs. harmony (preserve the peace). honesty is upstream — letting harmony override it here has compound costs.
