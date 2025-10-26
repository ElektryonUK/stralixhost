# Stralix Cloud Monorepo - Panel/Agent scaffold

This scaffolds the control plane (panel) and data plane (agent) for a modern cPanel alternative.

## Modules
- panel-frontend/ (Next.js UI)
- panel-backend/ (FastAPI control plane)
- agent/ (FastAPI node agent)
- infrastructure/ (templates and scripts)
- shared/ (schemas and clients)

Follow INSTRUCTIONS.md rules: production builds, SQLAlchemy text() for raw SQL, no secrets in repo.
