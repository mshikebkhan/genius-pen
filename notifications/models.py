from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    """Display notifications."""
    NOTIFICATION_TYPES = ((1,'Like'),(2,'Comment'), (3,'Reply'), (4,'Follow'), (5,'Publish'))

    story = models.ForeignKey('story.Story', on_delete=models.CASCADE, related_name="noti_story", blank=True, null=True)
    comment = models.ForeignKey('story.Comment', on_delete=models.CASCADE, related_name="noti_comment", blank=True, null=True)
    reply = models.ForeignKey('story.Reply', on_delete=models.CASCADE, related_name="noti_reply", blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    preview = models.CharField(max_length=90, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

