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
from .models import QuizResult

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
    retake = request.GET.get('retake', 'false') == 'true'
    
    if retake:
        for i in range(1, 26):
            key = f'quiz_q{i}'
            if key in request.session:
                del request.session[key]
        request.session['retaking_quiz_in_progress'] = True

        if request.user.is_authenticated:
            QuizResult.objects.filter(user=request.user).delete()

    elif request.user.is_authenticated:
        if QuizResult.objects.filter(user=request.user).exists():
            return redirect('quiz_results')

    dark_mode = request.session.get('dark_mode', False)
    return render(request, 'base/quiz.html', {'dark_mode': dark_mode, 'retake': retake})


def start_quiz(request):
    # Clear previous quiz answers
    retake = request.GET.get('retake', 'false') == 'true'
    
    if not retake and request.user.is_authenticated:
        if QuizResult.objects.filter(user=request.user).exists():
            return redirect('quiz_results')
    for i in range(1, 26):
        request.session.pop(f'quiz_q{i}', None)
    return redirect('quiz_page_1')  


def about(request):
    dark_mode = request.session.get('dark_mode', False)
    return render(request, 'base/about.html', {'dark_mode': dark_mode})

def loginPage(request):
    page = 'login'
    context = {'page': page}
    
    # Save the 'next' parameter if present
    next_page = request.GET.get('next', 'home')
    
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
            # Redirect to the next page if provided
            return redirect(request.POST.get('next', 'home'))
        else:
            messages.error(request, "Password is incorrect.")
    
    # Pass the next parameter to the template
    context['next'] = next_page
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    next_page = request.GET.get('next', 'home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            # Redirect to the next page if provided
            return redirect(request.POST.get('next', 'home'))
        else:
            messages.error(request, "An error occurred during registration.")
            print(form.errors)

    return render(request, 'base/login_register.html', {'form': form, 'next': next_page})

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

def quiz_page(request, page_num):
    page_num = int(page_num)

    page_ranges = {
        1: range(1, 6),
        2: range(6, 11),
        3: range(11, 16),
        4: range(16, 21),
        5: range(21, 26),
    }

    if page_num not in page_ranges:
        return redirect('quiz_page_1')
    
    retake = request.GET.get('retake', request.POST.get('retake', 'false')) == 'true'
    
    if not retake and request.user.is_authenticated:
        if QuizResult.objects.filter(user=request.user).exists():
            return redirect('quiz_results')
            

    required = [f'q{i}' for i in page_ranges[page_num]]
    template_name = f'base/quiz_questions{"" if page_num == 1 else page_num}.html'

    if request.method == "POST":
        data = request.POST.dict()
        if any(not data.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, template_name, {"data": data})

        for q in required:
            request.session[f'quiz_{q}'] = data[q]

        if page_num == 5:
            return redirect('quiz_results')
        else:
            return redirect(f'quiz_page_{page_num + 1}')


    initial = {f"q{i}": request.session.get(f"quiz_q{i}", "") for i in page_ranges[page_num]}
    return render(request, template_name, {"data": initial})

def description(request):
    return render(request, 'base/description.html')

def quiz_submit(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('quiz_results')) 
    else:
        return HttpResponseRedirect(reverse('quiz'))

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
    13: ["Science & Environment", "Healthcare"],
    14: ["Creative & Design", "Engineering"],
    15: ["Trade", "Engineering"],
    16: ["Creative & Design", "Business"],
    17: ["Entertainment", "Education & Social Impact"],
    18: ["Business", "Healthcare"],
    19: ["Healthcare"],
    20: ["Entertainment"],
    21: ["Trade"],
    22: ["Science & Environment"],
    23: ["Technology", "Business"],
    24: ["Creative & Design", "Healthcare"],
    25: ["Public Services", "Engineering"]
    }

    
    for q in range(1, 26):
        answer = int(request.session.get(f'quiz_q{q}', 0))
        related_fields = question_map.get(q, [])
        for field in related_fields:
            field_scores[field] += answer

  
    sorted_fields = sorted(field_scores.items(), key=lambda x: x[1], reverse=True)
    top_fields = sorted_fields[:2]
    
    request.session['top_field_1'] = top_fields[0][0]
    request.session['top_field_2'] = top_fields[1][0] if len(top_fields) > 1 else None
    request.session['score_field_1'] = top_fields[0][1]
    request.session['score_field_2'] = top_fields[1][1] if len(top_fields) > 1 else None
    
    retaking_quiz = request.session.pop('retaking_quiz', False)
    
    result_saved = False
    if request.user.is_authenticated:
        existing_result = QuizResult.objects.filter(user=request.user).first()
        if existing_result and retaking_quiz:
            existing_result.top_field_1 = request.session.get('top_field_1', '')
            existing_result.top_field_2 = request.session.get('top_field_2', '')
            existing_result.score_field_1 = request.session.get('score_field_1', 0)
            existing_result.score_field_2 = request.session.get('score_field_2', 0)
            existing_result.save()
            messages.success(request, "Your quiz results have been updated!")
            result_saved = True
        else:
            result_saved = QuizResult.objects.filter(user=request.user).exists()

    return render(request, 'base/quiz_results.html', {
        "top_fields": top_fields,
        "result_saved": result_saved
    })

@login_required
@login_required
def save_results(request):
    if request.method == 'POST':
        existing_result = QuizResult.objects.filter(user=request.user).first()
        
        if existing_result:
            existing_result.top_field_1 = request.session.get('top_field_1', '')
            existing_result.top_field_2 = request.session.get('top_field_2', '')
            existing_result.score_field_1 = request.session.get('score_field_1', 0)
            existing_result.score_field_2 = request.session.get('score_field_2', 0)
            existing_result.save()
            messages.success(request, "Your quiz results have been updated!")
        else:
            QuizResult.objects.create(
                user=request.user,
                top_field_1=request.session.get('top_field_1', ''),
                top_field_2=request.session.get('top_field_2', ''),
                score_field_1=request.session.get('score_field_1', 0),
                score_field_2=request.session.get('score_field_2', 0)
            )
            messages.success(request, "Your quiz results have been saved!")
        
        return redirect('quiz_results')
    
    return redirect('quiz_results')

def career_description(request):
    return render(request, 'base/career_description.html')