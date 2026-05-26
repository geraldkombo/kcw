# KCW Deployment Guide — Lovable Frontend + Render Backend

## Architecture

```
Lovable ── hosts frontend dashboard (free)
Render  ── hosts backend API (free)
```

The frontend communicates with the backend via the `API_BASE` variable in `app.js`.

---

## Step 1: Deploy Backend to Render (Free)

1. Push this repo to GitHub
2. Go to https://render.com → New Web Service → Connect your GitHub repo
3. Settings:
   - **Name**: `kcw-api`
   - **Region**: Ohio (US East) — closest to Kenya
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`
   - **Plan**: Free
4. In Environment Variables, add:
   - `DATABASE_URL` = `sqlite:///data/kcw.db` (SQLite is file-based; Render ephemeral storage resets on restart — ok for demo)
   - `LOG_LEVEL` = `INFO`
   - `CORS_ORIGINS` = `*` (allows Lovable frontend to call API)
5. Deploy → wait 2-3 minutes
6. Your API is live at `https://kcw-api.onrender.com`

> **Note**: Render's free tier spins down after 15 min idle. First request after idle takes ~30s to wake. Fine for demo/pitch.

## Step 2: Upload Frontend to Lovable (Free)

1. Go to https://lovable.dev/projects
2. Click "Create Project" → "Import from ZIP"
3. Upload `kcw.zip` (includes backend + frontend code)
4. Paste the contents of `KCW_LOVABLE_SYSTEM_PROMPT.md` as the project prompt
5. Click "Create"
6. Lovable generates the production dashboard

## Step 3: Connect Frontend to Backend

1. In the Lovable project, open `app.js`
2. Find `const API_BASE =` at the top
3. Change it to `const API_BASE = 'https://kcw-api.onrender.com'`
4. Deploy the Lovable project

## Step 4: Verify

- Open your Lovable project URL
- Dashboard should load real data from the Render API
- If the API is asleep (first request), wait ~30s and refresh
- Precision Farming page will fetch live NASA POWER satellite data

## Testing Changes

```bash
# Backend tests
pytest tests/ -v -W error::DeprecationWarning

# Start API locally (for frontend dev)
uvicorn api.main:app --reload --port 8000
```

## File Structure for Lovable

```
kcw/
├── frontend/        # Your target — Lovable rewrites this
├── lovable/         # Prompts and instructions (read-only reference)
├── api/             # FastAPI backend (do not modify via Lovable)
├── agents/          # AI agents (do not modify)
├── tests/           # 105 tests
├── Dockerfile       # Alternative: Docker deployment
├── docker-compose.yml
└── requirements.txt
```
