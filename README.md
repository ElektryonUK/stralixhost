<!-- Project Information Badges -->
<p align="center">
  <img alt="Stralixhost" src="https://img.shields.io/badge/project%20name-stralixhost-blueviolet" />
  <img alt="Version" src="https://img.shields.io/badge/version-0.2.0-informational" />
  <img alt="License" src="https://img.shields.io/badge/license-Proprietary-red" />
  <img alt="Lines of Code" src="https://img.shields.io/tokei/lines/github/ElektryonUK/stralixhost" />
  <img alt="Primary language" src="https://img.shields.io/github/languages/top/ElektryonUK/stralixhost" />
  <img alt="Last updated" src="https://img.shields.io/github/last-commit/ElektryonUK/stralixhost" />
  <img alt="Commits" src="https://img.shields.io/github/commit-activity/y/ElektryonUK/stralixhost" />
</p>

<p align="center">
  <img alt="Stack" src="https://img.shields.io/badge/stack-FastAPI%2C%20Next.js%2C%20PostgreSQL%2C%20TypeScript%2C%20Python-6a1b9a?logo=python&logoColor=white" />
</p>

# Stralixhost

## Technologies

- Next.js 14 (App Router)
- React 18
- TypeScript 5
- Custom CSS (no Tailwind)
- ESLint (Next core-web-vitals, TS rules)
- PostgreSQL (schema + migrations)
- PM2 (production process manager)

A full-stack web application built as a monorepo with modern development practices.

## Project Structure

```
stralixhost/
├── frontend/          # Next.js frontend application
├── backend/           # Backend API (to be implemented)
├── database/          # Database schemas and migrations
├── shared/            # Shared utilities and types
└── docs/              # Project documentation
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Git

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ElektryonUK/stralixhost.git
   cd stralixhost
   ```

2. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Development Workflow

- Follow conventional commits for commit messages
- Use feature branches for new development
- Database schema changes require new migration files
- All changes should be tested before pushing

## Tech Stack

### Frontend
- Next.js 14+
- React
- Custom CSS (no Tailwind)
- TypeScript

### Backend (Planned)
- Node.js/Express or similar
- Database (PostgreSQL/MongoDB)
- Authentication system

## Contributing

Please read our contributing guidelines and follow the established code style and commit conventions.

## License

license: proprietary

This project is proprietary. All rights reserved.
