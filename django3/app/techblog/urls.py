from django.urls import path
from . import views
urlpatterns = [
    path("index.html", views.index ,name="index"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("page/<htmlname>", views.page, name="page")
]

