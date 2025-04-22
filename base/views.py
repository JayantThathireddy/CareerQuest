from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import JsonResponse

def set_dark_mode(request):
    if request.method == "POST":
        dark_mode = request.POST.get('dark_mode', 'false') == 'true'
        request.session['dark_mode'] = dark_mode
        return JsonResponse({'status': 'success', 'dark_mode': dark_mode})
    return JsonResponse({'status': 'error'}, status=400)



def home(request):
    dark_mode = request.session.get('dark_mode', False)
    return render(request, 'base/home.html', {'dark_mode': dark_mode})

def quiz(request):
    dark_mode = request.session.get('dark_mode', False)
    return render(request, 'base/quiz.html', {'dark_mode': dark_mode})  

def quiz_questions(request):
    
    questions = []  
    return render(request, 'base/quiz_questions.html', {'questions': questions})

def about(request):
    dark_mode = request.session.get('dark_mode', False)
    return render(request, 'base/about.html', {'dark_mode': dark_mode})

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

@login_required
def profile_settings(request):
    profile = request.user.profile

    if request.method == 'POST':
        if 'delete_account' in request.POST:
            request.user.delete()
            return redirect('home')

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-settings')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'base/profile-settings.html', {'form': form})

def quiz_page_1(request):
    if request.method == "POST":
        required = ['q1', 'q2', 'q3', 'q4', 'q5']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions.html')
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        return redirect('quiz_page_2')
    return render(request, 'base/quiz_questions.html')

def quiz_page_2(request):
    if request.method == "POST":
        required = ['q6', 'q7', 'q8', 'q9', 'q10']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions2.html')
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        return redirect('quiz_page_3')
    return render(request, 'base/quiz_questions2.html')

def quiz_page_3(request):
    if request.method == "POST":
        required = ['q11', 'q12', 'q13', 'q14', 'q15']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions3.html')
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        return redirect('quiz_page_4')
    return render(request, 'base/quiz_questions3.html')

def quiz_page_4(request):
    if request.method == "POST":
        required = ['q16', 'q17', 'q18', 'q19', 'q20']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions4.html')
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        return redirect('quiz_page_5')
    return render(request, 'base/quiz_questions4.html')

def quiz_page_5(request):
    if request.method == "POST":
        required = ['q21', 'q22', 'q23', 'q24', 'q25']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before submitting.")
            return render(request, 'base/quiz_questions5.html')
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        return redirect('quiz_results')
    return render(request, 'base/quiz_questions5.html')


def description(request):
    return render(request, 'base/description.html')

def quiz_submit(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('quiz_results')) 
    else:
        return HttpResponseRedirect(reverse('quiz'))

def quiz_results(request):
    return render(request, 'base/quiz_results.html')

def privacy(request):
    return render(request, 'base/privacy.html')

def terms(request):
    return render(request, 'base/terms.html')

def quiz_results(request):
    field_scores = {
        "Technology": 0,
        "Business": 0,
        "Education & Social Impact": 0,
        "Healthcare": 0,
        "Engineering": 0,
        "Creative & Design": 0,
        "Entertainment": 0,
        "Science & Environment": 0,
        "Public Services": 0,
        "Trade": 0,
    }

    
    question_map = {
        1: ["Technology", "Engineering"],
        2: ["Healthcare", "Education & Social Impact"],
        3: ["Creative & Design", "Technology"],
        4: ["Business", "Technology"],
        5: ["Education & Social Impact", "Public Services"],
        6: ["Creative & Design", "Entertainment"],
        7: ["Engineering", "Trade"],
        8: ["Business", "Public Services"],
        9: ["Entertainment", "Public Services"],
        10: ["Science & Environment", "Technology"],
        11: ["Education & Social Impact", "Public Services"],
        12: ["Science & Environment", "Trade"],
        13: ["Business", "Public Services"],
        14: ["Education & Social Impact", "Public Services"],
        15: ["Technology", "Business"],
        16: ["Science & Environment"],
        17: ["Business", "Public Services"],
        18: ["Creative & Design"],
        19: ["Trade", "Engineering"],
        20: ["Creative & Design", "Business"],
        21: ["Entertainment", "Education & Social Impact"],
        22: ["Public Services", "Education & Social Impact"],
        23: ["Business", "Healthcare"],
        24: ["Education & Social Impact", "Healthcare"],
        25: ["Technology", "Creative & Design"]
    }

    
    for q in range(1, 26):
        answer = int(request.session.get(f'quiz_q{q}', 0))
        related_fields = question_map.get(q, [])
        for field in related_fields:
            field_scores[field] += answer

  
    sorted_fields = sorted(field_scores.items(), key=lambda x: x[1], reverse=True)
    top_fields = sorted_fields[:2]  

    return render(request, 'base/quiz_results.html', {
        "top_fields": top_fields,
    })