from django.urls import path
from .import views

urlpatterns =[
    #Home page
    path('', views.Home, name='home'),

    #About us page
    path('about-us', views.AboutUs, name='about-us'),

    #Privacy policy page
    path('privacy-policy', views.PrivacyPolicy, name='privacy-policy'),

    #Terms & conditions page
    path('terms-and-conditions', views.TermsAndConditions, name='terms-and-conditions'),


]