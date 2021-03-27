from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name="index"),
    path('<htmlpage>' , views.page , name='index'),
    #path('<msg>/<int:id>/', views.index, name='index')
    
]


