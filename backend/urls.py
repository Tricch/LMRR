"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication.views import home, login, logout, signup, dashboard, profile, restaurant, search, handle_rating
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('dashboard', dashboard,  name='dashboard'),
    path('restaurant/<int:pk>', restaurant,  name='restaurant'),
    path('handle_rating/<int:pk>', handle_rating,  name='handleRatings'),
    path('signup', signup,  name='signup'),
    path('profile', profile,  name='profile'),
    path('logout', logout,  name='logout'),
    path('login', login,  name='login'),
    path('search',search,name="search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
