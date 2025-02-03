from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponseRedirect, JsonResponse, Http404
from story.models import Story
from notifications.models import Notification


def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)

			#Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
            password=request.POST['password2'])
            login(request, authenticated_user)
            messages.success(request, f'{first_name} your account has been created successfully. Please setup your profile!')
            return redirect('users:edit-profile')

        else:
            first_name = form.data.get('first_name')
            last_name = form.data.get('last_name')
            username = form.data.get('username')
            email = form.data.get('email')
            password = form.data.get('password1')               
            messages.error(request, f'Unable to create the account! Please correct the errors below.')

    else:
        form = SignUpForm()
        first_name = ''
        last_name = ''
        username = ''
        email = ''
        password = '' 

    	
    context = {
       'form': form, 'first_name': first_name, 'last_name': last_name, 'username': username, 'email':email, 'password': password
    }

    return render(request, 'users/signup.html', context)

@login_required
def LogOut(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required
def Profile(request, username=None):
    if username:#For other users
        user = get_object_or_404(User, username=username)
        profile = user.profile
        page_title = username

    else:#For current user
        profile = request.user.profile
        page_title = 'Profile'

    following_users = request.user.profile.following.all()
    stories = Story.objects.filter(user=profile.user).order_by('-date_created')
    context = {
    'page_title': page_title, 'profile': profile, 'stories': stories, 'following_users': following_users,
    }
    return render(request, 'users/profile.html', context)

@login_required
def EditProfilePage(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, f'Profile has been updated successfully.')
            return redirect('users:profile')
        else:
            messages.error(request, f' Unable to update profile. Please correct the error below.')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)
        

    context = {
       'uform': uform,
       'pform': pform
    }

    return render(request, 'users/edit_profile.html', context)

@login_required
def FollowUser(request, user_id):
    """Follow user"""
    user= get_object_or_404(User, id=user_id)
    response_data={}
    if request.method == 'POST' and user != request.user:
        user_profile = user.profile
        my_profile = request.user.profile

        if user not in my_profile.following.all():#Check if i follow the user 
            my_profile.following.add(user)#If i do then add user in my following
            my_profile.save()

            user_profile.followers.add(request.user)#And then add me in user's followers
            user_profile.save()

            #Notify user
            notify = Notification(sender=request.user, user=user, notification_type=4)
            notify.save()

            response_data['status'] = 'followed'

        else:#Unfollow
            my_profile.following.remove(user)
            my_profile.save()

            user_profile.followers.remove(request.user)#And then add me in user's followers
            user_profile.save()

            #Delete notification on unfollow
            notify = Notification.objects.filter(sender=request.user, user=user, notification_type=4)
            notify.delete()

            response_data['status'] = 'unfollowed'
        return JsonResponse(response_data)
    else:
        raise Http404 

@login_required
def Followers(request, username=None):
    if username:#For other users
        user = get_object_or_404(User, username=username)
        profile = user.profile
        page_title = username+'/Followers'

    else:#For current user
        profile = request.user.profile
        page_title = 'Followers'

    followers = profile.followers.all()
    following_users = request.user.profile.following.all()

    context = {
    'profile': profile, 'followers': followers, 'following_users': following_users,
    }
    return render(request, 'users/followers.html', context)


@login_required
def Following(request, username=None):
    if username:#For other users
        user = get_object_or_404(User, username=username)
        profile = user.profile
        page_title = username+'/Following'

    else:#For current user
        profile = request.user.profile
        page_title = 'Following'

    following = profile.following.all()
    following_users = request.user.profile.following.all()

    popular_users = []
    raw_popular_users = User.objects.all().order_by('-folllowers_users')
    for user in raw_popular_users:
        if user != request.user and user not in following_users:
            popular_users.append(user) 

    context = {
    'profile': profile, 'following': following, 'following_users': following_users, 'popular_users': popular_users,
    }
    return render(request, 'users/following.html', context)
