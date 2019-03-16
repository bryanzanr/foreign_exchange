# from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    # path('', views.index, name='login'),
    url(r'^$', views.login, name='login'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'register/$', views.register, name='register'),
    url(r'edit/$', views.edit_profile, name='edit_profile'),
    url(r'profile/$', views.show_profile, name='show_profile'),
    url(r'broadcast/$', views.broadcast, name='broadcast'),
    url(r'statistic/$', views.statistic, name='statistic'),
]
