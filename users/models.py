from django.db import models
from django.contrib.auth.models import User
from .locker import SaveProfilePic
#Importing validators to validate file sizes.
from .validators import ProfilePicSizeValidator
from story.models import Category, Story, Draft
from PIL import Image

#Gender options
gender_choices = (
    ('Male','Male'),
    ('Female', 'Female'),
    )

class Profile(models.Model):
    """User Profile"""
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, choices=gender_choices)
    profile_pic = models.ImageField(upload_to="profile_pics", default='website_data/default_profile_pic/default.png', validators=[ProfilePicSizeValidator])
    bio = models.TextField(max_length=300, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    youtube = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name="folllowers_users") 
    following = models.ManyToManyField(User, blank=True, related_name="following_users")
    interest_categories = models.ManyToManyField(Category, blank=True, related_name="interests_categories") 
    saved_stories = models.ManyToManyField(Story, blank=True, related_name="saved_stories") 
    liked_stories = models.ManyToManyField(Story, blank=True, related_name="liked_stories")
    read_history = models.ManyToManyField(Story, blank=True, related_name="read_history")       
    verified = models.BooleanField(default=False)

    def drafts_count(self):
        drafts = Draft.objects.filter(user=self.user).count()
        return drafts

    def stories_count(self):
        stories = Story.objects.filter(user=self.user).count()
        return stories

    def followers_count(self):
        followers = self.followers.all().count()
        return followers

    def following_count(self):
        following = self.following.all().count()
        return following        

    def saved_stories_count(self):
        saved_stories = self.saved_stories.all().count()
        return saved_stories

    def liked_stories_count(self):
        liked_stories = self.liked_stories.all().count()
        return liked_stories

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width> 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)        