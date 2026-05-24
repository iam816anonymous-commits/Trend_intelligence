# Trend Intelligence AI (India First)

An AI-powered platform for continuously collecting and analyzing trends in India, with plans for global expansion.

## Stack

- **Backend:** FastAPI, Python 3.12, Postgres, Redis, Qdrant
- **AI:** SentenceTransformers, OpenAI compatible layer
- **Collection:** feedparser, playwright, beautifulsoup4, newspaper3k, scrapy
- **Frontend:** Next.js, Tailwind, shadcn
- **Infra:** Docker, Docker Compose

## Project Structure

- `backend/`: FastAPI application and AI logic
- `frontend/`: Next.js dashboard
- `infra/`: Infrastructure configuration (shared with root)
- `docs/`: Architecture and design documentation

## Getting Started

1. Copy `.env.example` to `.env`
2. Run `docker compose up --build`
3. Backend will be available at `http://localhost:8000`
4. Frontend will be available at `http://localhost:3000`

## Phase 0 Deliverables
- [x] Running backend
- [x] Running frontend
- [x] DB connection checks
- [x] Docker setup
