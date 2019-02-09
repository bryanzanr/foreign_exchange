# from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    # path('', views.index, name='login'),
    url(r'^$', views.login, name='login'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'register/$', views.register, name='register'),
]
