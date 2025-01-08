from .views import *
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('timeout/', user_timeout, name='timeout')
]
