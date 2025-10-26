# Stralixhost Project Structure

This document outlines the structure and organization of the Stralixhost monorepo.

## Repository Overview

```
stralixhost/
├── README.md                    # Main project documentation
├── docs/                        # Project documentation
│   └── PROJECT_STRUCTURE.md     # This file
├── database/                    # Database schemas and migrations
│   ├── schema.sql               # Current database schema
│   └── migrations/              # Database migration files
│       └── 001_initial_schema.sql   # Initial migration
├── frontend/                    # Next.js frontend application
│   ├── app/                     # Next.js App Router pages
│   │   ├── globals.css              # Global styles
│   │   ├── layout.tsx               # Root layout
│   │   ├── page.tsx                 # Home page
│   │   ├── loading.tsx              # Loading UI
│   │   ├── error.tsx                # Error UI
│   │   └── not-found.tsx            # 404 page
│   ├── components/              # Reusable React components
│   │   └── Header.tsx               # Navigation header
│   ├── package.json             # Frontend dependencies
│   ├── tsconfig.json            # TypeScript configuration
│   ├── next.config.js           # Next.js configuration
│   ├── .eslintrc.json           # ESLint configuration
│   ├── .env.example             # Environment variables template
│   └── .gitignore               # Git ignore rules
└── backend/                     # Backend API (to be implemented)
└── shared/                      # Shared utilities (to be implemented)
```

## Architecture Overview

### Frontend (Next.js)

The frontend is built using Next.js 14 with the App Router and TypeScript:

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Custom CSS (no frameworks like Tailwind)
- **State Management**: React hooks (to be extended as needed)
- **UI Components**: Custom components in `/components` directory

#### Key Features

- Server-side rendering (SSR) and static site generation (SSG)
- TypeScript for type safety
- Custom CSS with CSS variables for theming
- Responsive design
- Error boundaries and loading states
- SEO-optimized with proper meta tags

#### Styling Approach

- CSS Modules for component-specific styles
- Global CSS variables for consistent theming
- No external CSS frameworks (Tailwind, Bootstrap, etc.)
- Mobile-first responsive design
- Custom utility classes when needed

### Database

PostgreSQL database with migration system:

- **Database**: PostgreSQL with UUID primary keys
- **Migration System**: SQL-based migrations with version tracking
- **Schema Management**: Centralized schema file + incremental migrations

#### Current Schema

- `users` - User authentication and profile data
- `user_sessions` - Session management
- `schema_migrations` - Migration version tracking

### Development Workflow

#### Commit Convention

We follow conventional commits:

```
type(scope): description

Detailed description of changes
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(auth): add user registration endpoint
fix(ui): resolve header navigation on mobile
docs: update API documentation
```

#### Database Migrations

When making database schema changes:

1. Create a new migration file in `database/migrations/`
2. Use sequential numbering: `002_add_user_roles.sql`, `003_create_posts_table.sql`
3. Include both UP and DOWN migration statements
4. Update the main `schema.sql` file to reflect the current state
5. Test migrations locally before committing

#### Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch (to be created)
- `feature/*` - Feature branches
- `fix/*` - Bug fix branches
- `hotfix/*` - Critical production fixes

## Getting Started

### Prerequisites

- Node.js 18+
- PostgreSQL 14+
- Git

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ElektryonUK/stralixhost.git
   cd stralixhost
   ```

2. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your configuration
   npm run dev
   ```

3. **Setup Database:**
   ```bash
   # Create PostgreSQL database
   createdb stralixhost
   
   # Run initial migration
   psql -d stralixhost -f database/migrations/001_initial_schema.sql
   ```

4. **Verify Setup:**
   - Frontend: http://localhost:3000
   - Ensure database connection is working

## Future Development

### Planned Features

1. **Backend API**
   - Node.js/Express server
   - RESTful API design
   - Authentication system
   - Database integration

2. **Authentication System**
   - User registration/login
   - Session management
   - Password reset functionality
   - Social login options

3. **Shared Package**
   - Common types and interfaces
   - Utility functions
   - API client library

### Tech Stack Expansion

- **Testing**: Jest, React Testing Library, Cypress
- **State Management**: Zustand or Redux Toolkit
- **API Client**: Axios or native fetch
- **Validation**: Zod for schema validation
- **Documentation**: Storybook for components

## Contributing Guidelines

1. **Code Style**: Follow existing patterns and ESLint rules
2. **Testing**: Add tests for new features
3. **Documentation**: Update documentation for significant changes
4. **Reviews**: All changes require code review
5. **Commits**: Follow conventional commit format

## Deployment

Deployment strategy (to be implemented):

- **Frontend**: Vercel or Netlify
- **Backend**: Docker containers on cloud platform
- **Database**: Managed PostgreSQL service
- **CI/CD**: GitHub Actions

---

*This document will be updated as the project evolves.*