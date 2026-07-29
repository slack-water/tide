# Prior skill baseline established at mission setup

Colin is already comfortable with Claude Code skill/subagent/hook mechanics (writing `SKILL.md` files, wiring subagents, registering hooks) and familiar with Matt Pocock's skills repo. He has not yet grounded the twelve-factor app specifically for this purpose. This sets the floor: lessons should never reteach mechanics or basic skill syntax — the zone of proximal development starts at applying engineering discipline (reliability, blast-radius scoping, idempotency, observability) to harness design, not at "how do I write a skill."

**Evidence:** Stated directly in response to setup questions — "Comfortable with mechanics of skills/subagents, want the engineering discipline" and "familiar" with Matt Pocock's repo but not flagged as familiar with 12-factor.

**Implications:** Future lessons on CI debugging, DB ops, backup/restore, and feature development should assume the mechanics and jump straight to the safety/reliability design questions specific to that activity's blast radius.
