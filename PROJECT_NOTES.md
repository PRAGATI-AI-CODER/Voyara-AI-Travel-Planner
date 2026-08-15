# Voyara — Project Notes

## Project Overview

Voyara is an AI-powered travel intelligence and itinerary planning platform.

The goal is to build a significantly improved version of a conventional AI travel planner by combining:

- Generative AI
- Retrieval-Augmented Generation (RAG)
- Real-time travel information
- Structured traveler preferences
- Constraint-aware itinerary planning
- Agentic workflows
- PostgreSQL
- FastAPI
- Next.js
- Data ingestion and processing

The project is being developed as a portfolio-grade full-stack AI project with deployment and placement interviews in mind.

---

# Development Log

## Day 1 — August 11, 2026

### Milestone: Project Foundation

### Objective

Initialize the Voyara repository and establish a clean development environment for the backend.

### Completed

- Created public GitHub repository: `Voyara-AI-Travel-Planner`
- Cloned repository locally.
- Connected local repository to GitHub remote.
- Created root `.gitignore`.
- Created `backend/` directory.
- Created Python virtual environment at `backend/.venv/`.
- Installed FastAPI.
- Installed Uvicorn.
- Generated backend `requirements.txt`.
- Verified that the virtual environment is excluded from Git.

### Backend Environment

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

FastAPI interactive documentation:

```text
/docs
```

---

## Day 2 — August 12, 2026

### Milestone: Frontend Foundation and Project Documentation

### Objective

Initialize the Voyara frontend using Next.js and establish a clean full-stack project structure while introducing project-level development documentation.

### Completed

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
- Kept React Compiler disabled.
- Retained the default `@/*` import alias.
- Successfully installed frontend dependencies.
- Verified that the frontend compiled successfully.
- Started the Next.js development server.
- Verified the frontend at `http://localhost:3000`.
- Replaced the default Next.js starter page with the initial Voyara page.
- Created `PROJECT_NOTES.md`.
- Created `CHANGELOG.md`.
- Established the project documentation workflow.
- Established the practice of documenting development milestones, technical decisions, testing, and progress.

### Frontend Environment

```text
Next.js        16.3.0
React          Installed
TypeScript     Enabled
ESLint         Enabled
Tailwind CSS   Enabled
App Router     Enabled
Turbopack      Enabled
React Compiler Disabled
```

### Frontend Structure

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

---

## Day 3 — August 13, 2026

### Milestone: Landing Page and Trip Intake

### Objective

Build the first real user-facing Voyara experience and establish the initial structured travel preference input layer.

### Completed

- Created reusable `Hero` component.
- Created `TripForm` component.
- Replaced the minimal homepage with the first Voyara landing page.
- Added Voyara product messaging.
- Added AI-powered travel intelligence branding.
- Added `Start planning` navigation.
- Added `Explore Voyara` interaction.
- Added feature cards:
  - Personalized
  - Context-aware
  - Intelligent
- Added structured trip-planning form.
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

### Completed

- Created `backend/schemas/` directory.
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

### Backend Structure

```text
backend/
├── .venv/
├── schemas/
│   └── trip.py
├── main.py
└── requirements.txt
```

### API

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

### Completed

- Connected `TripForm` to the FastAPI backend.
- Added controlled state management for the trip form.
- Added frontend API request handling.
- Added JSON request payload.
- Added loading state.
- Added success feedback.
- Added frontend error handling.
- Added `fetch()` integration with the backend.
- Added FastAPI CORS configuration.
- Connected the Next.js frontend to `POST /api/trips`.
- Verified frontend-backend communication locally.

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

### Objective

Introduce PostgreSQL persistence to Voyara and connect the FastAPI backend with the database so submitted trips can be stored and retrieved.

### Completed

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

### Trip Database Model

The `Trip` model stores:

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

The complete real-world flow was verified:

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

---

# Current Project Structure

```text
Voyara-AI-Travel-Planner/
│
├── backend/
│   ├── .venv/
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   ├── schemas/
│   │   └── trip.py
│   ├── .env
│   ├── init_db.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   │   └── page.tsx
│   │   └── components/
│   │       ├── landing/
│   │       │   └── Hero.tsx
│   │       └── trip-planner/
│   │           └── TripForm.tsx
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── next.config.ts
│   ├── eslint.config.mjs
│   └── postcss.config.mjs
│
├── .gitignore
├── CHANGELOG.md
└── PROJECT_NOTES.md
```

---

# Upcoming Development

```text
Travel data ingestion
        ↓
External travel data layer
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
Constraint-aware itinerary generation
        ↓
Agentic itinerary workflow
        ↓
Itinerary validation
        ↓
Authentication
        ↓
Production deployment
        ↓
Final testing
        ↓
Portfolio polish
```


---

## Day 5 — August 15, 2026

### Milestone: Complete Trip CRUD API

### Objective

Strengthen the Voyara backend by introducing structured API response schemas and completing the core CRUD operations for persistent trips stored in PostgreSQL.

### Completed

- Reviewed the existing PostgreSQL-backed trip API.
- Added structured Pydantic response schemas.
- Created the `TripResponse` schema.
- Created the `TripListResponse` schema.
- Created the `TripCreateResponse` schema.
- Updated `POST /api/trips` to use a structured response model.
- Updated `GET /api/trips` to use a structured response model.
- Added `GET /api/trips/{trip_id}` for retrieving a specific trip.
- Added proper `404 Not Found` handling when a requested trip does not exist.
- Added `DELETE /api/trips/{trip_id}` for deleting a specific trip.
- Added proper `404 Not Found` handling for deletion of non-existent trips.
- Verified FastAPI Swagger documentation after the API changes.
- Verified that the existing frontend continued to work after the backend API changes.
- Verified successful trip creation through the frontend.
- Verified successful trip persistence in PostgreSQL.
- Tested retrieval of individual trips.
- Tested deletion of an individual trip.
- Verified that deleted trips can no longer be retrieved.
- Verified that other existing trips remain unaffected after deletion.

### API Endpoints

```text
POST   /api/trips
GET    /api/trips
GET    /api/trips/{trip_id}
DELETE /api/trips/{trip_id}
```

### API Architecture

```text
POST /api/trips
       ↓
TripRequest
       ↓
Pydantic Validation
       ↓
SQLAlchemy
       ↓
PostgreSQL
       ↓
TripCreateResponse
```

```text
GET /api/trips
       ↓
SQLAlchemy
       ↓
PostgreSQL
       ↓
TripListResponse
```

```text
GET /api/trips/{trip_id}
       ↓
SQLAlchemy
       ↓
PostgreSQL
       ↓
TripResponse
       ↓
404 if trip does not exist
```

```text
DELETE /api/trips/{trip_id}
       ↓
SQLAlchemy
       ↓
PostgreSQL
       ↓
Trip deleted
       ↓
Success response
       ↓
404 if trip does not exist
```

### Response Schemas

Created the following Pydantic schemas:

```text
TripResponse
TripListResponse
TripCreateResponse
```

These provide structured and predictable API responses instead of relying only on manually constructed dictionaries.

### CRUD Status

```text
CREATE   POST   /api/trips              ✅
READ ALL GET    /api/trips              ✅
READ ONE GET    /api/trips/{trip_id}    ✅
DELETE   DELETE /api/trips/{trip_id}   ✅
```

### Testing

Verified successfully:

- FastAPI server starts successfully.
- Swagger documentation loads successfully.
- Structured response schemas are recognized by FastAPI.
- `POST /api/trips` successfully creates trips.
- Created trips are persisted in PostgreSQL.
- `GET /api/trips` successfully retrieves all stored trips.
- `GET /api/trips/{trip_id}` successfully retrieves an individual trip.
- Non-existent trip IDs return `404 Not Found`.
- `DELETE /api/trips/{trip_id}` successfully deletes a trip.
- Deleted trip IDs return `404 Not Found` when requested again.
- Existing trips remain unaffected after another trip is deleted.
- Next.js frontend continues to communicate successfully with FastAPI.
- Frontend trip submission continues to work after the API restructuring.

### Verified Database State

During CRUD testing:

```text
Trip ID 1 → Paris
Trip ID 2 → Deleted
Trip ID 3 → Japan
```

Verification confirmed:

```text
GET /api/trips/1 → Paris     ✅
GET /api/trips/2 → 404       ✅
GET /api/trips/3 → Japan     ✅
```

### Day 5 Architecture

```text
                         VOYARA
                            │
                            ▼
                    Next.js Frontend
                            │
                            ▼
                    FastAPI REST API
                            │
                  Pydantic Schemas
                            │
                            ▼
                       SQLAlchemy
                            │
                            ▼
                     PostgreSQL 18.6
                            │
                 ┌──────────┼──────────┐
                 ▼          ▼          ▼
              Create      Read      Delete
                 │          │          │
                 └──────────┼──────────┘
                            ▼
                     Persistent Trips
```

### Day 5 Status

```text
Response schemas              ✅
POST /api/trips               ✅
GET /api/trips                ✅
GET /api/trips/{trip_id}      ✅
DELETE /api/trips/{trip_id}   ✅
404 error handling            ✅
Swagger verification          ✅
Frontend integration          ✅
PostgreSQL persistence        ✅
CRUD testing                  ✅
End-to-end testing            ✅
```