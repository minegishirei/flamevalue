from django.urls import path
from . import views

urlpatterns = [
    path('<htmlpage>' , views.page , name='index'),
    #path('<msg>/<int:id>/', views.index, name='index')
    
]


