from django.contrib import admin

# Register your models here.
from myapp.models import Register, Login

admin.site.register(Register)
admin.site.register(Login)
