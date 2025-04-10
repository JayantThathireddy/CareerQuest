from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

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

def loginPage(request):
    page = 'login'
    context = {'page': page}
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist.")
            return render(request, 'base/login_register.html', context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Password is incorrect.")

    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration.")
            print(form.errors)


    return render(request, 'base/login_register.html', {'form': form})

def description(request):
    return render(request, 'base/description.html')

def quiz_submit(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('quiz_results')) 
    else:
        return HttpResponseRedirect(reverse('quiz'))
