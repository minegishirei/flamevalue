from django.urls import path
from . import views
urlpatterns = [
    path("", views.index ,name="index"),
    path("index.html", views.sitemap ,name="pop_page"),
    path("site", views.sitemap, name="pop_page"),
    path("robots.txt", views.robots, name="reload"),
    path("<category>/<yahoo_id>", views.page, name="page"),
    path("<category>/", views.category_list, name="category")

]
