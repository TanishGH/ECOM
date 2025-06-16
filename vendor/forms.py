from django import forms

from users.models import User
from .models import VendorProfile
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ['store_name', 'store_description', 'address']
        widgets = {
            'store_description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        
class VendorSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        user.is_active = False  # Deactivated until email is verified
        user.email_verification_token = get_random_string(50)
        if commit:
            user.save()
        return user

class VendorSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        user.is_active = False  # Deactivate until email is verified
        user.email_verification_token = get_random_string(50)
        if commit:
            user.save()
        return user

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        exclude = ('user', 'is_approved')
        model = VendorProfile
        exclude = ('user', 'is_approved')