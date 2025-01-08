from .views import *
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
]
