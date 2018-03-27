from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('register/', views.register, name='register'),
    path('header/', views.header, name='header'),
    path('footer/', views.footer, name='footer'),
    path('login/', views.login, name='login'),
    # path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout, name='logout'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('registered/', views.registered, name='registered'),
    path('invalid/', views.invalid_login, name='invalid'),
]
