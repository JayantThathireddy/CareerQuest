from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),  
    path('login/', views.login, name='login'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/submit/', views.quiz_submit, name='quiz_submit'),
    
    # 🔐 Login & Logout
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
]
