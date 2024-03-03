from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lgn, logout as lgo
from django.contrib import messages
from .models import Restaurant

def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email1')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
        else:
            new_user = User.objects.create_user(uname, email, pass1)
            new_user.save()
            messages.success(request, "Your account has been successfully created!")
            params = {'openModal': True}
            return render(request, 'index.html', params)
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            lgn(request, user)
            messages.success(request, "You've logged in successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'index.html')

def logout(request):
    lgo(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

def dashboard(request):
    if request.user.is_authenticated:
        all_restu = Restaurant.objects.all().order_by("-pk")
        params = {'resturants': all_restu}

        return render(request, 'dashboard.html', params)
    else:
        return redirect('home')
    
def restaurant(request):
    if request.user.is_authenticated:
        all_restu = Restaurant.objects.all().order_by("-pk")
        params = {'resturants': all_restu}

        return render(request, 'restaurant.html', params)
    else:
        return redirect('home')

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('home')