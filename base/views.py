from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

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
        # Save q1 to q5 into session or database
        request.session['quiz_q1'] = request.POST.get('q1')
        request.session['quiz_q2'] = request.POST.get('q2')
        request.session['quiz_q3'] = request.POST.get('q3')
        request.session['quiz_q4'] = request.POST.get('q4')
        request.session['quiz_q5'] = request.POST.get('q5')
        return redirect('quiz_page_2')  # Redirect to the next page
    return render(request, 'base/quiz_questions.html')

def quiz_page_2(request):
    if request.method == "POST":
        # Save q6 to q10 into session or database
        request.session['quiz_q6'] = request.POST.get('q6')
        request.session['quiz_q7'] = request.POST.get('q7')
        request.session['quiz_q8'] = request.POST.get('q8')
        request.session['quiz_q9'] = request.POST.get('q9')
        request.session['quiz_q10'] = request.POST.get('q10')
        return redirect('quiz_page_3')  # Redirect to the next page
    return render(request, 'base/quiz_questions2.html')

def quiz_page_3(request):
    if request.method == "POST":
        # Save q11 to q15 into session or database
        request.session['quiz_q11'] = request.POST.get('q11')
        request.session['quiz_q12'] = request.POST.get('q12')
        request.session['quiz_q13'] = request.POST.get('q13')
        request.session['quiz_q14'] = request.POST.get('q14')
        request.session['quiz_q15'] = request.POST.get('q15')
        return redirect('quiz_page_4')  # Redirect to the next page
    return render(request, 'base/quiz_questions3.html')

def quiz_page_4(request):
    if request.method == "POST":
        # Save q16 to q20 into session or database
        request.session['quiz_q16'] = request.POST.get('q16')
        request.session['quiz_q17'] = request.POST.get('q17')
        request.session['quiz_q18'] = request.POST.get('q18')
        request.session['quiz_q19'] = request.POST.get('q19')
        request.session['quiz_q20'] = request.POST.get('q20')
        return redirect('quiz_page_5')  # Redirect to the next page
    return render(request, 'base/quiz_questions4.html')

def quiz_page_5(request):
    if request.method == "POST":
        # Save q21 to q25 into session or database
        request.session['quiz_q21'] = request.POST.get('q21')
        request.session['quiz_q22'] = request.POST.get('q22')
        request.session['quiz_q23'] = request.POST.get('q23')
        request.session['quiz_q24'] = request.POST.get('q24')
        request.session['quiz_q25'] = request.POST.get('q25')
        return redirect('quiz_page_6')  # Redirect to the job description page
    return render(request, 'base/quiz_questions5.html')

def quiz_page_6(request):
    if request.method == "POST":
        # Save q26 to q30 into session or database
        request.session['quiz_q26'] = request.POST.get('q26')
        request.session['quiz_q27'] = request.POST.get('q27')
        request.session['quiz_q28'] = request.POST.get('q28')
        request.session['quiz_q29'] = request.POST.get('q29')
        request.session['quiz_q30'] = request.POST.get('q30')
        return redirect('quiz_page_7')  # Redirect to the job description page
    return render(request, 'base/quiz_questions6.html')

def quiz_page_7(request):
    if request.method == "POST":
        # Save q31 to q35 into session or database
        request.session['quiz_q31'] = request.POST.get('q31')
        request.session['quiz_q32'] = request.POST.get('q32')
        request.session['quiz_q33'] = request.POST.get('q33')
        request.session['quiz_q34'] = request.POST.get('q34')
        request.session['quiz_q35'] = request.POST.get('q35')
        return redirect('quiz_page_8')  # Redirect to the job description page
    return render(request, 'base/quiz_questions7.html')

def quiz_page_8(request):
    if request.method == "POST":
        # Save q36 to q40 into session or database
        request.session['quiz_q36'] = request.POST.get('q36')
        request.session['quiz_q37'] = request.POST.get('q37')
        request.session['quiz_q38'] = request.POST.get('q38')
        request.session['quiz_q39'] = request.POST.get('q39')
        request.session['quiz_q40'] = request.POST.get('q40')
        return redirect('quiz_page_9')  # Redirect to the job description page
    return render(request, 'base/quiz_questions8.html')

def quiz_page_9(request):
    if request.method == "POST":
        # Save q41 to q45 into session or database
        request.session['quiz_q41'] = request.POST.get('q41')
        request.session['quiz_q42'] = request.POST.get('q42')
        request.session['quiz_q43'] = request.POST.get('q43')
        request.session['quiz_q44'] = request.POST.get('q44')
        request.session['quiz_q45'] = request.POST.get('q45')
        return redirect('quiz_page_10')  # Redirect to the job description page
    return render(request, 'base/quiz_questions9.html')

def quiz_page_10(request):
    if request.method == "POST":
        # Save q46 to q50 into session or database
        request.session['quiz_q46'] = request.POST.get('q46')
        request.session['quiz_q47'] = request.POST.get('q47')
        request.session['quiz_q48'] = request.POST.get('q48')
        request.session['quiz_q49'] = request.POST.get('q49')
        request.session['quiz_q50'] = request.POST.get('q50')
        return redirect('description')  # Redirect to the job description page
    return render(request, 'base/quiz_questions10.html')

def description(request):
    return render(request, 'base/description.html')

def quiz_submit(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('quiz_results')) 
    else:
        return HttpResponseRedirect(reverse('quiz'))
