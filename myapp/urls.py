# from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'hello/', views.hello, name='hello'),
    url(r'register/', views.register, name='register'),
    url(r'register/$', views.register, name='register'),
    url(r'header/', views.header, name='header'),
    url(r'footer/', views.footer, name='footer'),
    url(r'^$', views.login, name='login'),
    url(r'login/', views.login, name='login'),
    # url(r'auth/', views.auth_view, name='auth'),
    url(r'logout/', views.logout, name='logout'),
    url(r'loggedin/', views.loggedin, name='loggedin'),
    url(r'registered/', views.registered, name='registered'),
    url(r'invalid/', views.invalid_login, name='invalid'),
]

# urlpatterns += patterns(”, (r’^static/(?P.*)$’,
#     ‘django.views.static.serve’, {‘document_root’:
#     settings.STATIC_ROOT}),)
