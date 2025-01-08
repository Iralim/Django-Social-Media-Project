from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User

from .services import send_friend_request, accept_friend_request, reject_friend_request
from .models import Friendship, FriendshipRequest



# Create your views here.
@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user == user:
        return redirect('profile_app:profile')
    
    friendship_status, request_id = FriendshipRequest.friendship_status(request.user, user)
    is_friend = FriendshipRequest.are_friends(request.user, user)

    user_info = {'user': user,
                'profile': user.profile,
                'is_friend': is_friend, 
                'friendship_status': friendship_status, 
                'request_id': request_id,
                }

    return render(request, 'contacts_app/view_profile.html', {'user_info': user_info, 'profile': request.user.profile})


@login_required
def view_users(request):
    users_info_list = []
    users = User.objects.exclude(id=request.user.id).order_by('-date_joined')

    for user in users:
        is_friend = FriendshipRequest.are_friends(request.user, user)
        friendship_status, request_id = FriendshipRequest.friendship_status(request.user, user)
        users_info_list.append({'user': user,
                                'profile': user.profile,
                                'is_friend': is_friend,
                                'friendship_status': friendship_status,
                                'request_id': request_id})
    
    return render(request, 'contacts_app/view_users.html', {'users_info_list': users_info_list, 'profile': request.user.profile})


@login_required
def view_friends(request):
    user = request.user
    users_info_list = []

    friend_requests_queryset = FriendshipRequest.objects.filter(to_user=user)
    friend_requests = [request.from_user for request in friend_requests_queryset]
    friends = list(user.profile.friends)

    users = friend_requests + friends
    
    for user in users:
        is_friend = FriendshipRequest.are_friends(request.user, user)
        friendship_status, request_id = FriendshipRequest.friendship_status(request.user, user)
        users_info_list.append({
            'user': user,
            'profile': user.profile,
            'is_friend': is_friend,
            'friendship_status': friendship_status,
            'request_id': request_id
        })


    return render(request, 'contacts_app/view_friends.html', {'users_info_list': users_info_list, 'profile': request.user.profile})


@login_required
def send_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)

    message = send_friend_request(request.user, to_user)

    next_url = request.POST.get('next', '/')
    return redirect(next_url)


@login_required
def accept_request(request, request_id):
    message = accept_friend_request(request_id)
    next_url = request.POST.get('next', '/')
    return redirect(next_url)


@login_required
def reject_request(request, request_id):
    message = reject_friend_request(request_id)
    next_url = request.POST.get('next', '/')
    return redirect(next_url)


def cancel_friend_request(request, to_user_id):
    from_user = request.user
    to_user = User.objects.get(id=to_user_id)
    profile = to_user.profile
    
    try:
        friend_request = FriendshipRequest.objects.get(from_user=from_user, to_user=to_user, status='pending')
        friend_request.delete()
        next_url = request.POST.get('next', '/')
        return redirect(next_url)  
    
    except FriendshipRequest.DoesNotExist:
        return HttpResponse("The friend request was not found or has already been accepted/rejected.")


def remove_friend(request, friend_id):
    
    try:
        friend_to_remove = User.objects.get(id=friend_id)
        friendship = Friendship.objects.get(
            Q(user1=request.user, user2=friend_to_remove) | Q(user1=friend_to_remove, user2=request.user)
        )
        friendship.delete()

        next_url = request.POST.get('next', '/')
        return redirect(next_url, user_id=friend_id)
    
    except Friendship.DoesNotExist:
        return HttpResponse("Friendship record not found.")

