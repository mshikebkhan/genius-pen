from django.db import models
#Importing validators to validate min lentghs.
from django.core.validators import MinLengthValidator
from .locker import SaveCategoryCover, SaveDraftCover, SaveStoryCover
from django.contrib.auth.models import User
from PIL import Image
from .validators import CoverImageValidator

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from notifications.models import Notification

from django.db.models.signals import post_save, post_delete
#from django.dispatch import receiver
from django_cleanup import cleanup

class Category(models.Model):
    """Category to which articles are connected"""
    title = models.CharField(max_length=100, null=True)
    cover = models.ImageField()
    followers = models.ManyToManyField(User, blank=True, related_name="category_folllowers_users") 
    date_created=models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
    	return self.title

#Visiblity options
visibility_choices = (
    ('Public','Public'),
    ('Private', 'Private'),
    )


class Draft(models.Model):
    """Raw story"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300)
    cover = models.ImageField(null=True, blank=True, validators=[CoverImageValidator], upload_to='story_covers')    
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=10000)
    visibility = models.CharField(max_length=100, choices=visibility_choices, default="Public")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title[:90]


    def save(self, *args, **kwargs):
        super(Draft, self).save(*args, **kwargs)
        if self.cover:
            img = Image.open(self.cover.path)

            if img.height > 1200 or img.width> 720:
                output_size = (1200, 720)
                img.thumbnail(output_size)
                img.save(self.cover.path)  

class Story(models.Model):
    """Published story"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=300)
    cover = models.ImageField(null=True, blank=True, validators=[CoverImageValidator])    
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=10000)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    visibility = models.CharField(max_length=100, choices=visibility_choices, default="Public")
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "Stories"

    def user_publish_story(sender, instance, created, *args, **kwargs):
        """add notifications to all followers + resize story cover if it exists"""
        if created:
            story = instance
            sender = story.user
            followers = sender.profile.followers.all()

            for follower in followers:
                if story.visibility == "Public" :
                    notify = Notification(story=story,  sender=sender, user=follower, notification_type=5)
                    notify.save()          
        pass

    def user_delete_story(sender, instance, *args, **kwargs):
        """remove notifications from all followers if user deletes story."""
        story = instance
        sender = story.user
        notify = Notification(story=story,  sender=sender, notification_type=5)
        notify.delete()


    def comments_count(self):
        comments = Comment.objects.filter(story=self).count()
        return comments


    def __str__(self):
        return self.title[:90]
 


class Comment(models.Model):
    """Comments on story"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    story = models.ForeignKey(Story,on_delete=models.CASCADE) 
    body = models.TextField(max_length=500)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    reported = models.BooleanField(default=False)
   
    def replies_count(self):
        replies = Reply.objects.filter(comment=self).count()
        return replies

    def user_comment_story(sender, instance, *args, **kwargs):
        """add notification if user add comment."""
        comment = instance
        story = comment.story
        if comment.user != story.user:
            preview = comment.body[:70]
            sender = comment.user
            notify = Notification(comment=comment, story=story,  sender=sender, user=story.user, preview=preview ,notification_type=2)
            notify.save()

    def user_del_comment_story(sender, instance, *args, **kwargs):
        """remove notification if user removes comment."""
        comment = instance
        story = comment.story
        sender = comment.user
        notify = Notification.objects.filter(comment=comment, sender=sender, notification_type=2)
        notify.delete()


    def __str__(self):
        return self.body[:90]


class Reply(models.Model):
    """Reply on comment"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE) 
    body = models.TextField(max_length=500)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    reported = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Replies"

    def user_reply_comment(sender, instance, *args, **kwargs):
        """add notification if user add reply."""
        reply = instance
        comment = reply.comment
        story = comment.story 
        if reply.user != comment.user:
            preview = reply.body[:70]
            sender = reply.user
            notify = Notification(reply=reply, comment=comment, story=story,  sender=sender, user=comment.user, preview=preview ,notification_type=3)
            notify.save()

    def user_del_reply_comment(sender, instance, *args, **kwargs):
        """remove notification if user removes reply."""
        reply = instance
        comment = reply.comment
        sender = reply.user
        notify = Notification.objects.filter(reply=reply, sender=sender, notification_type=3)
        notify.delete()

    def __str__(self):
        return self.body[:90]


#Comment notfy.
post_save.connect(Comment.user_comment_story, sender=Comment)
post_delete.connect(Comment.user_del_comment_story, sender=Comment)

#Reply notfy.
post_save.connect(Reply.user_reply_comment, sender=Reply)
post_delete.connect(Reply.user_del_reply_comment, sender=Reply)

#Publish story notfy.
post_save.connect(Story.user_publish_story, sender=Story)
post_delete.connect(Story.user_delete_story, sender=Story)          