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

### Milestone: Frontend Foundation and Project Documentation

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
- Created `PROJECT_NOTES.md`.
- Created `CHANGELOG.md`.
- Established the project documentation workflow.
- Established the practice of documenting development milestones, technical decisions, testing, and progress.

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

---

## Day 3 — August 13, 2026

### Milestone: Landing Page and Trip Intake

### Added

- Created the reusable `Hero` component.
- Created the `TripForm` component.
- Replaced the minimal homepage with the first Voyara landing page.
- Added Voyara product messaging.
- Added AI-powered travel intelligence branding.
- Added the `Start planning` button.
- Added the `Explore Voyara` interaction.
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

---

## Day 4 — August 14, 2026

### Milestone: PostgreSQL Database and Persistent Trip Storage

### Added

- Installed PostgreSQL 18.6 on Windows.
- Verified PostgreSQL installation.
- Created the `voyara` PostgreSQL database.
- Verified successful connection to the `voyara` database.
- Installed SQLAlchemy.
- Installed Psycopg.
- Installed `python-dotenv`.
- Updated `backend/requirements.txt`.
- Created the `backend/database/` directory.
- Created `backend/database/database.py`.
- Created `backend/database/models.py`.
- Created `backend/.env`.
- Configured the PostgreSQL connection using `DATABASE_URL`.
- Protected `.env` through `.gitignore`.
- Created the SQLAlchemy database engine.
- Created the SQLAlchemy session factory.
- Created the SQLAlchemy declarative base.
- Created the database session dependency.
- Created the `Trip` SQLAlchemy model.
- Created the PostgreSQL `trips` table.
- Created `backend/init_db.py`.
- Verified Python-to-PostgreSQL connectivity.
- Connected the FastAPI backend to PostgreSQL.
- Updated `POST /api/trips` to persist trips in PostgreSQL.
- Added PostgreSQL-generated trip IDs.
- Added `GET /api/trips` for retrieving saved trips.
- Verified saved trips directly through PostgreSQL.
- Connected the actual Next.js frontend to the PostgreSQL-backed API.
- Detected and fixed a CORS issue during frontend-backend integration.
- Verified complete end-to-end trip submission and persistence.

### Database Environment

```text
PostgreSQL    18.6
Database      voyara
User          postgres
Port          5432
```

### Python Database Stack

```text
SQLAlchemy
psycopg
psycopg-binary
python-dotenv
```

### Database Structure

```text
backend/
├── database/
│   ├── database.py
│   └── models.py
├── schemas/
│   └── trip.py
├── .env
├── init_db.py
├── main.py
└── requirements.txt
```

### Trip Model

The `Trip` SQLAlchemy model stores:

```text
id
destination
start_date
end_date
travelers
budget
travel_style
interests
```

### Database Connection Flow

```text
.env
   ↓
python-dotenv
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL 18.6
   ↓
voyara
```

### Trip Persistence Flow

```text
TripForm
   ↓
POST /api/trips
   ↓
FastAPI
   ↓
TripRequest
   ↓
Pydantic Validation
   ↓
SQLAlchemy Trip Model
   ↓
PostgreSQL
   ↓
Saved Trip
   ↓
Database-generated ID
   ↓
API Response
```

### Trip Retrieval Flow

```text
GET /api/trips
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
Saved Trips
   ↓
JSON Response
```

### Frontend-Backend Integration

Verified the complete real-world flow:

```text
Voyara Frontend
       ↓
Next.js TripForm
       ↓
POST /api/trips
       ↓
FastAPI
       ↓
Pydantic Validation
       ↓
SQLAlchemy
       ↓
PostgreSQL
       ↓
Persistent Trip
       ↓
Success Response
       ↓
Voyara Frontend
```

### CORS Fix

During frontend testing, the request initially returned:

```text
Failed to fetch
```

The issue was identified as missing CORS configuration after the database integration update.

Configured local development origins:

```text
http://localhost:3000
http://127.0.0.1:3000
```

After restoring CORS configuration, frontend submission worked successfully.

### Testing

Verified successfully:

- PostgreSQL installation works.
- `voyara` database exists.
- Python connects successfully to PostgreSQL.
- SQLAlchemy connects successfully to PostgreSQL.
- `trips` table was created successfully.
- Valid trip data is accepted.
- `POST /api/trips` creates and persists trips.
- PostgreSQL generates the trip ID.
- Saved trips can be verified directly in PostgreSQL.
- `GET /api/trips` retrieves saved trips.
- Next.js successfully communicates with FastAPI.
- CORS configuration works correctly.
- A trip submitted through the actual Voyara frontend is persisted in PostgreSQL.
- End-to-end frontend → FastAPI → PostgreSQL flow works successfully.

### Day 4 Architecture

```text
                         VOYARA
                            │
                            ▼
                    Next.js Frontend
                            │
                         TripForm
                            │
                            ▼
                    FastAPI Backend
                            │
                    Pydantic Validation
                            │
                            ▼
                       SQLAlchemy
                            │
                            ▼
                     PostgreSQL 18.6
                            │
                            ▼
                       Saved Trips
                            │
                            ▼
                     GET /api/trips
```

### Day 4 Status

```text
PostgreSQL installation       ✅
voyara database               ✅
Database connection           ✅
SQLAlchemy setup              ✅
Psycopg setup                 ✅
.env configuration            ✅
Trip database model           ✅
trips table                   ✅
POST /api/trips persistence   ✅
GET /api/trips retrieval      ✅
Frontend integration          ✅
CORS configuration            ✅
End-to-end testing            ✅
```
```


---

## Day 5 — August 15, 2026

### Added

- Added structured Pydantic response schemas:
  - `TripResponse`
  - `TripListResponse`
  - `TripCreateResponse`
- Added `GET /api/trips/{trip_id}` to retrieve an individual trip.
- Added `DELETE /api/trips/{trip_id}` to delete an individual trip.
- Added `404 Not Found` handling for non-existent trips.
- Updated `POST /api/trips` with a structured response model.
- Updated `GET /api/trips` with a structured response model.

### Backend

- Improved the FastAPI trip API structure.
- Completed core CRUD operations for persistent trips.
- Continued using SQLAlchemy and PostgreSQL for trip persistence.

### Testing

- Verified FastAPI Swagger documentation.
- Verified trip creation through the frontend.
- Verified PostgreSQL persistence.
- Verified retrieval of individual trips.
- Verified deletion of trips.
- Verified deleted trips return `404 Not Found`.
- Verified existing trips remain unaffected after deletion.
- Verified complete frontend → FastAPI → PostgreSQL integration.

### Day 5 Status

```text
Structured response schemas     ✅
Create trip                     ✅
Read all trips                  ✅
Read single trip                ✅
Delete trip                     ✅
404 error handling              ✅
Frontend integration            ✅
PostgreSQL persistence          ✅
CRUD testing                    ✅
End-to-end testing              ✅
```