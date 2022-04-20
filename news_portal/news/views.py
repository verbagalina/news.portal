from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import *
from .filters import PostFilter
from django.shortcuts import redirect


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    queryset = Post.objects.filter(categoryType='NW')
    template_name = 'post_list.html'
    context_object_name = 'postList'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostsSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    queryset = Post.objects.filter(categoryType='NW')
    template_name = 'post_search.html'
    context_object_name = 'postList'
    paginate_by = 5

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
    #    return context

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    #def get_context_data(self, *args, **kwargs):
    #    return {
    #        **super().get_context_data(*args, **kwargs),
    #        'filter': self.get_filter()
    #    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.get_filter()
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostEdit(PermissionRequiredMixin, DetailView):
    permission_required = ('news.add_post', 'news.change_post', 'news.delete_post',)
    model = Post
    context_object_name = 'post'
    template_name = 'edit_post.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        for c in categories:
            c.ischeck = 0
            if len(PostCategory.objects.filter(postThrough=context['post'], categoryThrough=c)) == 1:
                c.ischeck = 1
        context['categories'] = categories
        context['users'] = Author.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        id = request.POST['id_post']
        title = request.POST['title']
        if len(title) == 0:
            title = 'No title'
        article = request.POST['text']
        if len(article) == 0:
            article = '* no publication *'
        categoryType = request.POST['category-type']
        user = request.POST['author']
        user = User.objects.get(id=user)
        user = Author.objects.get(authorUser=user)
        postCategory = []
        cs = Category.objects.all()
        for c in cs:
            field = 'category-' + str(c.id)
            try:
                field = request.POST[field]
            except:
                field = 0
            postCategory.append(field)
        post = Post.objects.get(id=id)
        Post(title=title, text=article, categoryType=categoryType, author=user)
        post.title=title
        post.text=article
        post.categoryType=categoryType
        post.author=user
        post.save()
        pc = PostCategory.objects.filter(postThrough=post).delete()
        for category in postCategory:
            if category != 0:
                c = Category.objects.get(id=category)
                pc = PostCategory(postThrough=post, categoryThrough=c)
                pc.save()
        return redirect(f'/news/{id}')


class DeletePost(PermissionRequiredMixin, DetailView):
    permission_required = ('news.add_post', 'news.change_post', 'news.delete_post',)
    model = Post
    template_name = 'delete_post.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        id = request.POST['id_post']
        post = Post.objects.get(id=id).delete()
        return redirect(f'/news')


class AddPosts(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_post', 'news.change_post', 'news.delete_post',)
    model = Post
    template_name = 'add_post.html'
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['users'] = Author.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        if len(title) == 0:
            title = 'No title'
        article = request.POST['text']
        if len(article) == 0:
            article = '* no publication *'
        categoryType = request.POST['category-type']
        user = request.POST['author']
        user = User.objects.get(id=user)
        user = Author.objects.get(authorUser=user)
        postCategory = []
        cs = Category.objects.all()
        for c in cs:
            field = 'category-' + str(c.id)
            try:
                field = request.POST[field]
            except:
                field = 0
            postCategory.append(field)
        post = Post(title=title, text=article, categoryType=categoryType, author=user)
        post.save()
        for category in postCategory:
            if category != 0:
                c = Category.objects.get(id=category)
                pc = PostCategory(postThrough=post, categoryThrough=c)
                pc.save()
        return redirect(f'/news/{post.id}')  #super().get(request, *args, **kwargs)
