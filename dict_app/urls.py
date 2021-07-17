from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('login', views.loginandregister),
    path('users/register', views.register),
    path('users/login', views.login),
    path('logout', views.logout),
    path('users/profile', views.profile),
    path('words/<str:content>', views.word),
    path('findaword', views.process),
    path('words/like/<int:wordid>', views.like),
    path('words/delete/<int:wordid>', views.delete),

]