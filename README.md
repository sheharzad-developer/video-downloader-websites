# Video Downloader Websites

This project builds **six video downloader websites** with a single Django backend that uses the **Cobalt API**. Each site has its own front-end (HTML/CSS) with consistent layout and distinct branding (colors, fonts, buttons).

## The six websites

1. **TikTok Video Downloader** – TikTok-style / SSSTik-inspired layout (light theme, Paste/Clear/Download).
2. **Facebook Video Downloader** – Blue theme.
3. **Instagram Video Downloader** – Yellow/orange shades.
4. **YouTube Video Downloader** – Red theme.
5. **YouTube to MP3 Converter** – Same URL input; sends `downloadMode: "audio"` and `audioFormat: "mp3"` to get audio.
6. **All-in-One Downloader** – SaveFrom.net-style; one form handles all supported URLs (TikTok, Facebook, Instagram, YouTube, etc.).

Same API backend for all; Cobalt handles the actual downloads.

---

## Technical structure

### Front-end

- **HTML + CSS** only (no heavy JS frameworks).
- **Core layout is consistent** across all sites: one URL input, Download button, result area (link or error).
- **Per-site branding:** different colors, fonts, and button styles so each site feels unique while keeping the same structure (minimal impact on search rankings, fast to implement).
- **Examples:** TikTok page follows an SSSTik-style layout; Facebook uses a blue theme; Instagram uses yellow/orange; YouTube/YouTube to MP3 use red; All-in-One uses a purple accent.

### Back-end

- **Django (Python)** with one app that:
  - Serves the six downloader pages (each with its own theme).
  - Exposes a single API: **POST `/api/download/`** with JSON `{ "url": "https://..." }` and optional Cobalt params (`videoQuality`, `downloadMode`, `audioFormat`, etc.).
- **Cobalt API** is called from `downloader/services.py`; you can replace this with your own API later without changing views or URLs.
- Designed to run on **your own server** (VPS or AAPanel), not shared hosting.

---

## Content management options

1. **Django admin** – Use Django’s admin panel at `/admin/` for content and SSO-based management. Efficient when the whole stack is Django.
2. **WordPress** – Run WordPress on the same or another server. Embed the download form (HTML/JS) on WordPress pages; the form sends requests to your Django API URL (e.g. `https://api.yourdomain.com/api/download/`). You only need the form markup and the API URL; enable CORS on the Django side (or via Nginx) so the WordPress domain can call the API. See [DEPLOYMENT.md](DEPLOYMENT.md#9-cors-for-wordpress-integration).

---

## Hosting options

- **Shared hosting** is not used — restrictions (e.g. for YouTube downloaders) and the need to run a long-lived process rule it out for full Django.
- **VPS** (e.g. [UlaHost](https://ulahost.com)) — Run the full Django app with Gunicorn + Nginx. See **[DEPLOYMENT.md](DEPLOYMENT.md)** for step-by-step instructions (env vars, CORS for WordPress, etc.).
- **Vercel** — Deploy only the download API as a serverless function and the six pages as static HTML. No Django admin or full app. See **[VERCEL.md](VERCEL.md)** for deploy steps and limitations (e.g. timeout, cold starts).

---

## Local setup

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Optional: set your Cobalt instance URL (defaults to public API):

```bash
export COBALT_API_URL=https://your-cobalt-instance.com
```

Run:

```bash
python manage.py runserver
```

Then open:

- **TikTok:** http://127.0.0.1:8000/tiktok/
- **Facebook:** http://127.0.0.1:8000/facebook/
- **Instagram:** http://127.0.0.1:8000/instagram/
- **YouTube:** http://127.0.0.1:8000/youtube/
- **YouTube to MP3:** http://127.0.0.1:8000/youtube-mp3/
- **All-in-One:** http://127.0.0.1:8000/all-in-one/ or http://127.0.0.1:8000/

---

## API (for forms and WordPress)

**POST** `/api/download/`  

**Body (JSON):**  
`{ "url": "https://tiktok.com/...", "videoQuality": "720", "downloadMode": "auto" }`  

Optional Cobalt params: `audioFormat`, `downloadMode` (e.g. `"audio"` for MP3), `videoQuality`, etc.

**Response:** Cobalt JSON (e.g. `status`, `url`, `filename` or `error`).

Use this endpoint from the built-in HTML forms or from WordPress; the same form can be embedded on every site.

---

## Swapping to your own API

The Cobalt call lives in `downloader/services.py`. Replace `request_download()` to call your own API; views and URLs stay the same.

---

## Project layout

- `config/` – Django project settings and root URLs.
- `downloader/` – App: views, services (Cobalt), URL configs, templates.
- `downloader/templates/downloader/` – `base.html` (shared layout for Facebook, Instagram, YouTube, YouTube to MP3, All-in-One) and `ssstik_style.html` (TikTok-specific layout).
- `DEPLOYMENT.md` – VPS deployment (UlaHost or equivalent), Gunicorn, Nginx, CORS.
- `VERCEL.md` – Deploy to Vercel (static pages + serverless API only; no full Django).
