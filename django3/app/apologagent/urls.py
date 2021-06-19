from django.urls import path
from . import views
urlpatterns = [
    path('index.html', views.index , name="index"),
    path("page/<htmlname>", views.page , name="page")
]




#https://webslides.tv/demos/portfolios#slide=8


