"""
Export the six downloader pages as static HTML for Vercel.
Run: python manage.py export_vercel_pages
Writes to public/ (api_url will be /api/download for serverless).
"""
import json
import traceback
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from django.template import loader

from downloader.views import SITES


class Command(BaseCommand):
    help = "Export downloader pages to public/ for Vercel static deployment."

    def handle(self, *args, **options):
        try:
            self._export()
        except Exception as e:
            self.stderr.write(traceback.format_exc())
            raise

    def _export(self):
        base_dir = Path(settings.BASE_DIR)
        public_dir = base_dir / "public"
        public_dir.mkdir(parents=True, exist_ok=True)

        request = HttpRequest()
        request.META["SERVER_NAME"] = "localhost"
        request.META["SERVER_PORT"] = "80"
        request.META["REQUEST_METHOD"] = "GET"

        site_to_file = {
            "tiktok": "tiktok",
            "facebook": "facebook",
            "instagram": "instagram",
            "youtube": "youtube",
            "youtube_mp3": "youtube-mp3",
            "all_in_one": "index",
        }

        for site, config in SITES.items():
            template = "downloader/ssstik_style.html" if site == "tiktok" else "downloader/base.html"
            context = {
                "site_name": config["name"],
                "theme_slug": config["theme_slug"],
                "post_payload_json": json.dumps(config["post_payload"]),
                "api_url": "/api/download",
            }
            html = loader.render_to_string(template, context, request=request)
            out_file = public_dir / f"{site_to_file[site]}.html"
            out_file.write_text(html, encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"Wrote {out_file}"))

