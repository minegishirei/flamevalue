from django.urls import path
from . import views
switchPage = views.SwitchPage()
urlpatterns = [
    path('', switchPage.index , name="index"),
    path("index.html" , switchPage.index , name=''),
    path("robots.txt", switchPage.robots, name="robots"),
    path("sitemap.xml", switchPage.sitemap , name= ""),
    path("<htmlpage>" , switchPage.page , name=''),
]


