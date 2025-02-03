from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.core.exceptions import ValidationError


forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']


class SignUpForm(UserCreationForm):
    """Sign Up form for new users."""
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name' , 'last_name' ,  'password1' , 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


    def clean(self):
 
        # data from the form is fetched using super function
        super(SignUpForm, self).clean()
         
        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        username_list = list(username)
        periods_list = ['/','"', "'", '!', '#', '*', '%', '$', '^', '&', '(', ')', '+', ',', '?', '\\' ]

 
        if username:

        # conditions to be met for the username length
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                'Minimum 3 characters required'])

            if username in forbidden_users:
                self._errors['username'] = self.error_class([
                'Invalid name for user, this is a reserverd word.'])

            for var in username:
                if var in  periods_list:
                    self._errors['username'] = self.error_class([
                    'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])

        if first_name:
            if len(first_name) < 2:
                self._errors['first_name'] = self.error_class([
                'Minimum 2 characters required'])

        if email:
            if User.objects.filter(email=email).exists():
                self._errors['email'] = self.error_class([
                'A user with this email already exists!'])

        # return any errors if found
        return self.cleaned_data


#Gender options
gender_choices = (
    ('Male','Male'),
    ('Female', 'Female'),
    )


class ProfileUpdateForm(forms.ModelForm):
    """Form to update/edit profile."""
    gender = forms.ChoiceField(choices=gender_choices)
    class Meta:
        model = Profile
        fields = ['profile_pic', 'gender', 'bio', 'facebook', 'twitter', 'instagram', 'youtube']
        widgets = {
        'gender': forms.Select(choices=gender_choices),
        }



class UserUpdateForm(forms.ModelForm):
    """Update user details."""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username','first_name' , 'last_name', 'email']

    def clean(self):
 
        # data from the form is fetched using super function
        super(UserUpdateForm, self).clean()
         
        # extract the username and text field from the data
        first_name = self.cleaned_data.get('first_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        username_list = list(username)
        periods_list = ['/','"', "'", '!', '#', '*', '%', '$', '^', '&', '(', ')', '+', ',', '?', '\\' ]

 
        if username:

        # conditions to be met for the username length
            if len(username) < 3:
                self._errors['username'] = self.error_class([
                'Minimum 3 characters required'])

            for var in username:
                if var in  periods_list:
                    self._errors['username'] = self.error_class([
                    'Enter a valid username. This value may contain only letters, numbers, and @ . _ etc characters.'])

        if first_name:
            if len(first_name) < 2:
                self._errors['first_name'] = self.error_class([
                'Minimum 2 characters required'])

        if email:
            if User.objects.filter(email=email).exists():
                user_obj = User.objects.get(email=email)
                if user_obj.username != username:
                    self._errors['email'] = self.error_class([
                    'A user with this email already exists!'])

        # return any errors if found
        return self.cleaned_data