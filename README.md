# Stralixhost

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

This project is proprietary. All rights reserved.