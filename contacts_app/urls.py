from django.urls import path
from . import views

app_name = 'contacts_app'

urlpatterns = [
    path('view_profile/<int:user_id>', views.view_profile, name='view_profile'),
    path('view_friends', views.view_friends, name='view_friends'),
    path('view_users', views.view_users, name='view_users'),
    path('send_request/<int:user_id>/', views.send_request, name='send_request'),
    path('accept_request/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('cancel_friend_request/<int:to_user_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
]
