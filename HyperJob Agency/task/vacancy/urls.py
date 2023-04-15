from django.urls import path
from .views import MainPageView, VacancyMainPageView, SignUpView, LoginView, LogoutView, home, NewVacancyView, NewResumeView

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('vacancies/', VacancyMainPageView.as_view(), name='vacancies'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('home/', home, name='home'),
    path('vacancy/new', NewVacancyView.as_view(), name='new'),
    path('resume/new', NewResumeView.as_view(), name='new'),
]
