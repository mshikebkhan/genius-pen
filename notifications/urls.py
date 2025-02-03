from django.urls import path
from . import views

urlpatterns = [

#Notifications page
path('notifications', views.Notifications, name='notifications'),

#Clear notifications
path('clear-notifications', views.ClearNotifications, name='clear-notifications'),

]
