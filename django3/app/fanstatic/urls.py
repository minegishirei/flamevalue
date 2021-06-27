from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name="index"), 
    path("index.html", views.index ,name="pop_page"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("pop_page.html", views.pop_page ,name="pop_page"),
    path("all_page.html", views.all_page ,name="all_page"),
    path("page/<htmlname>/data_loading.html", views.data_loading, name="data_loading"),
    path('page/<htmlname>/<pagetype>', views.page , name="index"),
    
    #path("sitemap.xml", views.sitemap, name="sitemap"),
    #path("robots.txt", views.robots, name="robots"),
    #path("page/<htmlname>", views.page , name="page")
]

