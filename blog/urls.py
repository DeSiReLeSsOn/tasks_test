from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostListView, PostDetailView 







urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]