# Render deployment guide

This project can be hosted as two Render services:

- `bachelor-cardio-ai-api`: FastAPI backend
- `bachelor-cardio-ai-demo`: static Vite frontend

## Deploy

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint**.
3. Connect the GitHub repository.
4. Render will read `render.yaml` and create both services.
5. After the backend deploys, open:

```text
https://bachelor-cardio-ai-api.onrender.com/health
```

6. Open the frontend:

```text
https://bachelor-cardio-ai-demo.onrender.com
```

## If Render changes service URLs

Set these environment variables in Render:

Backend service:

```text
CORS_ALLOW_ORIGINS=https://your-frontend-url.onrender.com
```

Frontend service:

```text
VITE_API_BASE_URL=https://your-backend-url.onrender.com
```

Then redeploy both services.

## Presentation note

Free hosted services can sleep after inactivity. Open `/health` a few minutes before the presentation so the backend wakes up before the live demo.
