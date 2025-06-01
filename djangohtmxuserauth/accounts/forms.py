from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    given_name = forms.CharField(max_length=100, required=True)
    surname = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'given_name', 'surname')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                given_name=self.cleaned_data['given_name'],
                surname=self.cleaned_data['surname']
            )
        return user


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['given_name', 'surname']
        widgets = {
            'given_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['given_name'].label = 'First Name'
        self.fields['surname'].label = 'Last Name'
