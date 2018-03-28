from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('register/', views.register, name='register'),
    url(r'register/$', views.register, name='register'),
    path('header/', views.header, name='header'),
    path('footer/', views.footer, name='footer'),
    url(r'^$', views.login, name='login'),
    url(r'login/', views.login, name='login'),
    # path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout, name='logout'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('registered/', views.registered, name='registered'),
    path('invalid/', views.invalid_login, name='invalid'),
]

# urlpatterns += patterns(”, (r’^static/(?P.*)$’,
#     ‘django.views.static.serve’, {‘document_root’:
#     settings.STATIC_ROOT}),)
