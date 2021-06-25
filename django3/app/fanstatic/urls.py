from django.urls import path
from . import views
urlpatterns = [
    path('', views.page , name="index"), 
    path('page/<htmlname>', views.page , name="index"),
    #path("sitemap.xml", views.sitemap, name="sitemap"),
    #path("robots.txt", views.robots, name="robots"),
    #path("page/<htmlname>", views.page , name="page")
]

