"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from word_meanings_sentences import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('accounts/', include('allauth.urls')),

    # path('accounts/profile/',views.home, name='profile'),
    path('home/',views.home, name='home'),
    path('API_test/', views.API_test, name='API_test'),
    path('start/', views.start, name='start'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('accounts/logout/',views.logout, name='account_logout'),
    path('getword/', views.getword, name='getword'),
    path('end/', views.end, name='end'),
    path('checkSentence/', views.checkSentence, name='Sentence'),
    path('api-auth/', include('rest_framework.urls')),
    path('get/', views.getSentence)

    # path("", include("word_meanings_sentences.urls")),
   



    # Extra code
    # path('accounts/', include('allauth.urls')),
    # path('', TemplateView.as_view(template_name="index.html")),
    # path('logout', LogoutView.as_view()),
]


