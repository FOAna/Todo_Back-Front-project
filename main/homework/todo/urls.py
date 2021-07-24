from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('login/', views.user_login, name='login'),
    path('register', views.user_register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_view/', views.my_view, name='me_view'),
    path('create/<str:pk>/', views.create_todo, name='create'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('delete_all_todo/', views.delete_all),
    path('edit/<str:pk>/<str:new>', views.edit),
    path('all_user_data', views.all_user_data),
    path('pomodoro_count/<str:pk>', views.pomodoro_count)
]

