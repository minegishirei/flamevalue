from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name="index"), 
    path("index.html", views.index ,name="pop_page"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("page/<htmlname>/data_loading.html", views.data_loading, name="data_loading"),
    path('page/<htmlname>/<pagetype>', views.page , name="index"),
]

