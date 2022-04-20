from django.urls import path
# Импортируем созданное нами представление
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
   path('', PostsList.as_view()),
   path('search', PostsSearch.as_view()),
   path('<int:pk>', PostDetail.as_view()),
   path('add', login_required(AddPosts.as_view())),
   path('<int:pk>/edit', login_required(PostEdit.as_view())),
   path('<int:pk>/delete', login_required(DeletePost.as_view())),
]