from django.contrib import admin
from .models import FriendshipRequest, Friendship

# Register your models here.
admin.site.register(Friendship)
admin.site.register(FriendshipRequest)