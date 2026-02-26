import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET

from .services import request_download

# Site config: slug -> { name, theme_slug, post_payload }
SITES = {
    "tiktok": {"name": "TikTok", "theme_slug": "tiktok", "post_payload": {}},
    "facebook": {"name": "Facebook", "theme_slug": "facebook", "post_payload": {}},
    "instagram": {"name": "Instagram", "theme_slug": "instagram", "post_payload": {}},
    "youtube": {"name": "YouTube", "theme_slug": "youtube", "post_payload": {}},
    "youtube_mp3": {
        "name": "YouTube to MP3",
        "theme_slug": "youtube-mp3",
        "post_payload": {"downloadMode": "audio", "audioFormat": "mp3"},
    },
    "all_in_one": {"name": "All-in-One", "theme_slug": "all-in-one", "post_payload": {}},
}


@require_GET
def downloader_page(request, site):
    """Render the downloader form page for a given site (tiktok, facebook, etc.)."""
    config = SITES.get(site)
    if not config:
        return JsonResponse({"error": "Not found"}, status=404)

    context = {
        "site_name": config["name"],
        "theme_slug": config["theme_slug"],
        "post_payload_json": json.dumps(config["post_payload"]),
        "api_url": request.build_absolute_uri(reverse("api_download")),
    }
    template = "downloader/ssstik_style.html" if site == "tiktok" else "downloader/base.html"
    return render(request, template, context)


@csrf_exempt
@require_http_methods(["POST"])
def api_download(request):
    """
    API for the downloader form. Expects JSON: { "url": "https://..." }
    Optional: videoQuality, audioFormat, downloadMode, etc. (Cobalt params).
    Returns Cobalt response (download link or error).
    """
    try:
        data = json.loads(request.body or "{}")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse(
            {"status": "error", "error": {"code": "invalid_json"}},
            status=400,
        )
    url = data.get("url", "").strip()
    if not url:
        return JsonResponse(
            {"status": "error", "error": {"code": "missing_url"}},
            status=400,
        )
    options = {k: v for k, v in data.items() if k != "url" and v is not None}
    result = request_download(url, **options)
    return JsonResponse(result)
