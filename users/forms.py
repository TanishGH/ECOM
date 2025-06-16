from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_picture', 'phone_number')
        
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User  # or Profile if you have a separate profile model
        fields = ['first_name', 'last_name', 'email', 'username']  # Add other fields as needed
        # If you have profile picture in a separate Profile model:
        # fields = ['first_name', 'last_name', 'email', 'username', 'profile_picture']