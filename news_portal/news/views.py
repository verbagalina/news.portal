from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    queryset = Post.objects.filter(categoryType='NW')
    template_name = 'postList.html'
    context_object_name = 'postList'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
