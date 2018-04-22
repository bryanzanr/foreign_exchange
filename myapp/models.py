from django.db import models

# from imgurpython import ImgurClient
# # from django.utils import timezone
# import os
# import json
# # from django.core.validators import validate_image_file_extension
# # Create your models here.
# from django.urls import reverse
# from . import broadcast as tb

# Create your models here.


class Register(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    merchant_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    repeat_password = models.CharField(max_length=50)

    # def register(self):
    #     self.save()

    # def __str__(self):
    #     return self.first_name


class Login(models.Model):

    email = models. EmailField(max_length=100)
    password = models. CharField(max_length=50)

    # def __str__(self):
    #     return self.email


class User(models.Model):

    # the variable to take the inputs
    user_name = models.CharField(max_length=100)
    user_avatar = models.FileField()

    # on submit click on the user entry page, it redirects to the url below.
    # def get_absolute_url(self):
    #     client_id = os.environ['IMGUR_CLIENT_ID']
    #     client_secret = os.environ['IMGUR_CLIENT_SECRET']
    #     client = ImgurClient(client_id, client_secret)
    #     # arr = os.listdir()
    #     # for i in range(len(arr)):
    #     # 	if '.jpg' in arr[i]:
    #     image_json = client.upload_from_path(
    #         self.user_avatar.name, config=None, anon=True)
    #     print(image_json)
    #     image_json['user'] = str(self.user_name)
    #     arr = json.load(open('flyit/myapp/static/text/image.txt'))
    #     arr.append(image_json)
    #     with open('flyit/myapp/static/text/image.txt', 'w') as file:
    #         file.write(json.dumps(arr))
    #     os.remove(self.user_avatar.name)
    #     tb.main()
    #     return reverse('uploadfileapp:home')


class Ads(models.Model):

    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    address = models.CharField(max_length=45)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    # fileUpload = models.ImageField(validators=
    # [validate_image_file_extension])
    img = models.URLField(max_length=300, default=None, blank=True, null=True)
    published_date = models.DateTimeField(auto_now=True)

    # def publish(self):
    #     self.save()

    # def __str__(self):
    #     return self.title
