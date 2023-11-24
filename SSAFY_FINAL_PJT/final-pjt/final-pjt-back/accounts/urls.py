from django.urls import path
from . import views


urlpatterns = [
    path('signout/', views.signout),
    path('profile/update/<int:user_pk>/', views.profileUpdate),
    path('profile/<int:user_pk>', views.user_list),
]
