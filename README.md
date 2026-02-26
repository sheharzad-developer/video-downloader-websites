# Video Downloader Websites

Six video downloader sites (TikTok, Facebook, Instagram, YouTube, YouTube to MP3, All-in-One) with a single Django backend using the Cobalt API. Each site has its own front-end with consistent layout and distinct branding.

## Sites

- **TikTok** — `/tiktok`
- **Facebook** — `/facebook`
- **Instagram** — `/instagram`
- **YouTube** — `/youtube`
- **YouTube to MP3** — `/youtube-mp3`
- **All-in-One** — `/` or `/all-in-one`

Same API backend for all; Cobalt handles the downloads.

## Local setup

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Optional: set your Cobalt instance URL

```bash
export COBALT_API_URL=https://your-cobalt-instance.com
```

Run:

```bash
python manage.py runserver
```

## API

**POST** `/api/download/`  
Body (JSON): `{ "url": "https://...", "videoQuality": "720", "downloadMode": "auto" }`  
Optional: `audioFormat`, `downloadMode` (e.g. `"audio"` for MP3), `videoQuality`.

Response: Cobalt JSON (e.g. `status`, `url`, `filename` or `error`).

## Deploy

- **Vercel:** Static pages in `public/` + serverless `/api/download`. Set Build Command to a no-op and use committed `public/`. Add `COBALT_API_URL` in env if needed.
- **VPS:** Django + Gunicorn + Nginx; set `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG=False`, `COBALT_API_URL` in env.

To regenerate static pages for Vercel: `python manage.py export_vercel_pages`, then commit `public/`.
