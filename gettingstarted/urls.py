from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views
# import myapp.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    # path("", myapp.views.landing, name="landing"),
    # path("db/", myapp.views.db, name="db"),
    path("", hello.views.landing, name="landing"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    # path('hello/', include('myapp.urls')),
    path('hello/', include('hello.urls')),
    path('api/v1/', include('polls.urls')),
]
