#!/usr/bin/env bash
# db-readonly-guard.sh — the soft layer of a two-layer DB gate.
# Source this; it exports db_query(), the only way any script that
# sources it can touch the database.
#
# The REAL gate is not in this file. It's whatever role DB_READONLY_URL
# authenticates as — see reference/db-role-setup.sql. That role has no
# write grants at all, enforced by the database engine itself. This
# wrapper adds a cheap client-side fast-fail on top of that — never
# the other way around. See lessons/0003-gating-destructive-db-access.html
# for why the order matters (a regex-only defense here would be the
# CVE-2026-54760 mistake, not a fix for it).
set -euo pipefail

: "${DB_READONLY_URL:?Set DB_READONLY_URL to a connection string for a SELECT-only role}"

db_query() {
  local sql="$1"

  # Fast-fail heuristic. Deliberately naive — this is NOT the security
  # boundary, just a cheap early exit so an obvious mistake fails in
  # milliseconds instead of round-tripping to the network. A cleverly
  # obfuscated write can slip past this line; it cannot slip past the
  # database's own permission check below. (nocasematch matters here —
  # without it this check silently misses "delete from users" because
  # bash regex doesn't case-fold by default. Tested; it really doesn't.)
  shopt -s nocasematch
  if [[ "$sql" =~ ^[[:space:]]*(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|GRANT|REVOKE|CREATE)[[:space:]] ]]; then
    shopt -u nocasematch
    echo "db_query: rejected client-side — this wrapper only issues reads." >&2
    return 1
  fi
  shopt -u nocasematch

  # The real gate: agent_readonly has no write grants, full stop.
  # Even a write statement that evades the check above is rejected by
  # Postgres itself with a permission error, because that's a fact
  # about the credential, not a decision this script makes.
  psql "$DB_READONLY_URL" -v ON_ERROR_STOP=1 -t -c "$sql"
}
