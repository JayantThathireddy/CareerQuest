from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('quiz/<str:pk>/', views.quiz, name="quiz"),
    path('about/<str:pk>/', views.about, name="about"),
    
    # 🔐 Login & Logout
path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
]
