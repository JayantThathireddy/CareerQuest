from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('set-dark-mode/', views.set_dark_mode, name='set-dark-mode'),
    path('about/', views.about, name='about'),  
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('profile-settings/', views.profile_settings, name='profile-settings'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/questions/', views.quiz_questions, name='quiz_questions'),
    path('description/', views.description, name='description'),
    path('quiz/submit/', views.quiz_submit, name='quiz_submit'),
    path('quiz/1/', views.quiz_page_1, name='quiz_page_1'),
    path('quiz/2/', views.quiz_page_2, name='quiz_page_2'),
    path('quiz/3/', views.quiz_page_3, name='quiz_page_3'),
    path('quiz/4/', views.quiz_page_4, name='quiz_page_4'),
    path('quiz/5/', views.quiz_page_5, name='quiz_page_5'),
    path('quiz/results/', views.quiz_results, name='quiz_results'),
    path('quiz/save-results/', views.save_results, name='save_results'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    
    path('career_description/', views.career_description, name='career_details'),

    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)