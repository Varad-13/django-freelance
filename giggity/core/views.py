from django.shortcuts import render, redirect
from django.db.models import Q
from .models import UserProfile, Post, Post_tag, Recommendations
from django.contrib.auth.decorators import login_required


@login_required(login_url='account_login')
def landing(request):

    return render(request, 'core/landing.html')

@login_required(login_url='account_login')
def index(request):

        users = UserProfile.objects.exclude(username=request.user.username)
        posts = Post.objects.all()
        user_profiles = UserProfile.objects.in_bulk([post.freelancer.user_id.id for post in posts])
        tags = Post_tag.objects.filter(post__in=posts).distinct()
        context = {
            'users': users,
            'posts' : posts,
            'user_profiles': user_profiles,
            'tags': tags,
        }
        return render(request, 'core/index.html', context)


def search(request, query):
    results = Post.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    context = {
        'query' : query,
        'posts' : results,
    }
    return render(request, 'core/search.html', context)

def recommendations_view(request):
    user = request.user # Assuming you're using authentication
    recommendations = Recommendations.objects.filter(user=user, visited=False).order_by('-score')[:9]
    recommended_posts = [recommendation.post for recommendation in recommendations]

    return render(request, 'core/for_you.html', {'posts': recommended_posts})

def top_posts_view(request):
    top_posts = Post.objects.all().order_by('-post_id')[:9]  # Adjust the ordering criteria as needed

    return render(request, 'core/top_posts.html', {'posts': top_posts})
