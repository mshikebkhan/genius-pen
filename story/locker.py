#Import OS 
import os

#Import project settings
from django.conf import settings


def SaveCategoryCover(instance, filename):
    """topic Category will be uploaded to MEDIA_ROOT/TopicCoverImages/<topicname>/<cover.jpg>"""
    category_cover_name = f'website_data/categories_data/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, category_cover_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return category_cover_name


def SaveDraftCover(instance, filename):
    """Draft will be uploaded to custom a directory"""
    draft_cover_name = f'user_data/{instance.user}/stories_data/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, draft_cover_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return draft_cover_name

def SaveStoryCover(instance, filename):
    """Story will be uploaded to custom a directory"""
    story_cover_name = f'user_data/{instance.user}/stories_data/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, story_cover_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return story_cover_name    