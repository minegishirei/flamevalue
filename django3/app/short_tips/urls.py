from django.urls import path
from . import views
switchPage = views.SwitchPage()
urlpatterns = [
    path('', switchPage.index , name="index"),
    path("index.html" , switchPage.index , name=''),
    path('table_index.html', switchPage.table_index , name="table_index"),
    path("sql.html", switchPage.sql , name=""),
    path("<htmlpage>" , switchPage.page , name=''),
]


