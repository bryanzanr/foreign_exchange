from django.db import models

# Create your models here.


class Register(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    merchant_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    repeat_password = models.CharField(max_length=50)

    def register(self):
        self.save()

    def __str__(self):
        return self.first_name


class Login(models.Model):

    email = models. EmailField(max_length=100)
    password = models. CharField(max_length=50)

    def __str__(self):
        return self.email
