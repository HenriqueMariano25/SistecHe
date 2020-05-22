from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def login(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        user = auth.authenticate(request, username=login, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        print(login)
        print(password)
        print("O method é POST")
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')
