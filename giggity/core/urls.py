from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('index', views.index, name='index'),
    path('search/<str:query>', views.search, name='search'),
    path('for_you', views.recommendations_view, name='recommendations'),
    path('top', views.top_posts_view, name='recommendations'),
    path('create_post', views.create_post, name='create_post')
]
