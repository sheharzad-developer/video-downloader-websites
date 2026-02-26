from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_download, name="api_download"),
]
