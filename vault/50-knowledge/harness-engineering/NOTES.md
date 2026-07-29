# Notes

## Preferences
- Dual context: personal tooling (tide, other solo repos) now, team standard later. Lessons can gesture at both but don't need to design for team rollout yet — see MISSION.md "Out of scope."
- Skill/subagent/hook mechanics already known. Never re-teach frontmatter syntax, `/skill` invocation, tool permission basics — that's floor, not ceiling.
- Explicitly wants *deep* learning — resist superficial how-to framing. Every lesson should ground claims in a cited primary source, not just assert best practice.
- PDF export: batched, not per-lesson. Run `./export-pdf.sh` periodically; don't build auto-export hooks.
- Reading device is a ReMarkable tablet (e-ink) — style.css print rules force light background / high contrast regardless of screen color scheme.

## Workspace mechanics
- `./export-pdf.sh` uses headless Chrome (`/Applications/Google Chrome.app`) to print each `lessons/*.html` and `reference/*.html` to `./pdf/`. One PDF per file — ReMarkable handles a folder of separate docs fine, no need to merge.
- Quiz pattern: `<details>` / `<summary>` with a print override in `assets/style.css` (`details:not([open]) > *:not(summary) { display: block !important }`) so answers stay collapsed on screen (real retrieval practice) but render open in the PDF (useful as a read-later reference).
