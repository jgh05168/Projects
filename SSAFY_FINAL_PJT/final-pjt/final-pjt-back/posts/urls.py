from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.post_list),
    path('category/', views.category),
    path('category/create/', views.category_create),
    path('category/<int:category_pk>/', views.category_delete),
    path('posts/<int:post_pk>/', views.post_detail),
    path('posts/<int:post_pk>/comments/', views.comment),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('posts/<int:post_pk>/like/', views.like),
]
