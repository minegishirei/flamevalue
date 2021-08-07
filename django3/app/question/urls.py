from django.urls import path
from . import views
urlpatterns = [
    path("", views.index ,name="index"),
    path("index.html", views.sitemap ,name="pop_page"),
    path("sitemap2.xml", views.sitemap, name="pop_page"),
    path("<category>/<yahoo_id>", views.page, name="page"),
    path("<category>/", views.category_list, name="category")

]
