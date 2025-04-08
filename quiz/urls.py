from django.urls import path
from . import views

urlpatterns = [
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/<int:questao_id>/responder/', views.responder, name='responder'),
]
