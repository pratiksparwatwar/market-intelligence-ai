# Market Intelligence AI

An AI-powered market intelligence platform that reads financial news, identifies market themes, and generates educational insights. Not an investment advisor.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, Tailwind CSS, TypeScript |
| Backend | FastAPI, Python 3.11 |
| Database | PostgreSQL (Neon) |
| AI | DeepSeek API (OpenAI-compatible) |
| Hosting | Render |

---

## Quick Start (Local)

### Prerequisites
- Python 3.11+
- Node.js 20+
- A Neon PostgreSQL database
- A DeepSeek API key

---

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and DEEPSEEK_API_KEY

# Start server
uvicorn app.main:app --reload --port 8000
```

The backend creates all database tables automatically on startup.

**Seed sample data (optional):**
```bash
python seed_data.py
```

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start dev server
npm run dev
```

Open http://localhost:3000

---

### 3. Test the full flow

1. Go to http://localhost:3000/admin
2. Click **"Fetch News"** — fetches articles from RSS feeds
3. Click **"Generate Themes"** — runs DeepSeek AI to identify themes
4. Go to http://localhost:3000/dashboard — see your themes!

---

## Environment Variables

### Backend (`backend/.env`)

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
DEEPSEEK_API_KEY=sk-your-key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
CORS_ORIGINS=http://localhost:3000,https://your-render-frontend.onrender.com
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Deploy to Render

### Backend (Web Service)

1. Create a new **Web Service** on Render
2. Connect your GitHub repo, set **Root Directory** to `backend`
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (from `.env.example`)

### Frontend (Web Service)

1. Create another **Web Service** on Render
2. **Root Directory:** `frontend`
3. **Build Command:** `npm install && npm run build`
4. **Start Command:** `npm start`
5. Add env var: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

### Database (Neon)

1. Create a Neon project at https://neon.tech
2. Copy the connection string
3. Set it as `DATABASE_URL` in your backend env vars
4. Tables are auto-created on first startup

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/articles` | List articles (filter by source) |
| GET | `/api/themes` | List themes (filter by sentiment, risk) |
| GET | `/api/themes/{id}` | Theme detail with source articles |
| GET | `/api/assets` | Asset overview with sentiment |
| GET | `/api/assets/{asset}/themes` | Themes for an asset |
| GET | `/api/assets/{asset}/articles` | Articles for an asset |
| POST | `/api/admin/fetch-news` | Trigger news ingestion |
| POST | `/api/admin/generate-themes` | Trigger AI theme generation |
| DELETE | `/api/admin/clear-data` | Clear all test data |
| GET | `/health` | Health check |

Interactive docs: http://localhost:8000/docs

---

## Pages

| Route | Description |
|-------|-------------|
| `/dashboard` | Main dashboard: themes, risk signals, assets, articles |
| `/themes` | All themes with sentiment/risk filters |
| `/themes/[id]` | Theme detail with supporting sources |
| `/assets` | Asset category overview |
| `/assets/[asset]` | Asset-specific themes and articles |
| `/sources` | All ingested articles with source filter |
| `/admin` | Admin panel: fetch news, generate themes, clear data |

---

## Adding New News Sources

Edit `backend/app/services/news_fetcher.py` and add to the `RSS_SOURCES` list:

```python
{
    "name": "Your Source Name",
    "url": "https://example.com/rss.xml",
    "asset_tags": ["Indian equity market"],
    "sector_tags": ["Banking"],
    "macro_tags": ["monetary policy"],
},
```

---

## Disclaimer

This platform provides market intelligence and educational insights only. It does not provide investment advice, buy/sell recommendations, or guaranteed predictions.
