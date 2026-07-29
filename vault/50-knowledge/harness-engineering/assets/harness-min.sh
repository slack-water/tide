#!/usr/bin/env bash
# harness-min.sh — the smallest useful harness: trigger -> agent -> verify -> gate.
# Usage: ./harness-min.sh "fix the failing test in src/parser.ts" "npm test"
#
# Companion script for lessons/0002-anatomy-of-a-harness-workflow.html
set -euo pipefail

task="$1"
verify_cmd="${2:-npm test}"
max_attempts=3
run_id="$(date +%s)-$$"
run_dir="./harness-runs/${run_id}"
mkdir -p "$run_dir"
log_file="$run_dir/events.jsonl"

log() {
  jq -nc --arg ts "$(date -Iseconds)" --arg event "$1" --arg detail "$2" \
    '{ts:$ts, event:$event, detail:$detail}' >> "$log_file"
}

session_id=""
prompt="$task"

for attempt in $(seq 1 "$max_attempts"); do
  log "agent_start" "attempt $attempt"

  claude_args=(--bare -p "$prompt" --allowedTools "Read,Edit" --output-format json)
  [[ -n "$session_id" ]] && claude_args+=(--resume "$session_id")

  response="$(claude "${claude_args[@]}")"
  session_id="$(jq -r '.session_id' <<< "$response")"
  is_error="$(jq -r '.is_error' <<< "$response")"
  log "agent_result" "is_error=$is_error session=$session_id"

  if [[ "$is_error" == "true" ]]; then
    log "escalate" "agent call itself errored"
    echo "Agent call failed — escalating. Events: $log_file" >&2
    exit 1
  fi

  # Verification is deliberate and separate: a deterministic check the
  # harness runs itself, never the agent's own claim that it's done.
  if eval "$verify_cmd" > "$run_dir/verify-$attempt.log" 2>&1; then
    log "gate_pass" "verified on attempt $attempt"
    echo "Done — verified in $attempt attempt(s). Events: $log_file"
    exit 0
  fi

  log "gate_fail" "verification failed on attempt $attempt"
  prompt="Verification failed. Output:
$(tail -n 40 "$run_dir/verify-$attempt.log")
Fix it."
done

log "escalate" "exhausted $max_attempts attempts"
echo "Exhausted $max_attempts attempts — escalating to a human. Events: $log_file" >&2
exit 1
