from .models import FriendshipRequest

def friend_requests_count(request):
    if request.user.is_authenticated:
        return {
            'friend_requests_count': FriendshipRequest.objects.filter(
                to_user=request.user, status='pending'
            ).count()
        }
    return {}
