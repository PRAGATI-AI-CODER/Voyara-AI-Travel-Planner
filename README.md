@'
# ✈️ Voyara — AI-Powered Travel Intelligence & Itinerary Planner

Voyara is a full-stack AI travel planning platform that transforms a traveler's preferences into personalized, structured, and constraint-aware travel itineraries.

The project combines a modern Next.js frontend with a FastAPI backend, PostgreSQL database, and Google Gemini-powered itinerary generation.

---

## 🚀 Features

- 🌍 Personalized travel itinerary generation
- 🤖 Google Gemini AI integration
- 🧠 Constraint-aware AI planning
- 📅 Multi-day itinerary generation
- 💰 Budget-aware planning
- 👥 Traveler-aware recommendations
- 🎯 Interest-based personalization
- 🧭 Travel-style-aware planning
- ✅ Structured AI output validation
- 🔄 Automatic AI validation and retry
- 🛡️ Deterministic fallback when AI planning fails
- 📍 Geographic consistency constraints
- 🗄️ PostgreSQL-backed trip management
- ⚡ FastAPI REST APIs
- 🎨 Next.js frontend
- 📱 Responsive itinerary presentation

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      Next.js UI      │
                         │   React + TypeScript  │
                         └──────────┬───────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      Backend         │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
          ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
          │ Trip Service │  │ AI Planning  │  │ Constraint   │
          │              │  │ Service      │  │ Service      │
          └──────┬───────┘  └──────┬───────┘  └──────────────┘
                 │                 │
                 ▼                 ▼
          ┌──────────────┐  ┌──────────────┐
          │ PostgreSQL   │  │ Gemini API   │
          └──────────────┘  └──────────────┘