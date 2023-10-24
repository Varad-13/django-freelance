from django.shortcuts import render, redirect
from .models import UserProfile, Post, Freelancer, Post_tag
from .forms import postform, userSignup
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate

def index(request):
        return render(request, 'core/landing.html')

def loggedin(request):
    users = UserProfile.objects.exclude(username=request.user.username)
    posts = Post.objects.all()
    context = {
        'users': users,
        'posts' : posts,
    }
    return render(request, 'core/index.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')

def search(request, query):
    results = Post.objects.filter(name__contains=query)
    context = {
        'posts' : results,
    }
    return render(request, 'core/search.html', context)

def createPost(request):
    form = postform(request.POST)
    if form.is_valid():
        rec = form.save(commit=False)
        rec.freelancer=Freelancer.objects.get(user_id=request.user)
        rec.save()
    else:
        form = postform()
    context = {
        'form' : form,
    }
    return render(request, 'core/createPost.html', context)

def userSignupForm(request):
    form = userSignup()
    if request.method == 'POST':        # For 'POST' request
        form = userSignup(request.POST)
        if form.is_valid():
            user = form.save()
            # Freelancer.objects.create(
            #     user_id=user,
            #     custom_url=request.POST.get('custom_url')
            #     )
            # user.save()
    else:
            form = userSignup()
    context = {
        'form' : form,
    }
    return render(request, 'core/userSignup.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'core/login.html', context)