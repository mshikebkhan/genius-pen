from django import forms
from .models import Draft, Category, Comment

#category_choices
category_choices = Category.objects.all().values_list('title', 'title')


#Visibility options
visibility_choices = (
    ('Public','Public'),
    ('Private', 'Private'),
    )

class StoryForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    visibility = forms.ChoiceField(choices=visibility_choices)
    category = forms.ChoiceField(choices=category_choices)
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), max_length=500, required=True)
    class Meta():
        model = Draft
        fields = ['title', 'cover', 'content', 'category', 'visibility']
        widgets = {
            'visibility': forms.Select(choices=visibility_choices),
            'category': forms.Select(choices=category_choices)
        }



class CommentForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), max_length=500, required=True)

	class Meta:
		model = Comment
		fields = ('body',)