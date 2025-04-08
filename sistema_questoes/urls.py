from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from django.contrib import admin
from django.urls import path, include
from quiz import views as quiz_views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', quiz_views.pagina_inicial, name='pagina_inicial'),
    path('quiz/', quiz_views.quiz, name='quiz'),
    path('quiz/<int:questao_id>/responder/', quiz_views.responder, name='responder'),
    path('relatorio/', quiz_views.relatorio, name='relatorio'),
    path('flashcards/', quiz_views.flashcards_view, name='flashcards'),
    path('login/', auth_views.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='quiz/login'), name='logout'),
    path('register/', quiz_views.register, name='register'),


]
