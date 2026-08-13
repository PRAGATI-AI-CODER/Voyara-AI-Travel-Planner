# Changelog

All notable changes to Voyara are documented in this file.

---

## [Unreleased]

Current development version.

---

## Day 1 — August 11, 2026

### Milestone: Project Foundation

### Added

- Created the public GitHub repository:
  `Voyara-AI-Travel-Planner`
- Cloned the repository locally.
- Connected the local repository to GitHub.
- Created the root `.gitignore`.
- Created the `backend/` directory.
- Created the Python virtual environment.
- Installed FastAPI.
- Installed Uvicorn.
- Created `backend/requirements.txt`.
- Created the initial FastAPI application.
- Added the root API endpoint.
- Added the health-check endpoint.
- Enabled FastAPI interactive API documentation.

### Backend

Initial backend structure:

```text
backend/
├── .venv/
├── main.py
└── requirements.txt
```

### API

Initial endpoints:

```text
GET /
GET /health
```

Interactive API documentation:

```text
/docs
```

---

## Day 2 — August 12, 2026

### Milestone: Frontend Foundation

### Added

- Verified Node.js installation.
- Verified npm installation.
- Created the `frontend/` application using `create-next-app`.
- Initialized the frontend with Next.js 16.3.0.
- Added TypeScript.
- Added ESLint.
- Added Tailwind CSS.
- Added Next.js App Router.
- Added the `src/` directory structure.
- Enabled Turbopack.
- Selected No for React Compiler.
- Retained the default `@/*` import alias.
- Successfully installed frontend dependencies.
- Verified that the frontend compiled successfully.
- Started the Next.js development server.
- Verified the frontend at:
  `http://localhost:3000`
- Replaced the default Next.js starter page with the initial Voyara page.

### Frontend

Initial frontend structure:

```text
frontend/
├── public/
├── src/
│   └── app/
│       ├── favicon.ico
│       ├── globals.css
│       ├── layout.tsx
│       └── page.tsx
├── package.json
├── package-lock.json
├── tsconfig.json
├── next.config.ts
├── eslint.config.mjs
└── postcss.config.mjs
```

### Configuration

```text
Next.js        16.3.0
TypeScript     Enabled
ESLint         Enabled
Tailwind CSS   Enabled
App Router     Enabled
Turbopack      Enabled
React Compiler Disabled
```

### Documentation

- Created `PROJECT_NOTES.md`.
- Created `CHANGELOG.md`.
- Established the project documentation workflow.
- Established the practice of documenting development milestones, technical decisions, testing, and progress.

### Testing

Verified successfully:

- Node.js installation.
- npm installation.
- Next.js project creation.
- Frontend dependency installation.
- Next.js development server.
- Local frontend at `http://localhost:3000`.
- Initial Voyara page rendering.
- Git tracking of the frontend.
- `.gitignore` correctly excluding generated files such as `node_modules/` and `.next/`.

---

## Day 3 — August 13, 2026

### Milestone: Landing Page and Trip Intake

### Added

- Created the reusable `Hero` component.
- Created the `TripForm` component.
- Replaced the minimal homepage with the first Voyara landing page.
- Added Voyara product messaging.
- Added AI-powered travel intelligence branding.
- Added the Start planning button.
- Added the Explore Voyara button.
- Added feature cards:
  - Personalized
  - Context-aware
  - Intelligent
- Added landing page navigation to the trip planner.
- Added a structured trip-planning form.
- Added destination input.
- Added start date input.
- Added end date input.
- Added traveler count input.
- Added budget input.
- Added travel-style selection.
- Added travel-interest selection.
- Added interactive selection states.

### Frontend Components

```text
frontend/
└── src/
    ├── app/
    │   └── page.tsx
    │
    └── components/
        ├── landing/
        │   └── Hero.tsx
        │
        └── trip-planner/
            └── TripForm.tsx
```

### Trip Data

The frontend collects:

```text
destination
start_date
end_date
travelers
budget
travel_style[]
interests[]
```

### Testing

Verified successfully:

- Landing page renders.
- Start Planning navigation works.
- Destination input works.
- Date inputs work.
- Traveler input works.
- Budget input works.
- Travel style selection works.
- Multiple interests can be selected.
- Trip intake section renders correctly.

---

### Milestone: Trip Request Schema and API

### Added

- Created the `backend/schemas/` directory.
- Created `backend/schemas/trip.py`.
- Added the `TripRequest` Pydantic model.
- Added destination validation.
- Added start date validation.
- Added end date validation.
- Added traveler count validation.
- Added budget validation.
- Added travel-style validation.
- Added interest validation.
- Added validation to prevent the end date from being before the start date.
- Added the `POST /api/trips` endpoint.
- Connected the `TripRequest` schema to the FastAPI endpoint.
- Verified the API through FastAPI Swagger documentation.

### Backend

Updated backend structure:

```text
backend/
├── .venv/
├── schemas/
│   └── trip.py
├── main.py
└── requirements.txt
```

### API

Added endpoint:

```text
POST /api/trips
```

### Trip Request Structure

```json
{
  "destination": "Paris",
  "start_date": "2026-09-01",
  "end_date": "2026-09-07",
  "travelers": 2,
  "budget": 50000,
  "travel_style": [
    "Relaxed"
  ],
  "interests": [
    "Food",
    "Culture"
  ]
}
```

### Validation Testing

Verified successfully:

- Valid trip data is accepted.
- Invalid end-date ordering is rejected.
- Invalid traveler count is rejected.
- FastAPI returns `422 Unprocessable Entity` for invalid requests.

---

### Milestone: Frontend-Backend Integration

### Added

- Connected the `TripForm` to the FastAPI backend.
- Added controlled state management for the trip form.
- Added frontend API request handling.
- Added JSON request payload.
- Added loading state.
- Added success feedback.
- Added frontend error handling.
- Added `fetch()` integration with the backend.
- Added FastAPI CORS configuration.
- Connected the Next.js frontend to `POST /api/trips`.

### Data Flow

```text
TripForm
   ↓
JSON Request
   ↓
POST /api/trips
   ↓
FastAPI
   ↓
TripRequest
   ↓
Pydantic Validation
   ↓
Structured Trip Data
   ↓
API Response
   ↓
Frontend
```

### CORS

Configured local development origins:

```text
http://localhost:3000
http://127.0.0.1:3000
```

### Testing

Verified successfully:

- FastAPI server starts correctly.
- FastAPI Swagger documentation loads.
- `POST /api/trips` appears in Swagger.
- Valid trip data is accepted.
- Invalid trip data is rejected.
- Frontend successfully sends trip data.
- Backend successfully receives trip data.
- Frontend displays successful submission feedback.
- Frontend-backend communication works locally.
- CORS configuration works correctly.

### Current Status

Voyara now has its first complete full-stack request flow:

```text
Next.js Frontend
       ↓
    TripForm
       ↓
  FastAPI Backend
       ↓
Pydantic Validation
       ↓
 Structured Trip Data
       ↓
    API Response
       ↓
    Frontend
```

---

## Upcoming Development

The next planned milestones are:

```text
PostgreSQL integration
        ↓
Trip persistence
        ↓
Database models
        ↓
Travel data ingestion
        ↓
ETL / ELT pipeline
        ↓
Travel knowledge base
        ↓
Embeddings
        ↓
Vector search
        ↓
RAG pipeline
        ↓
Gemini integration
        ↓
AI travel planner
        ↓
Agentic itinerary generation
        ↓
Itinerary validation
        ↓
Authentication
        ↓
Production deployment
```