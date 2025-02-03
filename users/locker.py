#Import OS 
import os

#Import project settings
from django.conf import settings

#Import User model
from django.contrib.auth.models import User


def SaveProfilePic(instance, filename):
    """profile_pic will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    profile_pic_name = f'user_data/{instance.user}/profile_data/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name

