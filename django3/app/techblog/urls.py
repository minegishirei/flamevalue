from django.urls import path
from . import views, views_markdown
urlpatterns = [
    path("", views.index ,name="index"),
    path("index.html", views.index ,name="index"),
    path("robots.txt", views.robots ,name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
    path("markdown_check.html", views_markdown.markdown_check, name="markdown"),
    path("edit.html", views_markdown.edit, name="edit"),
    path("<category>/<htmlname>", views.page, name="page"),
    path("about.html/", views.about, name="about"),
    path("<category_name>/", views.category_page, name="page"),
]

