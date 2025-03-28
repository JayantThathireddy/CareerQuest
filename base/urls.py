from django.urls import path
from .import views

urlpatterns=[
    path('', views.home, name="home"),
    path('quiz/<str:pk>/', views.quiz, name="quiz"),
    path('about/<str:pk>/', views.about, name="about"),
]