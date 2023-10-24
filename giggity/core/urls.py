from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.loggedin, name='windex'),
    path('search/<str:query>', views.search, name='search'),
    path('create-Post/', views.createPost, name='createPost'),
    path('usersignup/', views.userSignupForm, name='userSignup'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
]
