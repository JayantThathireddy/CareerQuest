from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# from .models import Question  # Uncomment this when your Question model is ready

def home(request):
    return render(request, 'base/home.html')

def quiz(request):
    return render(request, 'base/quiz.html')  # Quiz intro page

def quiz_questions(request):
    # Sample placeholder context; replace with real data if you have a model
    # questions = Question.objects.all()
    questions = []  # or pass in dummy questions for now
    return render(request, 'base/quiz_questions.html', {'questions': questions})

def about(request):
    return render(request, 'base/about.html')

def login(request):
    return render(request, 'base/login.html')

def description(request):
    return render(request, 'base/description.html')

def quiz_submit(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('quiz_results')) 
    else:
        return HttpResponseRedirect(reverse('quiz'))
