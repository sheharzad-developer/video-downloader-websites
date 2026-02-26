# VPS Deployment Guide (UlaHost or equivalent)

This project is designed for a **VPS** (e.g. [UlaHost](https://ulahost.com), DigitalOcean, Linode, Vultr). **Shared hosting is not recommended** due to restrictions often applied to video/YouTube downloaders and the need to run a long-lived Django process.

## Requirements

- Ubuntu 22.04 LTS or Debian 12 (or equivalent)
- Root or sudo access
- Domain or IP pointing to the server

## 1. Server setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx
```

## 2. Project on the server

Upload the project (e.g. via Git or rsync) to a directory such as `/var/www/video-downloader/`:

```bash
cd /var/www
sudo git clone <your-repo-url> video-downloader
# or rsync/scp the project files
cd video-downloader
```

## 3. Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Environment variables

Create `/var/www/video-downloader/.env` (or export in systemd) with:

```bash
# Required for production
export SECRET_KEY='your-long-random-secret-key-here'
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com,api.yourdomain.com'
export DEBUG='False'

# Cobalt API (your instance; optional – defaults to public API)
export COBALT_API_URL='https://your-cobalt-instance.com'
```

Use a strong `SECRET_KEY` (e.g. `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`).

## 5. Django production settings

The project already reads `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` from the environment in `config/settings.py`. Set them in `.env` (see step 4), then run:

```bash
source .env  # or export variables another way
python manage.py check
python manage.py collectstatic --noinput  # if you add static files later
python manage.py migrate
```

## 6. Gunicorn

Run Django with Gunicorn:

```bash
# From project root, with venv activated
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 2 --threads 4
```

Test: `curl http://127.0.0.1:8000/api/download/` (should return 405 Method Not Allowed for GET; POST is allowed).

## 7. Systemd service

Create `/etc/systemd/system/video-downloader.service`:

```ini
[Unit]
Description=Video Downloader Django (Gunicorn)
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/video-downloader
EnvironmentFile=/var/www/video-downloader/.env
ExecStart=/var/www/video-downloader/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 2 --threads 4
Restart=always

[Install]
WantedBy=multi-user.target
```

Adjust `User`/`Group` and paths as needed. Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable video-downloader
sudo systemctl start video-downloader
sudo systemctl status video-downloader
```

## 8. Nginx reverse proxy

Create `/etc/nginx/sites-available/video-downloader`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static/ {
        alias /var/www/video-downloader/static/;
    }
}
```

Enable and reload:

```bash
sudo ln -s /etc/nginx/sites-available/video-downloader /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

Use Certbot for HTTPS:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 9. CORS (for WordPress integration)

If the Django API is on `api.yourdomain.com` and the form is on a WordPress site at `www.yourdomain.com`, the browser will enforce CORS. Two options:

**Option A – Nginx:** Add CORS headers for the API location:

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    add_header Access-Control-Allow-Origin "https://www.yourdomain.com" always;
    add_header Access-Control-Allow-Methods "POST, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Content-Type" always;

    if ($request_method = OPTIONS) {
        return 204;
    }
}
```

**Option B – Django:** Install `django-cors-headers`, add to `INSTALLED_APPS` and `MIDDLEWARE`, and set `CORS_ALLOWED_ORIGINS = ["https://www.yourdomain.com"]` in settings.

## 10. UlaHost compatibility

The steps above use standard Ubuntu/Debian, Nginx, and Gunicorn. On UlaHost (or any VPS with a similar stack):

- Use their control panel only for DNS/domain if you prefer; the app runs via systemd + Nginx as above.
- If they provide AAPanel, you can still run Gunicorn as a custom app and put Nginx (or AAPanel’s Nginx) in front with the same `proxy_pass` and optional CORS config.
- Ensure outbound HTTPS is allowed so Django can call `COBALT_API_URL`.

## Summary checklist

- [ ] VPS with Ubuntu/Debian, Python 3, Nginx
- [ ] Project deployed, venv created, `pip install -r requirements.txt`
- [ ] `.env` with `SECRET_KEY`, `ALLOWED_HOSTS`, `DEBUG=False`, optional `COBALT_API_URL`
- [ ] Django `migrate` and `check`
- [ ] Gunicorn systemd service running on 127.0.0.1:8000
- [ ] Nginx proxying to Gunicorn, HTTPS with Certbot
- [ ] CORS configured if the form is on WordPress on another domain
