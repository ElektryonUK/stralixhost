# STRALIXHOST - AI DEVELOPMENT INSTRUCTIONS

This file contains the comprehensive instructions and requirements for developing the Stralixhost project. Any AI assistant working on this project should follow these guidelines precisely.

## PROJECT OVERVIEW

**Stralixhost** is a monorepo for a huge full-stack web application project. This is the foundational setup phase with plans for significant expansion.

## CORE REQUIREMENTS

### 1. REPOSITORY STRUCTURE
- **Monorepo architecture** - All components in a single repository
- **Modular organization** - Clear separation between frontend, backend, database, shared utilities
- **Professional structure** - Enterprise-level organization and practices

### 2. FRONTEND REQUIREMENTS

#### Technology Stack
- **Next.js** - Latest version (14+) with App Router
- **TypeScript** - Strict typing throughout
- **NO TAILWIND CSS** - Must use custom CSS only
- **React** - Latest stable version
- **Custom styling** - CSS Modules and custom CSS with variables

#### Frontend Structure
```
frontend/
├── app/                 # Next.js App Router
├── components/          # Reusable components
├── styles/              # Custom CSS files
├── public/              # Static assets
└── package.json         # Dependencies
```

#### Styling Guidelines
- **Custom CSS only** - No CSS frameworks (Tailwind, Bootstrap, etc.)
- **CSS Modules** for component-specific styles
- **CSS Variables** for theming and consistency
- **Responsive design** - Mobile-first approach
- **Professional UI** - Clean, modern design patterns

### 3. DATABASE REQUIREMENTS

#### Database System
- **PostgreSQL** - Primary database
- **UUID primary keys** - Use uuid-ossp extension
- **Migration system** - Version-controlled schema changes

#### Database Structure
```
database/
├── schema.sql           # Current complete schema
└── migrations/          # Incremental migration files
    ├── 001_initial_schema.sql
    ├── 002_next_migration.sql
    └── ...
```

#### Migration Rules
- **Sequential numbering** - 001, 002, 003, etc.
- **Descriptive names** - Clear purpose in filename
- **Up/Down migrations** - Include rollback capability
- **Schema tracking** - Update main schema.sql after each migration
- **New migration for every DB change** - Never modify existing migrations

### 4. DEVELOPMENT PRACTICES

#### Git Workflow
- **All changes pushed to Git** - Every modification committed
- **Conventional commits** - Structured commit messages
- **Proper commit descriptions** - Detailed explanations of changes

#### Commit Message Format
```
type(scope): brief description

Detailed description of changes including:
- What was changed
- Why it was changed
- Any breaking changes
- Additional context
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Testing changes
- `chore`: Maintenance

#### Code Quality
- **TypeScript strict mode** - No any types without justification
- **ESLint configuration** - Code quality enforcement
- **Consistent formatting** - Follow established patterns
- **Error handling** - Proper error boundaries and user feedback
- **Loading states** - User experience during async operations

### 5. PROJECT DOCUMENTATION

#### Required Documentation
- **README.md** - Project overview and quick start
- **PROJECT_STRUCTURE.md** - Detailed architecture documentation
- **INSTRUCTIONS.md** - This file for AI assistants
- **Code comments** - Complex logic explanation
- **API documentation** - When backend is implemented

Additionally:
- **README technology banner** - Always keep a "Technologies" section at the very top of README listing all currently used tools/libraries. Update it whenever a new technology is introduced.
- **License tag** - README must include `license: proprietary` in the License section.

### 6. BEST PRACTICES TO FOLLOW

#### File Organization
- **Clear naming conventions** - Descriptive, consistent names
- **Logical grouping** - Related files together
- **Proper imports** - Relative paths and barrel exports where appropriate

#### Component Development
- **Functional components** with hooks
- **TypeScript interfaces** for all props
- **CSS Modules** for styling
- **Accessibility** - Proper ARIA labels and semantic HTML
- **Performance** - Optimize for loading and runtime

#### Database Design
- **Normalized structure** - Avoid data duplication
- **Proper indexing** - Performance optimization
- **Foreign key constraints** - Data integrity
- **Audit trails** - created_at, updated_at fields
- **Soft deletes** - When appropriate

## CURRENT PROJECT STATE

### Completed Components
✅ GitHub repository created  
✅ README.md with project overview  
✅ Database schema with users and sessions  
✅ Migration system implemented  
✅ Next.js frontend application setup  
✅ Basic page structure and routing  
✅ Custom CSS styling system  
✅ Error handling and loading states  
✅ TypeScript configuration  
✅ ESLint setup  
✅ Project documentation  

### Immediate Next Steps
- [ ] Implement backend API server
- [ ] Add authentication system
- [ ] Create shared utilities package
- [ ] Implement user registration/login
- [ ] Add database connection layer
- [ ] Create API client for frontend
- [ ] Add testing framework
- [ ] Set up CI/CD pipeline

### Long-term Roadmap
- [ ] User management system
- [ ] Role-based access control
- [ ] Email system integration
- [ ] File upload functionality
- [ ] Search capabilities
- [ ] Analytics implementation
- [ ] Performance monitoring
- [ ] Security hardening

## DEVELOPMENT ENVIRONMENT

### Required Tools
- **Node.js** 18+ (for frontend)
- **PostgreSQL** 14+ (for database)
- **Git** (version control)
- **VS Code** (recommended editor)

### Environment Setup
1. Clone repository
2. Install frontend dependencies (`cd frontend && npm install`)
3. Set up PostgreSQL database
4. Run database migrations
5. Configure environment variables
6. Start development server

## CRITICAL RULES FOR AI ASSISTANTS

### Absolute Requirements
1. **NEVER use Tailwind CSS** - Only custom CSS allowed
2. **Always create database migrations** - Never modify existing ones
3. **Follow conventional commits** - Proper format and descriptions
4. **Push all changes to Git** - Every modification must be committed
5. **Update documentation** - Keep all docs current with changes
6. **Use TypeScript strictly** - Proper typing throughout
7. **Test locally before committing** - Ensure functionality works
8. **Always run and build in production mode** - Use production builds by default for verification (e.g., `npm run build && npm start` in frontend)
9. **README technology banner** - Keep technologies section current at the top of README; update on every new tool/library addition.
10. **License tag** - Ensure README contains `license: proprietary` in License section.

### Decision Making
- **Performance over convenience** - Choose solutions that scale
- **Security first** - Always consider security implications
- **User experience** - Prioritize intuitive, accessible interfaces
- **Code maintainability** - Write code that others can understand and modify
- **Future-proofing** - Consider scalability and extensibility

### When in Doubt
- **Follow existing patterns** - Consistency with current codebase
- **Ask for clarification** - Don't assume requirements
- **Document decisions** - Explain why choices were made
- **Test thoroughly** - Verify all functionality works

## TECHNOLOGY PREFERENCES

### Frontend
- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Custom CSS** with CSS Modules
- **React hooks** for state management
- **Native fetch** or Axios for API calls

### Backend (When Implemented)
- **Node.js** with Express or Fastify
- **TypeScript** throughout
- **PostgreSQL** with connection pooling
- **JWT** for authentication
- **bcrypt** for password hashing

### DevOps (Future)
- **Docker** for containerization
- **GitHub Actions** for CI/CD
- **Vercel/Netlify** for frontend deployment
- **Cloud PostgreSQL** for production database

## COMMUNICATION GUIDELINES

When working on this project:
1. **Explain all changes** made in commit messages
2. **Document new patterns** introduced
3. **Update relevant documentation** files
4. **Mention any breaking changes**
5. **Provide setup instructions** for new features

---

**Last Updated:** October 26, 2025  
**Version:** 1.2.0  
**Status:** Active Development

*This file should be updated whenever new requirements or guidelines are established.*