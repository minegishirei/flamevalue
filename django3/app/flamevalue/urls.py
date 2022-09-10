from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name="index"), 
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("<htmlname>", views.index ,name="pop_page")
]

