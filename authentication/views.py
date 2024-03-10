from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lgn, logout as lgo
from django.contrib import messages
from .models import Restaurant, Rating
from django.db.models import Avg
from django.db.models import Case, When
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recommendation(request):
    user = request.user.username
    user_detail = User.objects.get(username=user)
    ratings = Rating.objects.filter(user=user_detail)
    calculate_reco()

def get_similar(movie_name,rating,corrMatrix):
    similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings


def calculate_reco(request):
    movie_rating=pd.DataFrame(list(Rating.objects.all().values()))

    new_user=movie_rating.user_id.unique().shape[0]
    current_user_id= request.user.id
	# if new user not rated any movie
    if current_user_id>new_user:
        movie=Restaurant.objects.get(id=19)
        q=Rating(user=request.user,movie=movie,rating=0)
        q.save()

    userRatings = movie_rating.pivot_table(index=['user_id'],columns=['movie_id'],values='rating')
    userRatings = userRatings.fillna(0,axis=1)
    corrMatrix = userRatings.corr(method='pearson')

    user = pd.DataFrame(list(Rating.objects.filter(user=request.user).values())).drop(['user_id','id'],axis=1)
    user_filtered = [tuple(x) for x in user.values]
    movie_id_watched = [each[0] for each in user_filtered]

    similar_movies = pd.DataFrame()
    for movie,rating in user_filtered:
        similar_movies = similar_movies.append(get_similar(movie,rating,corrMatrix),ignore_index = True)

    movies_id = list(similar_movies.sum().sort_values(ascending=False).index)
    movies_id_recommend = [each for each in movies_id if each not in movie_id_watched]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(movies_id_recommend)])
    movie_list=list(Restaurant.objects.filter(id__in = movies_id_recommend).order_by(preserved)[:10])

    context = {'movie_list': movie_list}
    return render(request, 'dashboard.html', context)


def home(request):
    return render(request, 'index.html')


def dashboard(request):
    if request.user.is_authenticated:
        all_restu = Restaurant.objects.all().order_by("-pk")
        acous_restu = Restaurant.objects.all().filter(genre= 'Acoustic')
        ambie_restu = Restaurant.objects.all().filter(genre= 'Ambient')
        classic_restu = Restaurant.objects.all().filter(genre= 'Classical')
        intru_restu = Restaurant.objects.all().filter(genre= 'Instrumental')
        jaz_restu = Restaurant.objects.all().filter(genre= 'Jazz')
        pop_restu = Restaurant.objects.all().filter(genre= 'Pop')
        avg_ratings = Restaurant.objects.annotate(avg_rating=Avg(4.0)).order_by('-ratings')[0:10]
        
        
   
    params = {'resturants': all_restu, 
                  'acoustic': acous_restu,
                  'ambient': ambie_restu,
                  'classical': classic_restu,
                  'instrumental': intru_restu,
                  'jazz': jaz_restu,
                  'pops': pop_restu,
                  'avg_ratings': avg_ratings,
                  }

    return render(request, 'dashboard.html', params)


def handle_rating(request,pk):
    print("nnn")
    if request.method == 'POST':
            print("nnn")
            one_restu = Restaurant.objects.get(id=pk)
            user = request.user.username
            print("user = ",user)
            user_detail = User.objects.get(username=user)
            star_rating = request.POST.get('rating')
            restu_review = request.POST.get('restu_review')
            print("dfada = ",star_rating)
            restu_review = Rating(user=user_detail,restaurant=one_restu, rating=star_rating, review_desp = restu_review)
            restu_review.save()
    return redirect (f'/restaurant/{pk}')

    
def restaurant(request,pk):
    if request.user.is_authenticated:
        all_restu = Restaurant.objects.all().order_by("-pk")
        one_restu = Restaurant.objects.filter(id=pk)
        avg_ratings = Restaurant.objects.annotate(avg_rating=Avg(4.0)).order_by('-ratings')[0:10]                  
        params = {'resturants': all_restu,
                  'one_restu':one_restu, 
                  'avg_ratings':avg_ratings         
                }
        return render(request, 'restaurant.html', params)
    else:
        return redirect('home')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('home')
    
    
def search(request):
    if request.user.is_authenticated:
        try:
            query = request.POST.get('query')
            searched_restu = Restaurant.objects.filter(rest_name__icontains=query)
            params = {'searches':searched_restu}
            return render(request, 'search.html', params)
        except:
            return HttpResponse(messages.error(request, "Nothing Found."))
    else:
        return redirect('home')


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
    params = {'openModal': True}
    return render(request, 'index.html', params)