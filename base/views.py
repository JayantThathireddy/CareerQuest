from django.shortcuts import render
# Create your views here.

rooms = [
    {'id':1, 'name':'content'},
    {'id':2, 'name':'content'},
    {'id':3, 'name':'content'}
]

def home(request):
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def quiz(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/quiz.html', context)

def about(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/about.html', context)