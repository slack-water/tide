-- db-role-setup.sql
-- Run ONCE, by a human, with an admin credential. Never by an agent,
-- never as part of a harness run. This is a 12-factor admin process
-- (Factor 12) in its purest form: one-off, separate, disposable.
--
-- Companion to lessons/0003-gating-destructive-db-access.html

-- Nothing gets privileges by default.
REVOKE ALL ON SCHEMA public FROM PUBLIC;

-- A dedicated role for any harness/skill/agent that touches this database.
-- Never the app's own runtime user, never a superuser.
CREATE ROLE agent_readonly LOGIN PASSWORD :'agent_readonly_password';

GRANT CONNECT ON DATABASE app_db TO agent_readonly;
GRANT USAGE ON SCHEMA public TO agent_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO agent_readonly;

-- GRANT ... ON ALL TABLES only covers tables that exist right now.
-- Without this, a table created next week is invisible to REVOKE ALL
-- above but also unreachable by agent_readonly -- silently breaking
-- the agent's queries rather than silently widening its access, which
-- is the direction you want a misconfiguration to fail in.
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO agent_readonly;

-- Verify: this should return zero rows. If it doesn't, agent_readonly
-- can write, and nothing downstream in the harness will catch that.
-- SELECT grantee, table_name, privilege_type
-- FROM information_schema.role_table_grants
-- WHERE grantee = 'agent_readonly'
--   AND privilege_type NOT IN ('SELECT');
