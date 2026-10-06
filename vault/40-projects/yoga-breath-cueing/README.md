---
title: Yoga Breath-Cueing Tool
created: 2026-09-28
updated: 2026-09-29
folder: 40
type: project
status: active
importance: 3
goal: a breath-paced cue sequence for Surya Namaskara A that speaks breath, movement, and pose name in time with a slow in/out pattern
scope: surya A only, one tempo, cues on the breath — nothing else until it's been used once
tags: [yoga, teaching, audio, tts, making]
related: [ytt-overview]
schema-version: 1.0
ai-assisted: true
---

## Goal

Play Surya Namaskara A as a timed sequence where each movement lands on its own inhale or exhale, and the cue (breath, movement, pose name) is spoken inside that breath window. Something i can rehearse against while learning to teach, and maybe later run live.

## Scope

**In:** surya A. one sequence file. one adjustable breath tempo. breath tone + spoken cues. sanskrit/english toggle.
**Out (for now):** music, demo/video sync, other sequences, multiple voices, an app-store thing, anything that needs an account.

`later` items go in the inbox, not here — see [[FAILURE-MODES]] (scope creep, over-optimization spiral). the music idea is real (soul) but it's a second project.

## Done looks like

i run it, stand at the top of my mat, and it walks me through surya A at a slow tempo with nothing drifting: each pose change starts on the breath it belongs to, and the spoken cue finishes before the breath does. i use it in at least one real rehearsal before touching any of the out-of-scope list.

## Why this, why now

- **growth** — audio timing + TTS is a new-to-me domain, and it compounds into teaching craft (cueing is the Oct 17 topic; peer teach starts Nov 14).
- **vitality / soul** — it should serve embodied teaching, not replace it. the risk is a tool that makes me stare at a screen instead of breathing with the room.
- **watch:** the tooling is more fun than the teaching. if i've built more than i've rehearsed, stop and go teach it to an empty room once.

## Open question

rehearsal tool (for me, learning the rhythm) or live tool (students hear it)? changes everything about audio routing and voice choice. default assumption until decided: **rehearsal**.

## Design notes

**the core constraint:** a spoken cue has to fit inside its breath phase. at a slow tempo (~4s in / ~4s out) that's roughly 8–10 syllables at natural speech rate. "reach up — urdhva hastasana" fits. a full alignment cue doesn't. so cues need a short form (on the breath) and optionally a long form (held for the down-dog breaths, where there's time).

**data model — one row per breath phase:**

| field | example |
|---|---|
| `breath` | `in` / `out` / `hold` |
| `move` | "sweep the arms up" |
| `pose_sa` | Urdhva Hastasana |
| `pose_en` | upward salute |
| `quality` | optional — "long, smooth" |
| `beats` | override length in seconds (down dog holds) |

sequence is a JSON block embedded in `breath-cue.html` (a single file has to work from `file://` on a phone, so no fetching a separate yaml). it's editable in the page under "edit sequence", and steps can be reordered with the arrows; both save to the browser's local storage.

**draft sequence — verify against the YTT manual before trusting it.** this is the common Ashtanga-style count; the Alayah / Open to Grace version may differ (step vs jump, low-lunge variations, etc). ai-drafted.

| # | breath | pose | english | movement |
|---|---|---|---|---|
| 0 | — | Samasthitih / Tadasana | mountain | stand, feet together, ground |
| 1 | in | Urdhva Hastasana | upward salute | sweep arms up |
| 2 | out | Uttanasana | standing forward fold | fold, hands to floor |
| 3 | in | Ardha Uttanasana | half lift | lengthen spine |
| 4 | out | Chaturanga Dandasana | four-limbed staff | step/jump back, lower |
| 5 | in | Urdhva Mukha Svanasana | upward-facing dog | roll over, open chest |
| 6 | out | Adho Mukha Svanasana | downward-facing dog | lift hips back |
| — | 5 breaths | Adho Mukha Svanasana | downward-facing dog | hold |
| 7 | in | Ardha Uttanasana | half lift | step/jump forward |
| 8 | out | Uttanasana | standing forward fold | fold |
| 9 | in | Urdhva Hastasana | upward salute | rise, arms up |
| 10 | out | Samasthitih | mountain | hands to heart / sides |

**engine options (undecided, cheapest first):**

went with a single HTML page: `breath-cue.html`. Web Speech API for cues, Web Audio for the breath tone. no install, works on a phone. open it directly in a browser.

**tempo is in bpm, where 1 beat = 1 breath phase** (an inhale is a beat, an exhale is a beat). 15 bpm = 4s per phase = 7.5 full breaths/min. that keeps it compatible with music later.

**cue fit:** the page estimates how long each cue takes to say and shows measured time after a run; red = overran its breath. at 4s, sanskrit-only and english-only fit; "sanskrit, then english" overruns on four steps. default is sanskrit-only. the `CHARS_PER_SEC` constant is a guess to tune once measured.

**sanskrit pronunciation:** two layers. `say_sa` is an English-spelling respelling ("oordva hastasana") — used as the Web Speech fallback (browsers don't do SSML) and as the manifest lookup key. `ipa_sa` is a real IPA transcription ("ˈuːrd̪ʱʋɐ ɦɐˈst̪aːsɐnɐ") — used only when generating Polly audio, sent as an SSML `<phoneme>` tag. IPA gets dental/retroflex consonants, vowel length, and aspiration right in a way English spelling can't represent at all; it's a real improvement, not perfect — Polly maps the IPA onto Joanna's English phoneme inventory, so sounds with no English equivalent (retroflex stops, breathy voicing) get approximated to their closest English sound.

**recorded audio (AWS Polly):** `generate_audio.py` calls Polly for each unique cue and caches the mp3s in `audio/`, then writes a text→file manifest into `breath-cue.html` itself (a `<script id="audioManifest">` block, same pattern as the sequence). needs the AWS CLI configured (`aws configure` — this project never touches the credentials, just shells out). run it again after editing cue wording; unchanged text reuses its file, so only the changed cues get re-synthesized. **changing voice, engine, or an `ipa_sa` doesn't change the cache key** (it's keyed on the cue's visible text, not its pronunciation) — use `--force` to regenerate everything in those cases. cost is negligible — the full sequence is ~700 characters, well under a cent at neural rates.

this fixes the timing problem the char-count estimate couldn't: the page decodes each clip with the Web Audio API at load (not `<audio>`/`new Audio()` — that pipeline stalled in testing; `AudioContext.decodeAudioData` didn't) and uses its *real* duration as a floor on that breath phase, stretching the breath to let the cue finish rather than guessing. a step with no recorded audio (or a language mode you haven't generated) falls back to Web Speech exactly as before, so nothing regresses.

only sanskrit-only cues are generated by default (matching the page default). switching "pose names" to english or both will fall back to Web Speech until you run `generate_audio.py --lang en` (or `both`) too.

## Next action

- [ ] run it once for real: stand on the mat, do a full round with it, and write down what felt wrong (timing, voice, cue wording)

## Log

### 2026-09-29 (later, again)

removed the voice-select dropdown from the page — Joanna is decided (baked into the recorded audio via `generate_audio.py --voice`), and the dropdown only ever controlled the Web Speech *fallback* voice anyway. Web Speech still auto-picks a reasonable voice for un-recorded cues; there's just no UI to change it.

### 2026-09-29 (later)

switched sanskrit pronunciation from a plain-text respelling to real IPA via Polly's SSML `<phoneme>` tag. added `ipa_sa` per pose in the sequence; `generate_audio.py` now builds a plain-text version (still the manifest key + Web Speech fallback) alongside an SSML version with the phoneme tag (what's actually sent to Polly for the recorded clips). verified empirically before committing to it: confirmed Polly/Joanna neural honors phoneme overrides at all (an English "tomato" A/B test), then confirmed it doesn't choke on retroflex/breathy-voiced IPA symbols English doesn't have, before transcribing all 7 pose names. regenerated all 18 clips with `--force` (needed a new flag — the cache key is the cue's visible text, which pronunciation changes don't touch). confirmed by ear on 2 of 7 terms before the full regenerate; the other 5 use the same method, unverified.

also picked the voice: sampled Joanna/Ruth/Matthew/Kendra side by side, chose Joanna (staying with the original default).

### 2026-09-29

added AWS Polly audio: `generate_audio.py`, `audio/*.mp3` (18 clips, Joanna neural voice, sanskrit-only), and an embedded manifest in `breath-cue.html`. the page now measures each cue's real duration and stretches its breath to fit, instead of guessing from character count. also added reordering (↑/↓ on each step) and switched tempo to bpm (1 beat = 1 breath phase) per request.

hit one real bug along the way: `<audio>`/`new Audio()` never fired `loadedmetadata` in the browser-automation test environment (stuck at `loadstart`), while `AudioContext.decodeAudioData()` decoded the same file fine. switched cue playback to a Web Audio buffer source instead — one audio graph for tone and cues, and it sidesteps whatever that was. tested with a real mouse click (not just a synthesized `.click()`, which didn't count as a user gesture for the autoplay policy and left the context permanently `suspended`) — confirmed the context reaches `running` and the sequence plays through correctly.

still true: **not yet heard on an actual phone/speaker outside this test, and not yet used on a mat.**

### 2026-09-28 (later)

built `breath-cue.html`: surya A, bpm tempo, spoken cues + breath tone, rounds 1–5, reorderable steps, editable sequence json, per-cue fit check. tested logic in node and the page in a browser (no js errors); **not yet heard with a real voice or used on a mat.** the sequence is still an ai draft — verify against the YTT manual.

rehearsal-vs-live: decided rehearsal.

### 2026-09-28

project opened. drafted the surya A sequence and design constraints from the conversation. nothing built. sun salutes were covered in YTT week 1; cueing is Oct 17; first peer teach Nov 14 — that's the natural first real use.
