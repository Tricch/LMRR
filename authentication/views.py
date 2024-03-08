from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lgn, logout as lgo
from django.contrib import messages
from .models import Restaurant, Rating
from django.db.models import Sum, Avg
import pandas as pd
from django.db.models import Case, When

# import numpy as np
# import seaborn as sb
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.linear_model import LogisticRegression
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import r2_score
# import warnings
# warnings.filterwarnings('always')
# warnings.filterwarnings('ignore')
# import re
# from nltk.corpus import stopwords
# from sklearn.metrics.pairwise import linear_kernel
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer


def home(request):
    return render(request, 'index.html')

# def get_similar(restaurant,ratings,corrMatrix):
#     similar_ratings = corrMatrix[restaurant]*(ratings-2.5)
#     similar_ratings = similar_ratings.sort_values(ascending=False)
#     return similar_ratings

# def recommend(request):
#     restaurant_rating=pd.DataFrame(list(Restaurant.objects.all().values()))

#     new_user=restaurant_rating.user_id.unique().shape[0]
#     current_user_id= request.user.id
# 	# if new user not rated any restuarant
#     if current_user_id>new_user:
#         restu=Restaurant.objects.get(id=19)
#         q=Restaurant(user=request.user,restu=restu,ratings=0)
#         q.save()


#     userRatings = restaurant_rating.pivot_table(index=['user_id'],columns=['id'],values='ratings')
#     userRatings = userRatings.fillna(0,axis=1)
#     corrMatrix = userRatings.corr(method='pearson')

#     user = pd.DataFrame(list(Restaurant.objects.filter(user=request.user).values())).drop(['user_id','id'],axis=1)
#     user_filtered = [tuple(x) for x in user.values]
#     restaurant_id_viewed = [each[0] for each in user_filtered]

#     similar_restaurant = pd.DataFrame()
#     for restaurant,rating in user_filtered:
#         similar_restaurant = similar_restaurant.append(get_similar(restaurant,rating,corrMatrix),ignore_index = True)

#     restu_id = list(similar_restaurant.sum().sort_values(ascending=False).index)
#     restu_id_recommend = [each for each in restu_id if each not in restaurant_id_viewed]
#     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(restu_id_recommend)])
#     restu_list=list(Restaurant.objects.filter(id__in = restu_id_recommend).order_by(preserved)[:10])

#     context = {'movie_list': restu_list}
#     return render(request, 'dashboard', context)
    
    # one_restu = Restaurant.objects.filter(id=pk)
    # params = {'resturants': all_restu,'one_restu':one_restu}

    # return render(request, 'restaurant.html', params)



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
                  'avg_ratings': avg_ratings}

        return render(request, 'dashboard.html', params)
    else:
        return redirect('home')
    
    
def restaurant(request,pk):
    if request.user.is_authenticated:
        all_restu = Restaurant.objects.all().order_by("-pk")
        one_restu = Restaurant.objects.filter(id=pk)
        avg_ratings = Restaurant.objects.annotate(avg_rating=Avg(4.0)).order_by('-ratings')[0:10]

        params = {'resturants': all_restu,'one_restu':one_restu, 'avg_ratings': avg_ratings}

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
            return messages.error(request, "Nothing Found.")

    else:
        return redirect('home')
    
def rating(request):
    obj = Rating.objects.filter(rating=0).order_by("?").first()
    context = {
        'object': obj
    }
    return render(request, 'restaurant.html', context)