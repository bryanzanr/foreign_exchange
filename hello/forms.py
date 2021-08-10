from django import forms
# from .models import Register, Login
# import os
import requests
# import pyrebase
# import json
from django.utils import timezone


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    merchant_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    repeat_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def register(self, auth, firebase):
        if self.data['password'] == self.data['repeat_password']:
            try:
                regist_data = auth.create_user_with_email_and_password(self.data['email'],
                                                                       self.data['password'])
            except requests.exceptions.HTTPError as e:
                return {'error': e}
            db = firebase.database().child('merchants')
            result = {}
            result['first_name'] = self.data['first_name']
            result['last_name'] = self.data['last_name']
            result['merchant_name'] = self.data['merchant_name']
            result['username'] = self.data['email']
            result['profile_picture'] = ''
            db.child(regist_data['localId']).set(result)
            # result['name'] = result['first_name'] + ' ' + result['last_name']
            return {'auth': regist_data, 'result': result, 'error': None}
        else:
            return {'error': 'Both password field must be the same'}

    # def __init__(self, *args, **kwargs):
    #     super(RegisterForm, self).__init__(*args, **kwargs)
    #     self.fields['first_name'].required = True
    #     self.fields['last_name'].required = True
    #     self.fields['merchant_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['password'].required = True
    #     self.fields['repeat_password'].required = True
    #     self.fields['password'].widget.attrs['required'] = 'required'
    #     self.fields['repeat_password'].widget.attrs['required'] = 'required'


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def login(self, auth, firebase):
        try:
            logindata = auth.sign_in_with_email_and_password(self.data['email'],
                                                             self.data['password'])
        except requests.exceptions.HTTPError as e:
            return {'error': e}
        result = {}
        # print(logindata)
        # data = firebase.database().get().val()['merchants'][logindata['localId']]
        data = {}
        merchants = firebase.database().get().val()['merchants']
        # print(merchants)
        for _, merchant in merchants.items():
            # print(merchant)
            if merchant['username'] == logindata['email']:
                data = merchant
        # print(data)
        result['title'] = 'Broadcast'
        front_name = data['first_name']
        last_name = data['last_name']
        result['first_name'] = front_name
        result['last_name'] = last_name
        # result['name'] = front_name + ' ' + last_name
        result['username'] = logindata['email']
        result['merchant_name'] = data['merchant_name']
        result['profile_picture'] = data['profile_picture']
        return {'auth': logindata, 'result': result, 'error': None}

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].required = True
    #     self.fields['password'].required = True
    #     self.fields['password'].widget.attrs['required'] = 'required'


class AdsForm(forms.Form):

    # class Meta:
    #     model = Ads
    #     fields = ('title', 'desc', 'address',
    #               'latitude', 'longitude', 'tag', 'img')

    TAG_CHOICES = (
        ('1', 'Food'),
        ('2', 'Fashion'),
        ('3', 'Lifestyle'),
        ('4', 'Property'),
    )
    title = forms.CharField(label='Title', required=True, max_length=100)
    desc = forms.CharField(label='Description', required=True, max_length=300)
    address = forms.CharField(label='Address', required=False, max_length=45)
    latitude = forms.CharField(label='Latitude', required=False, max_length=30)
    longitude = forms.CharField(
        label='Longitude', required=False, max_length=30)
    tag = forms.CharField(label='Tag', required=False, widget=forms.Select(
        choices=TAG_CHOICES), max_length=2)

    def create_dict(self, email, img):
        temp = {}
        temp['title'] = self.data['title']
        temp['description'] = self.data['desc']
        temp['author'] = str(email)
        temp['publish'] = str(timezone.now())
        temp['lat'] = self.data['latitude']
        temp['long'] = self.data['longitude']
        temp['tag'] = self.data['tag']
        temp['img'] = img
        return temp

    def save(self, email, firebase, img):
        db = firebase.database().child('advertisements')
        ad = self.create_dict(email, img)
        try:
            db.push(ad)
        except requests.exceptions.HTTPError:
            return {'error': requests.exceptions.HTTPError}
        return {'error': None}


class ProfileForm(forms.Form):

    first_name = forms.CharField(
        label='First Name', required=True, max_length=100)
    last_name = forms.CharField(
        label='Last Name', required=True, max_length=100)
    merchant_name = forms.CharField(
        label='Merchant Name', required=True, max_length=100)

    def save(self, firebase, id, img):
        try:
            db = firebase.database()
            old_data = db.get().val()['merchants'][id]
            new_data = {}
            new_data['first_name'] = self.data['first_name']
            new_data['last_name'] = self.data['last_name']
            new_data['merchant_name'] = self.data['merchant_name']
            new_data['username'] = old_data['username']
            new_data['profile_picture'] = img
            db.child('merchants').child(id).update(new_data)
            # new_data['name'] = self.data['first_name'] + ' ' + self.data['last_name']
            return {'result': new_data, 'error': None}
        except requests.exceptions.HTTPError:
            return {'error': requests.exceptions.HTTPError}
    # profile_picture = forms.ImageField(label='Image', required=False)