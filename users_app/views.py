from django.shortcuts import render, redirect
from users_app.forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from profile_app.models import Profile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import transaction

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('posts_app:all_posts')
    return render(request, 'index.html')


def user_register(request):
    registered = False

    if request.method == 'POST':
        user_reg_form = UserRegistrationForm(data=request.POST)

        if user_reg_form.is_valid():
            try: 
                with transaction.atomic():
                    user = User.objects.create_user(
                        username=user_reg_form.cleaned_data['username'], 
                        password=user_reg_form.cleaned_data['password'])
                    
                    #links user to a Profile model (so they can upload profile pics etc.)
                    Profile.objects.create(user=user,
                        age=user_reg_form.cleaned_data['age'],
                        gender=user_reg_form.cleaned_data['gender'])
                    
                    login(request, user)

                    registered = True
                    return redirect('profile_app:profile')
            except Exception as e: #maybe we want more specific error handling in the future
                print(f"Error during registration: {e}")
        else:
            print(user_reg_form.errors)
        
    else:
        user_reg_form = UserRegistrationForm()

    return render(request, 'registration_form.html', {
        'user_reg_form' : user_reg_form, 
        'registered' : registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('posts_app:all_posts')
            else:
                return HttpResponse('User not active')
            
        else:
            print(f"Login failed for user: {username}")
            return render(request, 'invalid_login.html')
    else:
        return render(request, 'login.html')
    
def user_timeout(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('posts_app:all_posts')
            else:
                return HttpResponse('User not active')
            
        else:
            print(f"Login failed for user: {username}")
            return render(request, 'invalid_login.html')
    else:
        return render(request, 'timeout.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect('users:index')
