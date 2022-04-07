from django.urls import path
# Импортируем созданное нами представление
<<<<<<< HEAD
from .views import PostsList, PostDetail
=======
from .views import *
>>>>>>> 7bbca5d2 (Add, Edit, Delete)


urlpatterns = [
   path('', PostsList.as_view()),
<<<<<<< HEAD
   path('<int:pk>', PostDetail.as_view()),
=======
   path('search', PostsSearch.as_view()),
   path('<int:pk>', PostDetail.as_view()),
   path('add', AddPosts.as_view()),
   path('<int:pk>/edit', PostEdit.as_view()),
   path('<int:pk>/delete', DeletePost.as_view()),
>>>>>>> 7bbca5d2 (Add, Edit, Delete)
]