from django.shortcuts import redirect, render, render_to_response
from .forms import RegisterForm, LoginForm, ProfileForm, AdsForm

import hashlib
import json
import os
import requests
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
# from django.views import generic
# from django.views.generic import CreateView
from django.utils import timezone

# from django.urls import reverse
from . import broadcast as tb
from . import email as eb

# from .models import User
# from .models import Ads
# from django.shortcuts import render
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from imgurpython.helpers.error import ImgurClientRateLimitError
# from django.core.context_processors import csrf

# from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            reg = form.save()
            reg.save()
            return redirect('loggedin')
    else:
        form = RegisterForm()
    return render(request, "myapp/template/register.html", {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            reg = form.save()
            reg.save()
            return redirect('loggedin')
    else:
        form = LoginForm()
    return render(request, "myapp/template/login.html", {'form': form})


def loggedin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
            arr = json.loads(requests.get(temp).content.decode())
            arr = arr['user']
        except KeyError:
            return redirect('register')
        for i in range(len(arr)):
            if email == arr[i]['email']:
                temp = hashlib.sha1(password.encode('UTF8'))
                if temp.hexdigest() == arr[i]['password']:
                    request.session['email'] = email
                    data = get_user_data(arr, email)
                    url = '/myapp/broadcast/'
                    page_title = 'Broadcast'
                    return redirect(url, {'username': email, 'title': page_title,
                                          'name': data['name'],
                                          'merchant_name': data['merchant_name'],
                                          'profile_picture': data['profile_picture']})
    return redirect('login')


def registered(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        merchant_name = request.POST.get('merchant_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        profile_picture = ""
        if password == repeat_password:
            password = hashlib.sha1(password.encode('UTF8'))
            password = password.hexdigest()
            try:
                temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
                arr = json.loads(requests.get(temp).content.decode())
                temp = arr['user']
            except KeyError:
                temp = []
            arr = {}
            arr['email'] = email
            arr['password'] = password
            arr['first_name'] = first_name
            arr['last_name'] = last_name
            arr['merchant_name'] = merchant_name
            arr['profile_picture'] = profile_picture
            temp.append(arr)
            eb.main(temp, email)
            request.session['email'] = email
            eb.main(temp, email)
            # send_mail('Subject here', 'Here is the message.',
            # 'from@example.com', ['to@example.com'], fail_silently=False)
            url = '/myapp/broadcast/'
            page_title = 'Broadcast'
            name = first_name + ' ' + last_name
            return redirect(url, {'username': request.session['email'],
                                  'title': page_title, 'name': name,
                                  'merchant_name': merchant_name,
                                  'profile_picture': profile_picture})
        else:
            return redirect('register')
    else:
        return redirect('register')


def invalid_login(request):
    return render_to_response('myapp/template/invalid_login.html')


def logout(request):
    del request.session['email']
    return render(request, "myapp/template/logout.html", {})


def upload_image(img):
    imgur_key = os.environ['IMGUR_CLIENT_SECRET']
    imgur_id = os.environ['IMGUR_CLIENT_ID']
    client = ImgurClient(imgur_id, imgur_key)
    try:
        response = client.upload_from_path(img, config=None, anon=True)
    except (ConnectionError, ImgurClientError, ImgurClientRateLimitError) as e:
        return 'Error'
    # print(response)
    return response['link']


def mutate(request, item):
    mutable = request.POST._mutable
    request.POST._mutable = True
    link = upload_image(item)
    if link == 'Error':
        return False
    request.POST['img'] = link
    request.POST._mutable = mutable
    return True


def create_ad_dict(form, ads):
    temp = {}
    temp['title'] = form.data['title']
    temp['description'] = form.data['desc']
    temp['author'] = str(ads.author)
    temp['publish'] = str(ads.published_date)
    temp['lat'] = form.data['latitude']
    temp['long'] = form.data['longitude']
    temp['tag'] = form.data['tag']
    try:
        temp['img'] = form.data['img']
    except MultiValueDictKeyError:
        temp['img'] = ''
    return temp


def broadcast(request):
    user_temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    user_arr = json.loads(requests.get(user_temp).content.decode())['user']
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AdsForm(request.POST)
        # check if image has uploaded
        # check whether it's valid:
        try:
            img = request.FILES['fileupload'].temporary_file_path()
        except MultiValueDictKeyError:
            pass
        else:
            if not mutate(request, img):
                return redirect('response/', {'no_record_check': 0})
        # print(form.data)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            ads = form.save()
            ads.author = request.session['email']
            ads.published_date = timezone.now()
            ads.save()
            try:
                temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
                arr = json.loads(requests.get(temp).content.decode())
                arr = arr['advertisements']
            except KeyError:
                arr = []
            temp = create_ad_dict(form, ads)
            arr.append(temp)
            # print(arr)
            if tb.main(arr):
                return redirect('response/', {'record_check': 1})
            else:
                return redirect('response/', {'no_record_check': 0})
    form = AdsForm()
    # print(form.errors)
    temp = "myapp/template/broadcast.html"
    tmp = request.session['email']
    page_title = 'Broadcast'
    user_data = get_user_data(user_arr, tmp)
    if user_data['name'] == '':
        return redirect(register)
    return render(request, temp, {'form': form, 'username': tmp, 'title': page_title,
                                  'name': user_data['name'],
                                  'merchant_name': user_data['merchant_name'],
                                  'profile_picture': user_data['profile_picture']})


def index(request):
    return render(request, "myapp/template/index.html", {})


def get_user_data(arr, email):
    user_data = {}
    for i, v in enumerate(arr):
        if v['email'] == email:
            user_data['name'] = v['first_name'] + ' ' + v['last_name']
            user_data['first_name'] = v['first_name']
            user_data['last_name'] = v['last_name']
            user_data['merchant_name'] = v['merchant_name']
            user_data['profile_picture'] = v['profile_picture']
            user_data['email'] = v['email']
            break
        else:
            user_data['name'] = ''
            user_data['first_name'] = ''
            user_data['last_name'] = ''
            user_data['merchant_name'] = ''
            user_data['profile_picture'] = ''
            user_data['email'] = ''
    return user_data


def show_profile(request):
    url = "myapp/template/profile.html"
    page_title = 'My Profile'
    temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    arr = json.loads(requests.get(temp).content.decode())
    arr = arr['user']
    tmp = ''
    try:
        tmp = request.session['email']
    except KeyError:
        pass
    user_data = get_user_data(arr, tmp)
    if user_data['name'] == '':
        return redirect('/myapp/register/')
    return render(request, url, {'username': tmp, 'name': user_data['name'],
                                 'title': page_title,
                                 'first_name': user_data['first_name'],
                                 'last_name': user_data['last_name'],
                                 'merchant_name': user_data['merchant_name'],
                                 'email': user_data['email'],
                                 'profile_picture': user_data['profile_picture']})


def edit_data(arr, request, form):
    for i, v in enumerate(arr['user']):
        if v['email'] == request.session['email']:
            arr['user'][i]['first_name'] = form.data['first_name']
            arr['user'][i]['last_name'] = form.data['last_name']
            arr['user'][i]['merchant_name'] = form.data['merchant_name']
            try:
                temppath = request.FILES['profpic'].temporary_file_path()
                link = upload_image(temppath)
                arr['user'][i]['profile_picture'] = link
            except (MultiValueDictKeyError, KeyError) as e:
                arr['user'][i]['profile_picture'] = ''
            break
    return arr


def edit_profile(request):
    temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    arr = json.loads(requests.get(temp).content.decode())
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            arr = edit_data(arr, request, form)
            jsondata = json.dumps(arr)
            headers = {'Content-type': 'application/json'}
            try:
                req_change = requests.put(temp, data=jsondata, headers=headers)
            except ConnectionError:
                return redirect('response/', {'no_record_check': 0})
            print(req_change.content.decode())
            # print(">> change server status complete")
            return redirect('edit_success')
    else:
        arr = arr['user']
        form = ProfileForm()
        try:
            tmp = request.session['email']
        except KeyError:
            tmp = ''
        user_data = get_user_data(arr, tmp)
        if user_data['name'] == '':
            return redirect('/myapp/register/')
        url = "myapp/template/editProfile.html"
        page_title = 'Edit Profile'
        return render(request, url, {'form': form, 'username': tmp,
                                     'name': user_data['name'], 'title': page_title,
                                     'first_name': user_data['first_name'],
                                     'last_name': user_data['last_name'],
                                     'merchant_name': user_data['merchant_name'],
                                     'profile_picture': user_data['profile_picture']})


def edit_success(request):
    url = "myapp/template/editSuccess.html"
    page_title = 'Edit Success!'
    temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    arr = json.loads(requests.get(temp).content.decode())
    arr = arr['user']
    tmp = ''
    try:
        tmp = request.session['email']
    except KeyError:
        pass
    temp = get_user_data(arr, tmp)
    if temp['name'] == '':
        return redirect('/myapp/register/')
    return render(request, url, {'username': tmp, 'name': temp['name'], 'title': page_title,
                                 'first_name': temp['first_name'],
                                 'last_name': temp['last_name'],
                                 'merchant_name': temp['merchant_name'],
                                 'profile_picture': temp['profile_picture']})


def statistic(request):
    # queryset = Ads.objects.all()
    temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
    arr = json.loads(requests.get(temp).content.decode())
    arr = arr['advertisements']
    tmp = []
    username = request.session['email']
    for v in arr:
        if v['author'] == username:
            tmp.append(v)
    print(tmp)
    temp1 = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    arr1 = json.loads(requests.get(temp1).content.decode())
    arr1 = arr1['user']
    temp = get_user_data(arr1, username)
    page_title = "Statistics"
    url = "myapp/template/statistic.html"
    return render(request, url, {'username': username, 'name': temp['name'],
                                 'title': page_title,
                                 'first_name': temp['first_name'],
                                 'last_name': temp['last_name'],
                                 'merchant_name': temp['merchant_name'],
                                 'profile_picture': temp['profile_picture'], 'ads': tmp})
# def upload(request):
#     return render(request, "myapp/template/uploadfileapp/user_form.html", {})
