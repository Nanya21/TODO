from django.urls import path
from . import views

urlpatterns=[
    path('users/', views.users),
    path('users/', views.get_user),
    path('users/<uuid:user_id>/', views.user_detail),
    path('users/login/', views.Login),
    path('users/change_password/', views.reset_password)
    ]