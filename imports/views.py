from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth


def effective(request):
    if request.user.is_authenticated:
        return render(request, 'effective.html')
    else:
        return redirect('login')

