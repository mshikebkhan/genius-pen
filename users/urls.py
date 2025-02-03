from django.urls import path
from django.conf.urls import url
from .import views
from django.contrib.auth.views import LoginView

urlpatterns =[

#New user registration page.
path('signup', views.SignUp, name='signup'),

#Log In page.
path('login', LoginView.as_view(template_name='users/login.html'), name='login'),

#Log Out.
path('logout', views.LogOut, name='logout'),

#Profile Page
path('profile', views.Profile, name='profile'),

#Logged in user's Profile Page
path('<str:username>/profile', views.Profile, name='user-profile'),

#Edit Profile Page
path('edit-profile', views.EditProfilePage, name='edit-profile'),

#Follow User
path('follow-user/<str:user_id>/', views.FollowUser, name='follow-user'),

#Followers page
path('followers', views.Followers, name='followers'),

#Logged in user's Followers Page
path('<str:username>/followers', views.Followers, name='user-followers'),

#Following page
path('following', views.Following, name='following'),

#Logged in user's Following Page
path('<str:username>/following', views.Following, name='user-following'),

]
