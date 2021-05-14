from django.urls import path
from . import views
switchPage = views.SwitchPage()
urlpatterns = [
    path('', switchPage.main , name="index"),
    path("index.html" , views.index , name=''),
    path('table_index.html', switchPage.main , name="table_index"),
    path('buildable_index.html', switchPage.index , name="buildable_index"),
    path("<htmlpage>" , switchPage.main , name='')
]


