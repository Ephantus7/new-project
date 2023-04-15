from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Resume


class ResumeMainPage(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='index.html', context={'resumes': Resume.objects.all()})


