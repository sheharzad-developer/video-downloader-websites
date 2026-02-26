from django.urls import path
from . import views

app_name = "downloader"

urlpatterns = [
    path("tiktok/", views.downloader_page, {"site": "tiktok"}, name="tiktok"),
    path("facebook/", views.downloader_page, {"site": "facebook"}, name="facebook"),
    path("instagram/", views.downloader_page, {"site": "instagram"}, name="instagram"),
    path("youtube/", views.downloader_page, {"site": "youtube"}, name="youtube"),
    path("youtube-mp3/", views.downloader_page, {"site": "youtube_mp3"}, name="youtube_mp3"),
    path("all-in-one/", views.downloader_page, {"site": "all_in_one"}, name="all_in_one"),
    path("", views.downloader_page, {"site": "all_in_one"}, name="index"),
]
