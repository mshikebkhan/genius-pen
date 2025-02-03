from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect, HttpResponseRedirect, reverse
from .models import Category, Draft, Story, Comment, Reply
from .forms import StoryForm
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from notifications.models import Notification


def UploadImage(request):
    files = request.FILES['image']
    fs = FileSystemStorage()
    filename = str(files).split('.')[0]
    file_ = fs.save(filename, files)
    fileurl = fs.url(file_)
    return JsonResponse({'success': 1, 'file': {'url': fileurl}})

@login_required
def Interest(request):
    """Interest Page"""
    user = request.user
    profile = user.profile
    categories = Category.objects.all()
    interest_categories = profile.interest_categories.all()
    context = {'categories': categories, 'interest_categories': interest_categories}
    return render(request, 'story/interest.html', context)

@login_required
def CategoryDetail(request, category):
    """Category Detail Page"""
    user = request.user
    profile = user.profile
    category = Category.objects.get(title=category.replace('-', ' '))
    stories = Story.objects.filter(category=category).all().order_by('date_created')
    interest_categories = profile.interest_categories.all()
    context = {'category': category, 'stories': stories, 'interest_categories': interest_categories}
    return render(request, 'story/category.html', context) 

@login_required
def FollowCategory(request, category_id):
    """Follow category"""
    category = get_object_or_404(Category, id=category_id)
    response_data={}
    if request.method == 'POST':
        my_profile = request.user.profile

        if category not in my_profile.interest_categories.all():#Check if i follow the category 
            my_profile.interest_categories.add(category)#If i dont then add category in my ineterest
            my_profile.save()

            category.followers.add(request.user)#And then add me in categories's followers
            category.save()

            response_data['status'] = 'followed'

        else:#Unfollow
            my_profile.interest_categories.remove(category)
            my_profile.save()

            category.followers.add(request.user)#And then add me in user's followers
            category.save()

            response_data['status'] = 'unfollowed'
        return JsonResponse(response_data)
    else:
        raise Http404 

@login_required
def CreateStory(request):
    """Create story page"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = StoryForm()
    else:
        # POST data submitted; process data.
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            draft  = form.save(commit=False)
            draft.user = request.user
            draft.save()
            messages.success(request, 'Your Story has been drafted successfully. You can publish anytime')
            return redirect('story:drafts')
        else:
            messages.error(request, f' Unable to craete! Please correct the error below.')

    context = {'form': form}
    return render(request, 'story/draft_form.html', context)

@login_required
def Drafts(request):
    """User raw stories"""
    user = request.user
    drafts = Draft.objects.filter(user=user).order_by('-date_created')
    drafts_count = drafts.count()

    context = {
    'drafts': drafts, 'drafts_count': drafts_count
    }

    return render(request, 'story/drafts.html', context)    

@login_required
def SavedStories(request):
    """User saved stories"""
    user = request.user
    profile = user.profile
    saved_stories = profile.saved_stories.all()
    saved_stories_count = saved_stories.count()

    context = {
    'stories': saved_stories, 'saved_stories_count': saved_stories_count
    }

    return render(request, 'story/saved_stories.html', context)  

@login_required
def ReadHistory(request):
    """User recently read stories"""
    user = request.user
    profile = user.profile
    read_history = list(profile.read_history.all())
    read_history.reverse()

    context = {
    'stories': read_history
    }

    return render(request, 'story/read_history.html', context) 

@login_required
def ClearReadHistory(request):
    """Clear recently read history list """
    if request.method == "POST":
        user = request.user
        profile = user.profile 
        profile.read_history.clear()
        profile.save()
        messages.success(request, f'Your read history has been cleared successfully.')
        return redirect('story:read-history')
    else:
        Http404

@login_required
def DraftDetail(request,draft_title, draft_id):
    """Draft detail page"""
    user = request.user
    draft = get_object_or_404(Draft, id=draft_id, user=user)

    context = {
    'draft': draft
    }

    return render(request, 'story/draft.html', context) 


@login_required
def DeleteDraft(request, draft_id):
    """Delete draft"""
    if request.method == "POST":
        user = request.user
        draft = get_object_or_404(Draft, id=draft_id, user=user)
        draft.delete()
        messages.success(request, f'Your Draft has been deleted successfully.')
        return redirect('story:drafts')
    else:
        Http404

@login_required
def UpdateDraft(request, draft_id):
    """Update draft"""
    user = request.user
    draft = get_object_or_404(Draft, id=draft_id, user=user)
    if request.method == 'POST':
        
        form = StoryForm(request.POST, request.FILES, instance=draft)

        if form.is_valid():
            draft  = form.save(commit=False)
            draft.date_updated = timezone.now()
            draft.save()
            messages.success(request, f'Your Draft has been updated successfully.')
            return HttpResponseRedirect(reverse('story:draft',args=[draft.title, draft.id]))
        else:
            messages.error(request, f' Unable to update. Please correct the error below.')
    else:
        form = StoryForm(instance=draft)

    context = {
       'form': form, 'mod': 'Update draft'
    }

    return render(request, 'story/story_form.html', context)
from django.core.files import File
from django.core.files.base import ContentFile
@login_required
def Publish(request, draft_id):
    """Publish darfted story"""
    if request.method == "POST":
        user = request.user
        draft =  get_object_or_404(Draft, id=draft_id)
        if user == draft.user:
            story = Story.objects.create(
                user=draft.user, category=draft.category,
                title=draft.title,
                content=draft.content,
                visibility=draft.visibility, 
                )
            if draft.cover:
                with open(draft.cover.path, 'rb', True) as f:
                    data = File(f)
                    story.cover.save(draft.cover.name, data, True)
            draft.delete()
            messages.success(request, 'Your Story has been published successfully.')
            return redirect('story:drafts')
        else:  
            messages.error(request, 'Unable to publish something went wrong!')
            return HttpResponseRedirect(reverse('story:draft',args=[draft.title, draft.id]))
    else:
        raise Http404

@login_required
def StoryDetail(request,story_title, story_id):
    """Story detail page"""
    user = request.user
    profile = user.profile

    story = get_object_or_404(Story, id=story_id)

    story.views +=1#Increase a view
    story.save()

    read_history = profile.read_history.all()

    if story not in read_history and read_history.count() < 100:
        profile.read_history.add(story)


    saved_stories = user.profile.saved_stories.all()
    liked_stories = user.profile.liked_stories.all()
    following_users = user.profile.following.all()     


    context = {
    'story': story, 'saved_stories': saved_stories, 'liked_stories': liked_stories, 'following_users': following_users
    }

    return render(request, 'story/story.html', context) 

@login_required
def Comments(request, story_id, anchor=None):
    """Comments on a story"""
    if anchor:
        anchor = int(anchor)
    story = get_object_or_404(Story, id=story_id)
    comments = Comment.objects.filter(story=story).order_by('-date_created')
    context = {'story': story, 'comments': comments, 'anchor': anchor,}
    return render(request, 'story/comments.html', context)

@login_required
def Replies(request, comment_id, anchor=None):
    """Replies on a comment"""
    if anchor:
        anchor = int(anchor)
    comment = get_object_or_404(Comment, id=comment_id)
    replies = Reply.objects.filter(comment=comment).order_by('-date_created')
    context = {'comment': comment, 'replies': replies, 'anchor': anchor}
    return render(request, 'story/replies.html', context)

@login_required
def AddComment(request, story_id):
    """Add comment with JS"""
    if request.method =="POST":
        response_data= {}
        story = get_object_or_404(Story, id=story_id)
        body = request.POST.get('body')
        if len(body) > 0 and len(body) < 501 :
            comment = Comment.objects.create(user=request.user, story=story, body=body)
            response_data['status'] = "added"
            response_data['user'] = comment.user.first_name+' '+comment.user.last_name
            response_data['profile_pic'] = comment.user.profile.profile_pic.url
            response_data['body'] = body
            response_data['id'] = comment.id
        else:
            response_data['status'] = 'error'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def ReportComment(request, comment_id):
    """Report Comment"""
    response_data={}
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.reported == False:
            if comment.user != request.user:
                comment.reported = True
                comment.save()
                response_data['status'] = 'reported'
            else:
                raise Http404
        else:
            response_data['status'] = 'already_reported' 
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def DeleteComment(request, comment_id):
    """Delete comment with JS"""
    if request.method =="POST":
        response_data= {}
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user == request.user:
            comment.delete()
            response_data['status'] = "deleted"
        else:
            response_data['status'] = 'error'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def AddReply(request, comment_id):
    """Add reply with JS"""
    if request.method =="POST":
        response_data= {}
        comment = get_object_or_404(Comment, id=comment_id)
        body = request.POST.get('body')
        if len(body) > 0 and len(body) < 501 :
            reply = Reply.objects.create(user=request.user, comment=comment, body=body)
            response_data['status'] = "added"
            response_data['user'] = reply.user.first_name+' '+reply.user.last_name
            response_data['profile_pic'] = reply.user.profile.profile_pic.url
            response_data['body'] = body
            response_data['id'] = reply.id
        else:
            response_data['status'] = 'error'
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def ReportReply(request, reply_id):
    """Report Reply"""
    response_data={}
    if request.method == 'POST':
        reply = get_object_or_404(Reply, id=reply_id)
        if reply.reported == False:
            if reply.user != request.user:
                reply.reported = True
                reply.save()
                response_data['status'] = 'reported'
            else:
                raise Http404
        else:
            response_data['status'] = 'already_reported' 
        return JsonResponse(response_data)
    else:
        raise Http404

@login_required
def DeleteReply(request, reply_id):
    """Delete reply with JS"""
    if request.method =="POST":
        response_data= {}
        reply = get_object_or_404(Reply, id=reply_id)
        if reply.user == request.user:
            reply.delete()
            response_data['status'] = "deleted"
        else:
            response_data['status'] = 'error'
        return JsonResponse(response_data)
    else:
        raise Http404

def DeleteStory(request, story_id):
    """Delete story"""
    if request.method == "POST":
        user = request.user
        story = get_object_or_404(Story, id=story_id, user=user)
        story.delete()
        messages.success(request, f'Your Story has been deleted successfully.')
        return redirect('users:profile')
    else:
        raise Http404

@login_required
def UpdateStory(request, story_id):
    """Update story"""
    user = request.user
    story = get_object_or_404(Story, id=story_id, user=user)
    if request.method == 'POST':
        
        form = StoryForm(request.POST, request.FILES, instance=story)

        if form.is_valid():
            story  = form.save(commit=False)
            story.date_updated = timezone.now()
            story.save()
            messages.success(request, f'Your Story has been updated successfully.')
            return HttpResponseRedirect(reverse('story:story',args=[story.title, story.id]))
        else:
            messages.error(request, f' Unable to update. Please correct the error below.')
    else:
        form = StoryForm(instance=story)

    context = {
       'form': form, 'mod': 'Update story', 'story_id':story_id,
    }

    return render(request, 'story/story_form.html', context)


@login_required
def SaveStory(request, story_id):
    """Save Story"""
    response_data={}
    if request.method == 'POST':
        story = get_object_or_404(Story, id=story_id)
        profile = request.user.profile
        if story not in profile.saved_stories.all():
            profile.saved_stories.add(story)
            profile.save()
            response_data['status'] = 'saved'
        else:
            profile.saved_stories.remove(story)
            profile.save()
            response_data['status'] = 'removed' 
        return JsonResponse(response_data)
    else:
        raise Http404 


@login_required
def ReportStory(request, story_id):
    """Report Story"""
    response_data={}
    if request.method == 'POST':
        story = get_object_or_404(Story, id=story_id)
        if story.reported == False:
            if story.user != request.user:
                story.reported = True
                story.save()
                response_data['status'] = 'reported'
            else:
                raise Http404
        else:
            response_data['status'] = 'error' 
        return JsonResponse(response_data)
    else:
        raise Http404 

@login_required
def LikeStory(request, story_id):
    """Like Story"""
    response_data={}
    if request.method == 'POST':
        story = get_object_or_404(Story, id=story_id, visibility="Public")
        profile = request.user.profile
        if story not in profile.liked_stories.all():
            profile.liked_stories.add(story)
            profile.save()
            story.likes += 1
            story.save()
            response_data['status'] = 'liked'
            response_data['likes_count'] = story.likes
            print(story.likes)

            #Notify user
            if story.user != request.user:
                notify = Notification(sender=request.user, story=story, user=story.user, notification_type=1)
                notify.save()

        else:
            profile.liked_stories.remove(story)
            profile.save()
            story.likes -= 1
            story.save()
            response_data['status'] = 'unliked'               
            response_data['likes_count'] = story.likes
            print(story.likes)

            #Delete notification on unlike
            notify = Notification.objects.filter(sender=request.user, story=story, user=story.user, notification_type=1)
            notify.delete()

        return JsonResponse(response_data)
    else:
        raise Http404 
