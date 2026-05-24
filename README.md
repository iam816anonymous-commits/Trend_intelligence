# Trend Intelligence AI (India First)

An AI-powered platform for continuously collecting and analyzing trends in India, with plans for global expansion.

## Stack

- **Backend:** FastAPI, Python 3.12, Postgres, Redis, Qdrant
- **AI:** SentenceTransformers, OpenAI compatible layer
- **Collection:** feedparser, playwright, beautifulsoup4, newspaper3k, scrapy
- **Frontend:** Next.js, Tailwind, shadcn

## Project Structure

- `backend/`: FastAPI application and AI logic
- `frontend/`: Next.js dashboard
- `docs/`: Architecture and design documentation

## Local Setup

### Backend

1. Navigate to `backend/`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and update DB credentials.
6. Run: `uvicorn api.main:app --reload`

### Frontend

1. Navigate to `frontend/`
2. Install dependencies: `npm install`
3. Run development server: `npm run dev`

## Phase 0 Deliverables
- [x] Running backend
- [x] Running frontend
- [x] DB connection checks
- [x] Local setup guide
