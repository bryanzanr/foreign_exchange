from django.contrib import admin

# Register your models here.
from myapp.models import Register, Login, User, Ads

admin.site.register(User)
admin.site.register(Ads)

admin.site.register(Register)
admin.site.register(Login)
