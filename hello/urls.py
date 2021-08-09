from django.conf.urls import url

# from . import views
# from myapp import views
from hello import views
# from django.conf import settings
# from django.conf.urls.static import static
# /uploadfileapp/

# from myapp import views

# from . import views

# app_name = 'uploadfileapp'
# app_name = 'myapp'
urlpatterns = [
    url(r'broadcast/$', views.broadcast, name='broadcast'),
    url(r'response/$', views.index, name='response'),
    url(r'register/$', views.register, name='register'),
    url(r'^$', views.login, name='login'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'loggedin/$', views.loggedin, name='loggedin'),
    url(r'registered/$', views.registered, name='registered'),
    url(r'invalid/$', views.invalid_login, name='invalid'),
    url(r'editProfile/$', views.edit_profile, name='edit_profile'),
    url(r'editSuccess/$', views.edit_success, name='edit_success'),
    url(r'profile/$', views.show_profile, name='show_profile'),
    url(r'statistic/$', views.statistic, name='statistic'),
    # path('hello/', views.hello, name='hello'),
    # path('maps/', views.maps, name='maps'),
    # path('location/', views.location, name='location'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += patterns(”, (r’^static/(?P.*)$’,
#     ‘django.views.static.serve’, {‘document_root’:
#     settings.STATIC_ROOT}),)
