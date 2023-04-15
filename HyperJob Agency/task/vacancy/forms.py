from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Vacancy
from django.contrib.auth.models import User
from resume.models import Resume


class MyUserCreationForm(UserCreationForm):
    model = User

    username = forms.CharField(label='Username', max_length=30)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


class VacancyForm(forms.Form):
    model = Vacancy
    description = forms.CharField(label='Description', max_length=1000, widget=forms.Textarea(attrs={'rows': 5}))


class ResumeForm(forms.Form):
    model = Resume
    description = forms.CharField(label='Description', max_length=1000, widget=forms.Textarea(attrs={'rows': 5}))
