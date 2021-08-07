from django.urls import path
from . import views
urlpatterns = [
    path("", views.index ,name="index"),
    path("/sitemap.xml", views.sitemap, name="sitemap"),
    path("<category>/", views.category_list, name="category"),
    path("<category>/<yahoo_id>", views.page, name="page")
]

