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


def quiz_questions(request):
    retake = request.GET.get('retake', 'false') == 'true'
    
    if not retake and request.user.is_authenticated:
        if QuizResult.objects.filter(user=request.user).exists():
            return redirect('quiz_results')
            
    questions = []  
    return render(request, 'base/quiz_questions.html', {'questions': questions})

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

def quiz_page_1(request):
    retake = request.GET.get('retake', request.POST.get('retake', 'false')) == 'true'
    
    if not retake and request.user.is_authenticated:
        if QuizResult.objects.filter(user=request.user).exists():
            return redirect('quiz_results')
            
    if request.method == "POST":
        required = ['q1', 'q2', 'q3', 'q4', 'q5']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions.html', {'retake': retake})
        
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        
        request.session['retaking_quiz_in_progress'] = retake
        
        return redirect('quiz_page_2')
    
    return render(request, 'base/quiz_questions.html', {'retake': retake})

def quiz_page_2(request):
    retake = request.session.get('retaking_quiz_in_progress', False)
    if request.method == "POST":
        retake = request.POST.get('retake', 'false') == 'true'
        request.session['retaking_quiz_in_progress'] = retake
    
    if request.method == "POST":
        required = ['q6', 'q7', 'q8', 'q9', 'q10']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions2.html', {'retake': retake})
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        
        return redirect('quiz_page_3')
    
    return render(request, 'base/quiz_questions2.html', {'retake': retake})

def quiz_page_3(request):
    retake = request.session.get('retaking_quiz_in_progress', False)
    if request.method == "POST":
        retake = request.POST.get('retake', 'false') == 'true'
        request.session['retaking_quiz_in_progress'] = retake
    
    if request.method == "POST":
        required = ['q11', 'q12', 'q13', 'q14', 'q15']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions3.html', {'retake': retake})
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        
        return redirect('quiz_page_4')
    
    return render(request, 'base/quiz_questions3.html', {'retake': retake})

def quiz_page_4(request):
    retake = request.session.get('retaking_quiz_in_progress', False)
    if request.method == "POST":
        retake = request.POST.get('retake', 'false') == 'true'
        request.session['retaking_quiz_in_progress'] = retake
    
    if request.method == "POST":
        required = ['q16', 'q17', 'q18', 'q19', 'q20']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before continuing.")
            return render(request, 'base/quiz_questions4.html', {'retake': retake})
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        
        return redirect('quiz_page_5')
    
    return render(request, 'base/quiz_questions4.html', {'retake': retake})

def quiz_page_5(request):
    retake = request.session.get('retaking_quiz_in_progress', False)
    if request.method == "POST":
        retake = request.POST.get('retake', 'false') == 'true'
        request.session['retaking_quiz_in_progress'] = retake
    
    if request.method == "POST":
        required = ['q21', 'q22', 'q23', 'q24', 'q25']
        if any(not request.POST.get(q) for q in required):
            messages.error(request, "Please answer all the questions before submitting.")
            return render(request, 'base/quiz_questions5.html', {'retake': retake})
        for q in required:
            request.session[f'quiz_{q}'] = request.POST.get(q)
        
        if retake:
            request.session['retaking_quiz'] = True
        
        return redirect('quiz_results')
    
    return render(request, 'base/quiz_questions5.html', {'retake': retake})

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