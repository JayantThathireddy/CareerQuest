from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),  
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('quiz/', views.quiz, name='quiz'),  # Quiz intro page
    path('quiz/questions/', views.quiz_questions, name='quiz_questions'),  # ✅ New quiz-taking page
    path('description/', views.description, name='description'),
    path('quiz/submit/', views.quiz_submit, name='quiz_submit'),
    
    # 🔐 Login
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
]
