from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# from django.shortcuts import redirect, render, render_to_response
from django.shortcuts import redirect, render
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

import pyrebase

config = {
    "apiKey": os.environ['FLYIT_FIREBASE_API_KEY'],
    "authDomain": os.environ['FLYIT_FIREBASE_PROJECT_ID'] + ".firebaseapp.com",
    "databaseURL": os.environ['FLYIT_FIREBASE_DATABASE_URL'],
    "storageBucket": os.environ['FLYIT_FIREBASE_PROJECT_ID'] + ".appspot.com",
    # "serviceAccount": {
    #     "type": os.environ['FLYIT_FIREBASE_TYPE'],
    #     "project_id": os.environ['FLYIT_FIREBASE_PROJECT_ID'],
    #     "private_key_id": os.environ['FLYIT_FIREBASE_PRIVATE_KEY_ID'],
    #     "private_key": os.environ['FLYIT_FIREBASE_PRIVATE_KEY'],
    #     "client_email": os.environ['FLYIT_FIREBASE_CLIENT_EMAIL'],
    #     "client_id": os.environ['FLYIT_FIREBASE_CLIENT_ID'],
    #     "auth_uri": os.environ['FLYIT_FIREBASE_AUTH_URL'],
    #     "token_uri": os.environ['FLYIT_FIREBASE_TOKEN_URL'],
    #     "auth_provider_x509_cert_url": os.environ['FLYIT_FIREBASE_AUTH_PROVIDER'],
    #     "client_x509_cert_url": os.environ['FLYIT_FIREBASE_CERT_URL'],
    # }
}

firebase = pyrebase.initialize_app(config)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            reg = form.save()
            reg.save()
            return redirect('loggedin')
    else:
        form = RegisterForm()
    return render(request, "register.html", {'form': form})


def login(request):
    authe = firebase.auth()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            result = form.login(authe, firebase)
            # print(config, result)
            if result['error'] is not None:
                form = LoginForm()
                return render(request, "login.html", {'form': form, 'fail': True})
            request.session['auth'] = result['auth']
            request.session['userData'] = result['result']
            return render(request, 'broadcast.html', result['result'])
            # reg = form.save()
            # reg.save()
            # return redirect('loggedin')
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})


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
                    # url = '/myapp/broadcast/'
                    url = '/hello/broadcast/'
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
            # url = '/myapp/broadcast/'
            url = '/hello/broadcast/'
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
    # return render_to_response('invalid_login.html')
    render('invalid_login.html')


def logout(request):
    # del request.session['email']
    # return render(request, "logout.html", {})
    try:
        del request.session['auth']
        del request.session['userData']
    except (MultiValueDictKeyError, KeyError) as e:
        return render(request, "login.html", {})
    return render(request, "logout.html", {})

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
    # user_temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # user_arr = json.loads(requests.get(user_temp).content.decode())['user']
    temp = "broadcast.html"
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
            pass
        else:
            img = {}
            img['url'] = ''
            if not mutate(request, img):
                return redirect('response/', {'no_record_check': 0})
        # print(form.data)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ads = form.save()
            # ads.author = request.session['email']
            # ads.published_date = timezone.now()
            # ads.save()
            # try:
            #     temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
            #     arr = json.loads(requests.get(temp).content.decode())
            #     arr = arr['advertisements']
            # except KeyError:
            #     arr = []
            # temp = create_ad_dict(form, ads)
            # arr.append(temp)
            # print(arr)
            ads = form.save(request.session['userData']['username'], firebase, img['url'])
            # print(ads['error'])
            if ads['error'] is None:
                return redirect('statistic/')
            # if tb.main(arr):
            #     return redirect('response/', {'record_check': 1})
            else:
                form = AdsForm()
                user_data['form'] = form
                user_data['fail'] = True
                return render(request, temp, user_data)
                # return redirect('response/', {'no_record_check': 0})
    form = AdsForm()
    user_data['form'] = form
    return render(request, temp, user_data)
    # print(form.errors)
    # temp = "broadcast.html"
    # tmp = request.session['email']
    # page_title = 'Broadcast'
    # user_data = get_user_data(user_arr, tmp)
    # if user_data['name'] == '':
    #     return redirect(register)
    # return render(request, temp, {'form': form, 'username': tmp, 'title': page_title,
    #                               'name': user_data['name'],
    #                               'merchant_name': user_data['merchant_name'],
    #                               'profile_picture': user_data['profile_picture']})


def index(request):
    return render(request, "index.html", {})


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
    url = "profile.html"
    page_title = 'My Profile'
    # temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # arr = json.loads(requests.get(temp).content.decode())
    # arr = arr['user']
    # tmp = ''
    # try:
    #     tmp = request.session['email']
    # except KeyError:
    #     pass
    # user_data = get_user_data(arr, tmp)
    try:
        user_data = request.session['userData']
    except KeyError:
    # if user_data['name'] == '':
        render(request, "login.html", {})
        # return redirect('/hello/register/')
        # return redirect('/myapp/register/')
    user_data['title'] = page_title
    return render(request, url, user_data)
    # return render(request, url, {'username': tmp, 'name': user_data['name'],
    #                              'title': page_title,
    #                              'first_name': user_data['first_name'],
    #                              'last_name': user_data['last_name'],
    #                              'merchant_name': user_data['merchant_name'],
    #                              'email': user_data['email'],
    #                              'profile_picture': user_data['profile_picture']})


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
    # temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # arr = json.loads(requests.get(temp).content.decode())
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # arr = edit_data(arr, request, form)
            # jsondata = json.dumps(arr)
            # headers = {'Content-type': 'application/json'}
            try:
            #     req_change = requests.put(temp, data=jsondata, headers=headers)
            # except ConnectionError:
            #     return redirect('response/', {'no_record_check': 0})
            # print(req_change.content.decode())
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
        # arr = arr['user']
        form = ProfileForm()
        try:
            tmp = request.session['userData']
            # tmp = request.session['email']
        except KeyError:
            tmp = ''
        # user_data = get_user_data(arr, tmp)
        # if user_data['name'] == '':
            return render(request, "login.html", {})
            # return redirect('/hello/register/')
            # return redirect('/myapp/register/')
        url = "editProfile.html"
        page_title = 'Edit Profile'
        tmp['form'] = form
        tmp['title'] = page_title
        return render(request, url, tmp)
        # return render(request, url, {'form': form, 'username': tmp,
        #                              'name': user_data['name'], 'title': page_title,
        #                              'first_name': user_data['first_name'],
        #                              'last_name': user_data['last_name'],
        #                              'merchant_name': user_data['merchant_name'],
        #                              'profile_picture': user_data['profile_picture']})


def edit_success(request):
    url = "editSuccess.html"
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
        return redirect('/hello/register/')
        # return redirect('/myapp/register/')
    return render(request, url, {'username': tmp, 'name': temp['name'], 'title': page_title,
                                 'first_name': temp['first_name'],
                                 'last_name': temp['last_name'],
                                 'merchant_name': temp['merchant_name'],
                                 'profile_picture': temp['profile_picture']})


def statistic(request):
    # queryset = Ads.objects.all()
    # temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
    # arr = json.loads(requests.get(temp).content.decode())
    # arr = arr['advertisements']
    # tmp = []
    # username = request.session['email']
    # for v in arr:
    #     if v['author'] == username:
    #         tmp.append(v)
    # print(tmp)
    # temp1 = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # arr1 = json.loads(requests.get(temp1).content.decode())
    # arr1 = arr1['user']
    # temp = get_user_data(arr1, username)
    page_title = "Statistics"
    url = "statistic.html"
    # return render(request, url, {'username': username, 'name': temp['name'],
    #                              'title': page_title,
    #                              'first_name': temp['first_name'],
    #                              'last_name': temp['last_name'],
    #                              'merchant_name': temp['merchant_name'],
    #                              'profile_picture': temp['profile_picture'], 'ads': tmp})
    try:
        data = request.session['userData']
    except KeyError:
        return render(request, "login.html", {})
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
#     return render(request, "uploadfileapp/user_form.html", {})


# Create your views here.
def landing(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "landing.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
