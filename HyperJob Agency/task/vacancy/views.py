from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import MyUserCreationForm, VacancyForm, ResumeForm
from .models import Vacancy
from resume.models import Resume


class MainPageView(TemplateView):
    template_name = 'main.html'


class VacancyMainPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, template_name='vacancy.html', context={'vacancies': Vacancy.objects.all()})


class SignUpView(TemplateView):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = MyUserCreationForm()
        return render(request=request, template_name="signup.html", context={"form": form})

    def post(self, request, *args, **kwargs):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
        return render(request=request, template_name="signup.html", context={"form": form})


class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, template_name="login.html", context={'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            return render(request, template_name="login.html", context={'form': form})
        return render(request, template_name="login.html", context={'form': form})


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponse("You have successfully logged out.")


@login_required(login_url='login')
def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'home.html', context={'vacancies': Vacancy.objects.all(),
                                                         'resumes': Resume.objects.all()})
        else:
            return redirect('login')


class NewVacancyView(LoginRequiredMixin, TemplateView):

    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'new_vacancy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VacancyForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            form = VacancyForm(request.POST)
            if form.is_valid():
                vacancy = form.cleaned_data['description']
                author = User.objects.get(username=request.user.username)
                Vacancy.objects.create(description=vacancy, author=author)

                return redirect('home')
            return render(request, 'new_vacancy.html', {'form': form})

        return HttpResponseForbidden(status=403)


class NewResumeView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'new_resume.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResumeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.cleaned_data['description']
            author = User.objects.get(username=request.user.username)
            Resume.objects.create(description=resume, author=author)

            return redirect('home')
        return render(request, 'new_resume.html', {'form': form})

