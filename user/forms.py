"""
This is the forms.py file the project uses 4 form input from user
"""

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import  Profile, Match



# pylint: disable=too-many-ancestors
class CreateUserForm(UserCreationForm):
    """
    This class used django model user to create a new user

"""
# pylint: disable=too-few-public-methods
    class Meta:
        """
        define the model and its attributes in form 
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    """
    This is the login form 
"""

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())




class UpdateUserForm(forms.ModelForm):
    """
this is the form to update user details
"""

    password = None
# pylint: disable=too-few-public-methods
    class Meta:
        """
        define the model and its attributes in form 
        """

        model = User
        fields = ['username', 'email',]
        exclude = ['password1', 'password2', ]




class UpdateProfileForm(forms.ModelForm):
    """
This is the form to update profile picture
"""

    profile_pic = forms.ImageField(widget=forms.FileInput(attrs = {'class': 'form-control-file'}))
# pylint: disable=too-few-public-methods
    class Meta:
        """
        define the model and its attributes in form 
        """
        model = Profile
        fields = ['profile_pic', ]


class AddMatchForm(forms.ModelForm):
    """
This form is used to create matches
"""
# pylint: disable=too-few-public-methods
    class Meta:
        """
        define the model and its attributes in form 
        """
        model = Match
        fields = ['team1', 'team2', 'venue']
