"""
Cobalt API integration. Uses a single service layer so you can swap
to your own API later without changing views.
"""
import os
import requests


def get_cobalt_url():
    """Cobalt API base URL from env; default for local dev."""
    return os.environ.get("COBALT_API_URL", "https://api.cobalt.tools").rstrip("/")


def request_download(url: str, **options) -> dict:
    """
    Send a download request to Cobalt API.
    url: the media URL (TikTok, YouTube, Instagram, etc.)
    options: optional Cobalt params (videoQuality, audioFormat, downloadMode, etc.)
    Returns the API JSON response (status, url, filename, or error).
    """
    api_url = f"{get_cobalt_url()}/"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {"url": url, **options}
    try:
        r = requests.post(api_url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        return {"status": "error", "error": {"code": "request_failed", "context": str(e)}}
