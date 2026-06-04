---
name: deploy-stack
description: Deploy the full FRK stack — frontend to Netlify, backend to Render
triggers:
  - "/deploy"
  - "deploy"
inputs:
  environment: "production"
exit_criteria:
  - "Frontend deployed to Netlify"
  - "Backend deployed to Render"
  - "Health endpoint responds 200"
---

# Deploy Stack Workflow

## Phase 1: Verify Readiness
Run `pytest tests/ -v -W error::DeprecationWarning` — all 117 must pass.

Check `render.yaml` is present and correctly configured.

Check `frontend/index.html` and `app.js` are clean (no localhost URLs).

## Phase 2: Deploy Backend (Render)
Commit and push to GitHub. Render auto-deploys from `render.yaml`.

Verify: `curl -f https://frk-api.onrender.com/health`

## Phase 3: Deploy Frontend (Netlify)
The `frontend/` directory can be dragged to Netlify's deploy UI.
Or use Netlify CLI: `netlify deploy --prod --dir frontend/`

Verify the deployed URL loads with dashboard + traditional foods pages.

## Phase 4: Verify Integration
Confirm frontend API calls reach the backend.
Check CORS headers are correct.
Test `/api/v1/traditional-foods/list` returns data.
