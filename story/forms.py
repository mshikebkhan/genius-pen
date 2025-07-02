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
    category = forms.ChoiceField(choices=[])  # placeholder
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), max_length=500, required=True)

    class Meta:
        model = Draft
        fields = ['title', 'cover', 'content', 'category', 'visibility']
        widgets = {
            'visibility': forms.Select(choices=visibility_choices),
        }

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        try:
            self.fields['category'].choices = [
                (cat.title, cat.title) for cat in Category.objects.all()
            ]
        except:
            self.fields['category'].choices = []
	    
class CommentForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), max_length=500, required=True)

	class Meta:
		model = Comment
		fields = ('body',)
