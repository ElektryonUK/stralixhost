# Stralix Cloud Panel/Agent - Tasks Backlog

This document tracks remaining work for the cPanel-like control panel and node agent.

## Phase 1 – Control Plane foundations
- [ ] Nodes registry API (CRUD): store agent_url, roles/capabilities, trust_state, cert refs
- [ ] AgentClient integration in websites/provision (call /v1/vhosts)
- [ ] Task model + lifecycle (queued, running, failed, success) with retries/backoff
- [ ] Audit middleware (panel-backend): log actor, action, target, request-id
- [ ] RBAC gates on all panel routes (customer/staff/admin + org_id scoping)

## Phase 2 – Agent Nginx adapter (MVP websites)
- [ ] Render vhost from template (HTTP/HTTPS) with ACME location
- [ ] configtest, enable site (symlink), reload nginx
- [ ] Rollback to previous config on failure (backup and restore)
- [ ] Return detailed status (stdout/stderr), timings, checks

## Phase 3 – SSL / ACME
- [ ] http-01 issuance with certbot; install certs into vhost
- [ ] Renewal hooks; expiry monitoring
- [ ] dns-01 provider integration (Cloudflare/PowerDNS) – design + stubs

## Phase 4 – Databases
- [ ] MySQL/MariaDB: create db, user, grants; delete/rotate
- [ ] PostgreSQL: create db, role, grants; delete/rotate
- [ ] Panel CRUD and wiring to agent methods

## Phase 5 – DNS
- [ ] Local BIND/PowerDNS integration – zone create/update/remove
- [ ] Cloudflare provider integration on panel (optional)
- [ ] Zone templates and validation

## Phase 6 – Email (Postfix/Dovecot)
- [ ] Create mailbox, alias; set quota
- [ ] Update virtual maps; reload services
- [ ] Spam/AV integration plan

## Phase 7 – FTP/SFTP & Cron
- [ ] FTP/SFTP users (vsftpd/proftpd/system users) with chroot
- [ ] Cron jobs under /etc/cron.d with validation

## Phase 8 – Observability & Security
- [ ] Request-ID propagation panel↔agent; structured JSON logs
- [ ] Prometheus/OTEL exporters plan
- [ ] mTLS hardening (internal CA, SAN checks, rotation automation)
- [ ] JWT move to RS256/ES256 with key rotation and KMS/Vault
- [ ] Firewall rules guidance and provisioning scripts

## Phase 9 – Frontend (panel-frontend)
- [ ] Websites module UI (create, edit, suspend, delete)
- [ ] Nodes screen (status, roles, capabilities)
- [ ] SSL dashboard with expiry warnings
- [ ] Audit log viewer with filters
- [ ] DNS/DB/Email/FTP/Cron UIs (stubs → full)

## Phase 10 – Infrastructure & Ops
- [ ] Systemd units for panel-backend and agent (TLS/mTLS examples)
- [ ] Nginx upstream configs (reverse proxy with TLS)
- [ ] Provisioning scripts (Ansible) for new nodes
- [ ] Secrets management strategy (Vault/KMS) and env templates

## Stretch goals
- [ ] Message bus for tasks (Redis/Celery or Kafka) and saga patterns
- [ ] GitOps for node config (commits for vhost/dns changes with rollback)

---

All work must follow INSTRUCTIONS.md and INSTRUCTIONS_PANEL_AGENT.md.
