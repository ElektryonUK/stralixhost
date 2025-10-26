# STRALIXHOST - AI DEVELOPMENT INSTRUCTIONS

This file contains the comprehensive instructions and requirements for developing the Stralixhost project. Any AI assistant working on this project should follow these guidelines precisely.

## PROJECT OVERVIEW

**Stralixhost** is a monorepo for a full-stack hosting platform (web hosting, VPS, game servers, domains, SSL). This phase focuses on secure user management, hardened APIs, and production-grade deployments.

## CORE REQUIREMENTS

### 1. REPOSITORY STRUCTURE
- **Monorepo architecture** with clear separation between frontend, backend, database, scripts, and docs.
- **Security-first** design: never commit secrets, follow the env template, enforce CI checks.

### 2. FRONTEND REQUIREMENTS
- **Next.js (App Router)** with TypeScript, CSS Modules (no Tailwind).
- **Auth-aware header**: shows Login/Register for guests; shows user avatar/name with account/logout for authenticated users.
- **Auth pages**: login, register, verify email, forgot/reset password, account security (2FA).

### 3. BACKEND REQUIREMENTS
- **FastAPI** with JWT/session auth, bcrypt (or Argon2), TOTP 2FA, email verification, password reset.
- **Role-based access control**: customer, staff, admin.
- **Security logging**: login failures, password resets, role/status changes, 2FA events.
- **Rate limiting** on auth endpoints via middleware or Nginx/proxy.

### 4. DATABASE & MIGRATIONS
- PostgreSQL on an external server.
- Use migration files under `database/migrations/` with incremental numeric versions (e.g., `001_`, `002_`).
- A migration runner script is provided: `scripts/db_migrate.sh` (psql-based). Use `DATABASE_URL` env.
- Always update the main schema and write a new migration for any structural change.

### 5. ENVIRONMENT CONFIGURATION
- Maintain `backend/.env.example` with all required keys. Update it whenever new constants are introduced.
- Use strong, unique secrets in production; never commit real secrets.
- Critical vars: `DATABASE_URL`, `SECRET_KEY`, SMTP for emails, CORS origins, token expirations.

### 6. DEPLOYMENT
- Production builds only.
- Use PM2 to manage both frontend and backend.
- Backend launcher: `./launch_backend.sh [start|stop|restart|status|logs]` sets up venv, installs deps, and runs uvicorn under PM2.
- Configure Nginx to proxy `/` to Next.js and `/api/` to FastAPI.

## CRITICAL RULES
1. **NEVER use Tailwind CSS** — only custom CSS.
2. **Always create a new migration** for DB changes — never modify existing migrations.
3. **Follow conventional commits** with detailed descriptions.
4. **Push all changes to Git** and keep docs updated.
5. **Use strong hashing** (bcrypt/Argon2) for passwords; store TOTP secrets encrypted; rotate tokens.
6. **Enforce production**: build and run in production mode.
7. **Update backend/.env.example** whenever a new config is added (hard requirement).
8. **Use scripts/db_migrate.sh** to keep DB in sync with code.

## CHECKLIST FOR SECURITY
- Input validation (Pydantic), server-side checks.
- Prepared statements/ORM (SQLAlchemy).
- Secure cookies (HttpOnly, Secure, SameSite) or Bearer tokens with short TTL + refresh rotation.
- Rate-limit login, password reset, and verification endpoints.
- Log auth/security events to `security_audit_log`.
- Password policy (length/entropy), throttle failed attempts, lockouts.

## COMMUNICATION & DOCS
- Document any new environment variables in `backend/.env.example` and note usage in code comments.
- Update this INSTRUCTIONS file when adding new security or deployment requirements.

---

**Last Updated:** October 26, 2025  
**Version:** 1.3.0  
**Status:** Active Development
