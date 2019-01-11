from django.urls import path
from .views import PostListView
from . import views


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='news'),
]
