#!/usr/bin/env bash
# harness-durable.sh — a harness whose state survives its own process exit.
# Usage: ./harness-durable.sh [--dry-run]
#
# Companion script for lessons/0004-state-that-outlives-the-loop.html
#
# Shape:  human edits a staged draft
#           -> agent formats it and publishes (commit + push)
#           -> verification decides whether the draft is cleared or kept
#
# The staged draft and the run state are deliberately NOT temp files, and
# there is deliberately no cleanup trap. They outlive a failed run so that
# neither the human's input nor the cost accounting is lost to a process
# that exited early.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Config from the environment (Twelve-Factor III), with workable defaults.
TEMPLATE="${HARNESS_TEMPLATE:-entry_TEMPLATE.md}"
INSTRUCTIONS="${HARNESS_INSTRUCTIONS:-entry_INSTRUCTIONS.md}"
TARGET_DOC="${HARNESS_TARGET:-entries.md}"

# Durable state — tier three. Both belong in .gitignore. Both are removed
# only after a verified publish, and never anywhere else.
STAGED_DRAFT="$SCRIPT_DIR/.harness-draft.md"
STAGED_STATE="$SCRIPT_DIR/.harness-draft.state.json"

dry_run=false
[[ "${1:-}" == "--dry-run" || "${1:-}" == "-n" ]] && dry_run=true

for f in "$TEMPLATE" "$INSTRUCTIONS" "$TARGET_DOC"; do
  [[ -f "$f" ]] || { echo "missing required file: $f" >&2; exit 1; }
done

# ---------------------------------------------------------------- state load
EMPTY_STATE='{"attempts":0,"duration_ms":0,"total_cost_usd":0,"num_turns":0,
  "usage":{"input_tokens":0,"output_tokens":0,
           "cache_read_input_tokens":0,"cache_creation_input_tokens":0},
  "session_id":null}'

if [[ -f "$STAGED_STATE" ]]; then
  prior_state="$(cat "$STAGED_STATE")"
else
  prior_state="$EMPTY_STATE"
fi

# Stored in tier three; points at tier two. Empty means "no prior session."
prior_session_id="$(jq -r '.session_id // empty' <<<"$prior_state")"

# ------------------------------------------------------------------- trigger
# A leftover draft means the last run did not publish. Reopen the human's own
# words rather than a blank template, so nothing is ever retyped.
if [[ -f "$STAGED_DRAFT" ]]; then
  printf 'Resuming staged draft (%s prior attempt(s), $%.2f spent so far)\n' \
    "$(jq -r '.attempts' <<<"$prior_state")" \
    "$(jq -r '.total_cost_usd' <<<"$prior_state")" >&2
else
  cp "$TEMPLATE" "$STAGED_DRAFT"
fi

# vipe opens $EDITOR on stdin and emits the edited buffer on stdout. Write to
# a sibling path and mv into place: rename is atomic, so an editor or shell
# that dies mid-write cannot leave a truncated draft behind.
vipe < "$STAGED_DRAFT" > "${STAGED_DRAFT}.new"
mv "${STAGED_DRAFT}.new" "$STAGED_DRAFT"

# --------------------------------------------------------- context decision
# Retain or discard. Resuming keeps the agent's own reasoning about what it
# rejected last time; a fresh session re-reads the instructions from scratch.
# Resume for continuity, not for cost -- see the lesson.
if [[ -n "$prior_session_id" ]]; then
  prompt="Retry of the same entry. An earlier attempt in this session did not
publish -- see the conversation history for what was missing. The corrected
draft follows; apply the same instructions and try again."
  resume_args=(--resume "$prior_session_id")
else
  prompt="$(cat "$INSTRUCTIONS")"
  resume_args=()
fi

if [[ "$dry_run" == true ]]; then
  prompt="DRY RUN: draft the entry and output it. Do not write, commit, or push.

$prompt"
  allowed_tools="Read"
else
  allowed_tools="Read,Edit,Write,Bash(git add:*),Bash(git commit:*),Bash(git push:*)"
fi

# missing_fields makes a gate failure legible to the human, not just to the
# script -- the same principle as returning legible observations to an agent.
schema='{"type":"object","properties":{
  "entry":{"type":"string"},
  "missing_fields":{"type":"array","items":{"type":"string"}},
  "published":{"type":"boolean"}},
  "required":["entry","missing_fields","published"]}'

# ---------------------------------------------------------------- agent loop
# --allowedTools is re-passed on every run: permission *mode* is documented to
# restore across --resume, tool allowlists are not. Never let a permission set
# silently change on retry.
#
# "${resume_args[@]+"${resume_args[@]}"}" -- not the obvious "${resume_args[@]}".
# Under `set -u`, bash 3.2 (still /bin/bash on macOS) treats an empty array
# expansion as an unbound variable and aborts the run. That failure only shows
# up on the fresh-session path, which is exactly the one a resume test skips.
output="$(claude -p "$prompt" \
  "${resume_args[@]+"${resume_args[@]}"}" \
  --output-format json \
  --json-schema "$schema" \
  --allowedTools "$allowed_tools" \
  < "$STAGED_DRAFT")"

published="$(jq -r '.structured_output.published' <<<"$output")"

# ---------------------------------------------------------------- accounting
# The headless docs are explicit that cost/usage describe THIS invocation.
# They do not accumulate across --resume, so summing is the caller's job:
# without this, a task that succeeded on attempt three reports only attempt
# three's cost. session_id is carried, not summed -- it is an address, not a
# metric.
state="$(jq -n --argjson prev "$prior_state" --argjson cur "$output" '{
  attempts:       ($prev.attempts       + 1),
  duration_ms:    ($prev.duration_ms    + $cur.duration_ms),
  total_cost_usd: ($prev.total_cost_usd + $cur.total_cost_usd),
  num_turns:      ($prev.num_turns      + $cur.num_turns),
  usage: {
    input_tokens:                ($prev.usage.input_tokens                + $cur.usage.input_tokens),
    output_tokens:               ($prev.usage.output_tokens               + $cur.usage.output_tokens),
    cache_read_input_tokens:     ($prev.usage.cache_read_input_tokens     + $cur.usage.cache_read_input_tokens),
    cache_creation_input_tokens: ($prev.usage.cache_creation_input_tokens + $cur.usage.cache_creation_input_tokens)
  },
  session_id: $cur.session_id
}')"

jq -r '.structured_output.entry' <<<"$output"
echo

# ------------------------------------------------------------ gate & cleanup
# Cleanup is the LAST thing that happens, and only on a verified publish.
# Deleting the draft any earlier trades a retryable failure for a lost entry.
if [[ "$dry_run" == true ]]; then
  echo "Dry run — draft and state left untouched." >&2
elif [[ "$published" == true ]]; then
  rm -f "$STAGED_DRAFT" "$STAGED_STATE"
  echo "Published. Draft cleared." >&2
else
  echo "$state" > "$STAGED_STATE"
  echo "Not published — draft kept at $STAGED_DRAFT (resumes on next run)." >&2
  jq -r '.structured_output.missing_fields[]? | "  missing: \(.)"' <<<"$output" >&2
fi

printf 'Attempts %s · turns %s · cost $%.2f (cumulative across attempts)\n' \
  "$(jq -r '.attempts' <<<"$state")" \
  "$(jq -r '.num_turns' <<<"$state")" \
  "$(jq -r '.total_cost_usd' <<<"$state")" >&2
