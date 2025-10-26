# STRALIXHOST - AI DEVELOPMENT INSTRUCTIONS (Panel/Agent Extension)

This section extends the monorepo rules for the new control panel and node agent components.

## Modules Added
- panel-frontend/: Next.js App Router UI for the control panel
- panel-backend/: FastAPI control plane (RBAC, audit, orchestration, agent communication)
- agent/: Lightweight FastAPI node agent (vhost, DNS, mail, DB, SSL, FTP/SFTP, cron)
- infrastructure/: Nginx/DNS templates, provisioning scripts
- shared/: Shared Pydantic schemas, auth utils, agent client contracts

## Security & Networking
- Mutual TLS (mTLS) MUST be used for Panel ↔ Agent traffic in production.
  - Issue internal CA and per-service certificates; enforce SAN hostname checks; rotate certs.
  - Additionally sign each request with short-lived JWT (audience=node_id, action, expires ≤ 5m).
- Restrict agent ports via firewall to Panel IPs only. Prefer private interfaces/VPN.
- RBAC: customer, staff, admin. Scope every operation by org_id and ownership.
- Audit logging: Every mutating action MUST write a structured audit event.

## Rate Limiting & Abuse Prevention
- Public auth endpoints: keep RATE_LIMIT_* controls (already implemented in backend).
- Agent endpoints: rate-limit and require both mTLS and JWT.

## Tasks & Rollback
- All provisioning is idempotent. Agents must:
  - Stage config files, run configtest, then activate.
  - Backup previous state and roll back on failure.
- Panel records task lifecycle (queued, running, failed, success) and retries with backoff.

## Observability
- Propagate Request-ID across Panel and Agent.
- Use structured JSON logs. Plan for Prometheus/OTEL exporters.

## Templates & ACME
- Nginx vhost templates stored under infrastructure/nginx/templates.
- ACME http-01 challenges via /.well-known/acme-challenge/ and cert install into vhost.
- Support dns-01 in future (Cloudflare/PowerDNS).

## Coding Standards
- Production-only builds and configurations.
- SQLAlchemy: wrap raw SQL with text().
- No secrets committed. Update backend/.env.example and panel-backend env templates when adding variables.
- Follow conventional commits and push immediately.

## Next Implementation Steps
1. Agent client in panel-backend (mTLS + JWT) and wire /websites/provision to POST /v1/vhosts on agent.
2. Add nodes registry API in panel-backend; store agent_url, node roles/capabilities, trust state.
3. Implement nginx adapter in agent: write vhost from template, configtest, enable, reload, rollback.
4. Add audit logging middleware in panel-backend; write events for all mutating routes.
5. Provide systemd unit examples and Nginx upstreams for panel-backend and agent behind TLS.
