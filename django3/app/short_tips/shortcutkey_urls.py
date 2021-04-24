from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path("<htmlpage>" , views.shortcutkey_page , name='')
]


