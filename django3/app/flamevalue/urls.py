from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name="index"), 
    path("sitemap", views.sitemap, name="sitemap"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("robots.txt", views.robots, name="robots"),
    path("<htmlname>", views.index ,name="pop_page")
]

