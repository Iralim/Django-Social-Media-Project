from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from profile_app.models import Profile
from profile_app.forms import  ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User


def index(request):
    return render (request,'index.html')

#view own profile
@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile_app/profile.html', {'profile': profile})

#update profile
@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)  # Get the profile for the logged-in user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():                     #validate the updated_form
            form.save()
            messages.success(request, "Your Profile is updated!!")
            return redirect('profile_app:profile')       #redirect to profile page
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile_app/update_profile.html', {'form': form, 'profile':profile})

#view other user's profile
@login_required
def view_others_profile(request, username):
    user = get_object_or_404(User,username=username) # Get the user of the post
    other_profile = Profile.objects.get(user=user)  # Get the profile of user
    return render(request, 'profile_app/view_profile.html', {'profile':other_profile})
