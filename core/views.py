from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from story.models import Story
from django.contrib.auth.models import User
import random

def Home(request):
    """Home page"""

    if request.user.is_authenticated:

        user = request.user
        profile = user.profile
        following_users = profile.following.all()

        stories_from_following = []
        stories_from_interest = []

        stories = Story.objects.all().order_by('-date_created')
        for story in stories:
            if story.user in following_users and story.visibility == "Public":
                stories_from_following.append(story)

        interest_categories = profile.interest_categories.all()
        for story in stories:
            for category in interest_categories:
                if story.category == category.title and story.visibility == "Public":
                    stories_from_interest.append(story)

        list1 = set(stories_from_following)
        list2 = set(stories_from_interest)
        list3 = list1 - list2
        list4 = list(list1) 
        random.shuffle(list4)

        context = {'stories': list4}
    else:
        context = {}
    return render(request, 'core/home.html', context)

def AboutUs(request):
    """About us page"""
    return render(request, 'core/about-us.html')

def PrivacyPolicy(request):
    """Privacy Policy page"""
    return render(request, 'core/privacy-policy.html')

def TermsAndConditions(request):
    """Terms and Conditions"""
    return render(request, 'core/terms-and-conditions.html')


