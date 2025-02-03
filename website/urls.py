from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authViews 

urlpatterns = [
    #Admin portal url config
    path('admin/', admin.site.urls),

    #Core url config
    path('', include(('core.urls', 'core'), namespace = 'core')),

    #Users url config
    path('', include(('users.urls', 'users'), namespace = 'users')),

    #Story url config
    path('', include(('story.urls', 'story'), namespace = 'story')), 

    #Notifications url config
    path('', include(('notifications.urls', 'notifications'), namespace = 'notifications')), 

    #Password reset
   	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password-reset'),
   	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)