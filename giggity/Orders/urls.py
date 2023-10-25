from django.urls import path
from . import views

urlpatterns = [
    path('orders/detail/<str:author>/<str:url>/', views.detail, name='detail'),
]
