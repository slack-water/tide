# Mission: Harness Engineering

## Why
Colin wants to design and build a small set of production-grade Claude Code skills/subagents ("harnesses") for four operational activities — CI debugging, database monitoring/resolution, backup/restore, and feature development — that are safe enough to trust with real blast radius (broken CI, live databases). The mechanics of writing skills/subagents/hooks are already known; the gap is applying real engineering discipline (twelve-factor, SRE practice) so these harnesses are reliable rather than vibes-based. Useful now for personal repos (e.g. tide), solid enough to become a team standard later.

## Success looks like
- Can explain, from first principles, why a given skill/subagent design is safe or unsafe for a specific activity — citing a specific twelve-factor factor or SRE practice as justification, not just intuition
- Has designed a harness architecture for each of the four target activities, each explicitly addressing: blast-radius/permission scoping, idempotency/retries, observability (structured logs/output), and a rollback or escalation path
- Can look at an existing skill (Matt Pocock's or their own) and correctly classify its safety properties — identifying what's missing before it's trusted with production ops
- Has built and dry-run at least one real skill end-to-end in tide or another repo

## Constraints
- Sessions are short, one tightly-scoped lesson at a time — deep learning, not tutorial-following
- Skill/subagent/hook mechanics are already known — no lesson time on frontmatter syntax or "what is a skill" basics
- Primary content (lessons + reference docs) must render cleanly to PDF for offline reading on a ReMarkable tablet — print-friendly, high-contrast, serif-based layout takes priority over screen-only flourishes
- PDF export happens in batches, run periodically by Colin — no need for automatic per-lesson export

## Out of scope
- Team rollout / adoption process itself (org change management, training others) — revisit once personal patterns are proven
- Twelve-factor topics unrelated to harness design (containerization mechanics, port binding, concurrency/scale-out)
- Claude Code skill/subagent/hook mechanics 101 (already known — see [[0001-prior-skill-baseline]])
