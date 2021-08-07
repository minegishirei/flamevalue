from django.urls import path
from . import views
urlpatterns = [
    path("", views.index ,name="index"),
    path("index.html", views.index ,name="pop_page"),
    path("<page>", views.sitemap, name="page"),
    path("<category>/", views.category_list, name="category"),
    path("<category>/<yahoo_id>", views.page, name="page"),

]
