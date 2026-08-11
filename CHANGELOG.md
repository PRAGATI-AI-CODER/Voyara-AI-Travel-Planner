# Changelog

All notable changes to Voyara are documented in this file.

---

## [Unreleased]

Current development version.

---

## [0.2.0] — 2026-08-12

### Added

- Initialized Next.js frontend.
- Added TypeScript.
- Added ESLint.
- Added Tailwind CSS.
- Added Next.js App Router.
- Added `src/` directory structure.
- Added initial frontend application.
- Verified frontend development server.
- Replaced the default Next.js starter page with the initial Voyara page.

### Frontend

- Next.js 16.3.0
- React
- TypeScript
- Tailwind CSS
- Turbopack
- App Router

### Configuration

- React Compiler disabled.
- Default `@/*` import alias retained.
- Generated Next.js project structure retained.

---

## [0.1.0] — 2026-08-11

### Added

- Created the Voyara GitHub repository.
- Initialized the local Git repository.
- Connected the local repository to GitHub.
- Added the root `.gitignore`.
- Created the `backend/` directory.
- Created a Python virtual environment.
- Installed FastAPI.
- Installed Uvicorn.
- Created `backend/requirements.txt`.
- Created the initial FastAPI application.
- Added the root API endpoint.
- Added the health-check endpoint.
- Enabled FastAPI interactive API documentation.

### API

Initial endpoints:

```text
GET /
GET /health