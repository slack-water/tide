# tide — core priorities

> this document exists to keep the system honest about what it actually is.
> when in doubt about what to build next, start here.

---

## what tide actually is

tide is a **decision-support engine**.

not a life OS. not a PKM system. not a forkable template for strangers.

a system where your values, failure modes, and decision-making framework are first-class, queryable objects that you can ask AI to reason about in real time.

---

## the three priorities, in order

### 1. VALUES.md — the constitution

this is the upstream document. nothing else in the system matters without it.

values are not aspirational statements. they are the actual things you optimize for when you make decisions — including when you don't realize you're making one.

**VALUES.md must be:**

- written before anything else is relied upon
- weighted (not all values are equal)
- honest (what you actually optimize for, not what you wish you did)
- queryable (AI reads this first, every time)

**when you ask Claude a question using this system, VALUES.md is always the first context passed.**

---

### 2. FAILURE-MODES.md — the constraints

these are the places where you get stuck, spiral, or self-sabotage. they are not character flaws — they are known patterns with early signals and named costs.

a failure mode is only protective if it is **visible** and **costly**:

- visible means you can see yourself in it before it's too late
- costly means ignoring it has a real consequence you care about

**FAILURE-MODES.md must be:**

- specific (named patterns, not vague tendencies)
- actionable (each entry has a redirect and an accountability mechanism)
- updated as new patterns are identified
- read alongside VALUES.md — failure modes are often values in conflict

**when you ask Claude a question using this system, FAILURE-MODES.md is always the second context passed.**

---

### 3. everything else — supporting context

projects, knowledge, logs, work notes, making documentation — all of it is context. useful, sometimes essential, but always subordinate to values and failure modes.

the weight of context in any AI query should be proportional to its proximity to values. a note in 10-Self carries more weight than a note in 90-Archive. the folder weighting system in SYSTEM.md encodes this.

**the prompt architecture for any decision:**

```
1. here are my values [VALUES.md]
2. here are my known failure modes [FAILURE-MODES.md]
3. here is the decision i'm facing [current context]
4. here is relevant history [related notes, past decisions]
given all that, help me think through this.
```

---

## what this means for what to build next

in order:

1. **write VALUES.md** — nothing else functions without this
2. **write FAILURE-MODES.md** — the over-optimization spiral entry is already there; add others as you find them
3. **build a Claude prompt that reads both and helps with a real decision** — test it on one actual decision before adding any infrastructure
4. **build the schema upgrade tool** — only after the above three are working
5. **build CLAUDE.md** — the prompt and context-passing pattern that makes this repeatable

---

*the system works when you use it on yourself first.*
*prove it on one real decision. then iterate.*
