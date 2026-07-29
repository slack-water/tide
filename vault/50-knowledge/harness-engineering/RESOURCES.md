# Harness Engineering Resources

## Knowledge

- [Matt Pocock's skills repo](https://github.com/mattpocock/skills)
  Already familiar to Colin. Use for: concrete production skill examples, "small, sharp tools" design philosophy, the user-invoked vs. model-invoked split, `CLAUDE.md`/`SKILL.md` structure in the wild.
- [The Twelve-Factor App](https://12factor.net/)
  Canonical primary source, now community-maintained at [twelve-factor/twelve-factor](https://github.com/twelve-factor/twelve-factor). Use for: mapping factors (config, admin processes, disposability, logs, dev/prod parity, build/release/run) onto harness design.
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Anthropic
  Use for: progressive disclosure as the core skill-scoping principle, evaluation-driven skill design ("run on representative tasks, observe where they struggle"), safety guidance on trusted sources.
- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — Anthropic
  Use for: return-value design, actionable (non-traceback) error messages as a feedback-loop primitive, token efficiency, namespacing. Directly informs how a DB/CI skill should surface state back to the agent.
- [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic
  Use for: the workflow-vs-agent distinction, and the case for *not* adding agentic autonomy — relevant to backup/restore, where determinism should usually beat cleverness.
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
  Use for: `PreToolUse` / `PostToolUse` / `Stop` / `SubagentStop` mechanics as the concrete enforcement layer (quality gates) in Claude Code specifically. Note: subagents do not automatically inherit the main agent's permissions — a `PreToolUse` hook may be the only thing gating a subagent's tool calls.
- [Harness Engineering for AI Coding Agents](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) — Augment Code
  **Anchor source for this course.** Defines the three-layer model this workspace teaches from: Constraint Harnesses (feedforward), Feedback Loops (corrective), Quality Gates (enforcement). Core thesis: "Humans steer. Agents execute" — reliability comes from deterministic constraints, not probabilistic compliance.
- [What makes a harness a harness](https://arxiv.org/abs/2606.10106) (arXiv 2606.10106)
  Use for: a precise, defensible definition of "agent harness" and an inclusion/exclusion test distinguishing it from frameworks, SDKs, orchestrators, and evaluation scaffolds. Worth reading in full — the abstract undersells the taxonomy.
- [Google SRE Book — Managing Incidents](https://sre.google/sre-book/managing-incidents/)
  Use for: incident roles (Incident Commander / Comms Lead / Ops Lead), runbook design principles, postmortem culture. Direct input to the CI-debugging and DB-incident skills.
- [Google SRE Workbook — Incident Response](https://sre.google/workbook/incident-response/)
  Use for: practical incident-response walkthroughs and escalation paths, more concrete than the SRE book chapter above.

## Gaps

- No single high-trust source yet on backup/restore-specific engineering discipline (3-2-1 rule, restore-testing discipline, RPO/RTO framing). Needs sourcing before that lesson is built.
- No high-trust source yet specifically on CI/CD debugging methodology for agents — likely synthesized from SRE incident response + twelve-factor's build/release/run separation rather than a single source.

## Wisdom (Communities)

Not yet discussed with Colin — revisit once the first skill is built and there's something real to get feedback on.
