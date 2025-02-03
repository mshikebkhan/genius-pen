from django.urls import path

from django.conf.urls import url

from .import views


urlpatterns =[

#Follow Category
path('follow-category/<str:category_id>/', views.FollowCategory, name='follow-category'),

#Interests Page
path('interest', views.Interest, name='interest'),

#Category Detail Page
path('category/<str:category>', views.CategoryDetail, name='category'),

#Create story page
path('create-story', views.CreateStory, name='create-story'),

#User's raw stories Page
path('drafts', views.Drafts, name='drafts'),

#User's saved stories Page
path('saved-stories', views.SavedStories, name='saved-stories'),

#User's read history Page
path('read-history', views.ReadHistory, name='read-history'),

#Clear read story
path('clear-read-history', views.ClearReadHistory, name='clear-read-history'),

#Draft detail view
path('draft/<str:draft_title>/<str:draft_id>/', views.DraftDetail, name='draft'),

#Delete draft
path('delete-draft/<int:draft_id>', views.DeleteDraft, name='delete-draft'),

#Update draft
path('update-draft/<int:draft_id>', views.UpdateDraft, name='update-draft'),

#Publish draft
path('publish/<str:draft_id>/', views.Publish, name='publish'),

#Story detail view
path('story/<str:story_title>/<str:story_id>', views.StoryDetail, name='story'),

#Comments
path('comments/<str:story_id>', views.Comments, name='comments'),

#Comemnts page with #anchor
path('comments/<str:story_id>/<str:anchor>', views.Comments, name='comments'),

#Replies
path('replies/<str:comment_id>/', views.Replies, name='replies'),

#Replies page with anchor
path('replies/<str:comment_id>/<str:anchor>', views.Replies, name='replies'),

#Add a Comment
path('add-comment/<str:story_id>/', views.AddComment, name='add-comment'),

#Delete Comment with JS
path('delete-comment/<str:comment_id>/', views.DeleteComment, name='delete-comment'),

#Add a Reply
path('add-reply/<str:comment_id>/', views.AddReply, name='add-reply'),

#Delete Reply with JS
path('delete-reply/<str:reply_id>/', views.DeleteReply, name='delete-reply'),

#Delete story
path('delete-story/<int:story_id>', views.DeleteStory, name='delete-story'),

#Update story
path('update-story/<int:story_id>', views.UpdateStory, name='update-story'),

#Save story
path('save-story/<str:story_id>/', views.SaveStory, name='save-story'),

#Like story
path('like-story/<str:story_id>/', views.LikeStory, name='like-story'),

#Report story
path('report-story/<str:story_id>/', views.ReportStory, name='report-story'),

#Report Comment
path('report-comment/<str:comment_id>/', views.ReportComment, name='comment-story'),

#Report Reply
path('report-reply/<str:reply_id>/', views.ReportReply, name='report-reply'),

]