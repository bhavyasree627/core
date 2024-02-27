from home.views import index,person,login
from django.urls import path

urlpatterns = [
    path('index/', index),
    path('person/',person),
    path('login/',login)
]
