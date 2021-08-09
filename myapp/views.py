from django.shortcuts import redirect, render, render_to_response
from .forms import RegisterForm, LoginForm, ProfileForm, AdsForm

# import hashlib
import json
import os
import requests
import random
from django.utils.datastructures import MultiValueDictKeyError

import pyrebase
# from django.contrib import auth

# Create your views here.
# from django.views import generic
# from django.views.generic import CreateView
# from django.utils import timezone

# from django.urls import reverse
# from . import broadcast as tb
# from . import email as eb

# from .models import User
# from .models import Ads
# from django.shortcuts import render
# from imgurpython import ImgurClient
# from imgurpython.helpers.error import ImgurClientError
# from imgurpython.helpers.error import ImgurClientRateLimitError
# from django.core.context_processors import csrf

# from django.core.mail import send_mail
temp = 'https://api.myjson.com/bins/' + os.environ['FIREBASE_API_KEY']
config = json.loads(requests.get(temp).content.decode())
firebase = pyrebase.initialize_app(config)


def register(request):
    # request.session['firebase'] = firebase
    authe = firebase.auth()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            result = form.register(authe, firebase)
            if result['error'] is not None:
                form = RegisterForm()
                return render(request, "myapp/template/register.html", {'form': form,
                                                                        'fail': True})
            request.session['auth'] = result['auth']
            request.session['userData'] = result['result']
            return redirect('/myapp/broadcast/', result['result'])
    else:
        form = RegisterForm()
    return render(request, "myapp/template/register.html", {'form': form})


def login(request):
    authe = firebase.auth()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            result = form.login(authe, firebase)
            if result['error'] is not None:
                form = LoginForm()
                return render(request, "myapp/template/login.html", {'form': form,
                                                                     'fail': True})
            request.session['auth'] = result['auth']
            request.session['userData'] = result['result']
            return redirect('/myapp/broadcast/', result['result'])
    else:
        form = LoginForm()
    return render(request, "myapp/template/login.html", {'form': form})


def invalid_login(request):
    return render_to_response('myapp/template/invalid_login.html')


def logout(request):
    try:
        del request.session['auth']
        del request.session['userData']
    except (MultiValueDictKeyError, KeyError) as e:
        return redirect('register')
    return render(request, "myapp/template/logout.html", {})


def upload_image(img, firebase, id):
    folder = str(random.random())
    storage = firebase.storage()
    image_firebase = storage.child('images/' + folder, id)
    try:
        image_firebase.put(img)
    except requests.exceptions.HTTPError:
        return {'error': requests.exceptions.HTTPError}
    image_firebase = storage.child('images/' + folder, id)
    return {'url': image_firebase.get_url(None), 'error': None}


def broadcast(request):
    temp = "myapp/template/broadcast.html"
    page_title = 'Broadcast'
    try:
        user_data = request.session['userData']
    except KeyError:
        return redirect('register')
    user_data['title'] = page_title
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AdsForm(request.POST)
        # check if image has uploaded
        # check whether it's valid:
        try:
            tmp = request.FILES['fileupload'].temporary_file_path()
            img = upload_image(tmp, firebase, request.session['auth']['idToken'])
            if img['error'] is not None:
                raise MultiValueDictKeyError
        except MultiValueDictKeyError:
            img = {}
            img['url'] = ''
        # print(form.data)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            ads = form.save(request.session['userData']['username'], firebase, img['url'])
            # print(arr)
            print(ads['error'])
            if ads['error'] is None:
                return redirect('statistic/')
            else:
                form = AdsForm()
                user_data['form'] = form
                user_data['fail'] = True
                return render(request, temp, user_data)
    form = AdsForm()
    user_data['form'] = form
    # print(form.errors)
    return render(request, temp, user_data)


def index(request):
    return render(request, "myapp/template/index.html", {})


def show_profile(request):
    url = "myapp/template/profile.html"
    page_title = 'My Profile'
    try:
        data = request.session['userData']
    except KeyError:
        return redirect('/myapp/register/')
    data['title'] = page_title
    return render(request, url, data)


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            try:
                temppath = request.FILES['profpic'].temporary_file_path()
                link = upload_image(temppath, firebase, request.session['auth']['idToken'])
                if link['error'] is not None:
                    raise requests.exceptions.HTTPError
            except (MultiValueDictKeyError, KeyError) as e:
                link['url'] = ''
            except requests.exceptions.HTTPError:
                return redirect('register')
            request.session['userData'] = form.save(firebase,
                                                    request.session['auth']['localId'],
                                                    link['url'])['result']
            # print(">> change server status complete")
            return redirect('edit_success')
    else:
        form = ProfileForm()
        try:
            tmp = request.session['userData']
        except KeyError:
            return redirect('/myapp/register/')
        url = "myapp/template/editProfile.html"
        page_title = 'Edit Profile'
        tmp['form'] = form
        tmp['title'] = page_title
        return render(request, url, tmp)


def edit_success(request):
    url = "myapp/template/editSuccess.html"
    page_title = 'Edit Success!'
    try:
        data = request.session['userData']
    except KeyError:
        return redirect('/myapp/register/')
    data['title'] = page_title
    return render(request, url, data)


def statistic(request):
    try:
        data = request.session['userData']
    except KeyError:
        return redirect('/myapp/register/')
    page_title = "Statistics"
    url = "myapp/template/statistic.html"
    data['title'] = page_title
    data_ads = firebase.database().get().val()['advertisements']
    email = request.session['auth']['email']
    ads = []
    for v in data_ads:
        if data_ads[v]['author'] == email:
            ads.append(data_ads[v])
    data['ads'] = ads
    return render(request, url, data)
# def upload(request):
#     return render(request, "myapp/template/uploadfileapp/user_form.html", {})
