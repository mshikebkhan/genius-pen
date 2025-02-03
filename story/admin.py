from django.contrib import admin
from .models import Category, Draft, Story, Comment

admin.site.register(Category)
admin.site.register(Draft)
admin.site.register(Story)
admin.site.register(Comment)