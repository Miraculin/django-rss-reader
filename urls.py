from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^date/", views.current_datetime, name="date"),
    url(r"^$", views.index, name="index"),
    url(r"^article/", views.testArticle, name="article"),
]
