from django.urls import path
from . import views


urlpatterns = [
    path("date/", views.current_datetime, name="date"),
    path("", views.index, name="index"),
    path("article/", views.testArticle, name="article"),
]
