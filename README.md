# AI Crawler Intelligence Engine

Behavior-based AI crawler detection proof of concept built with FastAPI and PostgreSQL.

---

## Overview

This system analyzes raw server log files and detects AI-style retrieval behavior using deterministic behavioral scoring.

It does NOT rely on user-agent matching.

Instead, it evaluates:

- Crawl depth
- Burst request patterns
- URL repetition
- Sitemap interaction
- Behavioral clustering (0–100 AI score)

---

## Why This Matters

Modern AI systems retrieve content differently than traditional search engine crawlers.

This engine demonstrates how AI-style retrieval behavior can be identified purely through behavioral modeling.

---

## Architecture

Backend:
- FastAPI
- PostgreSQL
- Deterministic scoring engine

Frontend:
- Vanilla JavaScript
- Chart.js
- Dark-mode intelligence dashboard

---

## Behavioral Signals Modeled

- Average URL depth
- Burst rate
- Repeated URL ratio
- HTML vs resource request ratio
- Sitemap interaction

---

## How to Run Locally

### 1. Install dependencies

pip install -r requirements.txt

### 2. Create PostgreSQL database

Create database:
ai_crawler_detector

Run schema:
psql -U postgres -d ai_crawler_detector -f schema.sql

### 3. Add environment file

Create `.env`:

DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/ai_crawler_detector

### 4. Start backend

uvicorn main:app --reload

### 5. Start frontend

cd frontend
python -m http.server 5500

Visit:
http://localhost:5500

---

## Proof of Concept Scope

This project demonstrates:

- Behavioral AI crawler scoring
- Visual clustering
- Depth vs score correlation
- Burst activity modeling
- Explainable intelligence summary

This is a proof-of-concept and not production hardened.

---

## License

MIT (or specify if private use)
