from django.urls import path
from . import views
urlpatterns = [
    path("", views.index ,name="index"),
    path("index.html", views.index ,name="index"),
    path("robots.txt", views.robots ,name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("reload.html", views.reload, name="reload"),
    path("about.html", views.about, name="about"),
    path("<category>/<htmlname>", views.page, name="page"),
    path("<category_name>/", views.category_page, name="page")

]

