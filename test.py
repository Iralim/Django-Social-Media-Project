import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_project.settings')
django.setup()
from django.contrib.auth.models import User

from contacts_app.models import FriendshipRequest

if __name__ == '__main__':

    friendship_request = FriendshipRequest.objects.all()
    print(friendship_request)

    user = User.objects.get(id=1)

    print(friendship_request.obj)
    
