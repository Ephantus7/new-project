from django.urls import path
from .views import ResumeMainPage

urlpatterns = [
    path('resumes/', ResumeMainPage.as_view(), name='resumes'),
]
