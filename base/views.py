from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def quiz(request):
    return render(request, 'base/quiz.html')

def about(request):
    return render(request, 'base/about.html')

def login(request):
    return render(request, 'base/login.html')

def quiz_submit(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('quiz_results')) 
    else:
        
        return HttpResponseRedirect(reverse('quiz'))
