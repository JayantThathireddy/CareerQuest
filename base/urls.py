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
    path('quiz/1/', views.quiz_page_1, name='quiz_page_1'),
    path('quiz/2/', views.quiz_page_2, name='quiz_page_2'),
    path('quiz/3/', views.quiz_page_3, name='quiz_page_3'),
    path('quiz/4/', views.quiz_page_4, name='quiz_page_4'),
    path('quiz/5/', views.quiz_page_5, name='quiz_page_5'),
    path('quiz/6/', views.quiz_page_6, name='quiz_page_6'),
    path('quiz/7/', views.quiz_page_7, name='quiz_page_7'),
    path('quiz/8/', views.quiz_page_8, name='quiz_page_8'),
    path('quiz/9/', views.quiz_page_9, name='quiz_page_9'),
    path('quiz/10/', views.quiz_page_10, name='quiz_page_10'),
    
    # 🔐 Login
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
]
