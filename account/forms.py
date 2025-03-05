from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(label='email', required=True)
    first_name = forms.CharField(label='name',required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'username', 'email']
        help_texts = {'username':''}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passwords don't match")
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
