# from django.urls import path
# from django.urls import path
from django.conf.urls import url

from . import views
# /uploadfileapp/

# from myapp import views

# from . import views

# app_name = 'uploadfileapp'

urlpatterns = [
    # uploadfileapp/
    # url(r'^$', views.HomeView.as_view(), name='home'),

    # uploadifileapp/register
    # url(r'^broadcast/upload/$', views.UserEntry.as_view(), name='user-entry'),
    # path('hello/', views.hello, name='hello'),
    url(r'broadcast/$', views.broadcast, name='broadcast'),
    # path('broadcast/upload/', views.upload, name='upload'),
    # path('index/', views.index, name='index'),
    url(r'response/$', views.index, name='response'),
    # url(r'hello/$', views.hello, name='hello'),
    url(r'register/$', views.register, name='register'),
    # url(r'header/$', views.header, name='header'),
    # url(r'footer/$', views.footer, name='footer'),
    url(r'^$', views.login, name='login'),
    url(r'login/$', views.login, name='login'),
    # url(r'auth/', views.auth_view, name='auth'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'loggedin/$', views.loggedin, name='loggedin'),
    url(r'registered/$', views.registered, name='registered'),
    url(r'invalid/$', views.invalid_login, name='invalid'),
    # path('hello/', views.hello, name='hello'),
    # path('maps/', views.maps, name='maps'),
    # path('location/', views.location, name='location'),
]

# urlpatterns += patterns(”, (r’^static/(?P.*)$’,
#     ‘django.views.static.serve’, {‘document_root’:
#     settings.STATIC_ROOT}),)
