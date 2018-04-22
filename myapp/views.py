from django.shortcuts import redirect, render, render_to_response
from .forms import RegisterForm, LoginForm

import hashlib
import json
import os
import requests
# from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
# from django.views import generic
# from django.views.generic import CreateView
from django.utils import timezone

# from django.urls import reverse
from . import broadcast as tb

# from .models import User
# from .models import Ads
from .forms import AdsForm
# from django.shortcuts import render
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from imgurpython.helpers.error import ImgurClientRateLimitError
# from django.core.context_processors import csrf


# def hello(request):
#     return render(request, "myapp/template/hello.html", {})


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


# def header(request):
#     return render(request, "myapp/template/header.html", {})


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


# def footer(request):
#     return render(request, "myapp/template/footer.html", {})

# def auth_view(request):
    # if request.method == 'POST':
    # email = request.POST.get('email', '')
    # password = request.POST.get('password', '')
    # request.session['email'] = email
    # return HttpResponseRedirect('/myapp/loggedin/')
    # user = auth.authenticate(username=email, password=password)

    # if user is not None:
    # 	auth.login(request, user)
    # 	return HttpResponseRedirect('/loggedin')
    # else:
    # 	return HttpResponseRedirect('/invalid')


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
                    url = 'myapp/template/broadcast.html'
                    page_title = 'Broadcast'
                    return render(request, url, {'username': email, 'title': page_title,
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
            # email = hashlib.sha1(email.encode('UTF8'))
            # email = email.hexdigest()
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
            print(arr)
            # headers = {'Content-type': 'application/json'}
            # data = json.dumps(arr)
            # location = os.environ['DOMAIN'] + '/static/text/user.txt'
            # req_change = requests.put(location, data=data, headers=headers)
            temp.append(arr)
            user = {"user": temp}
            data = json.dumps(user)
            headers = {'Content-type': 'application/json'}
            link = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
            try:
                req_change = requests.put(link, data=data, headers=headers)
            except ConnectionError:
                return redirect('response/', {'no_record_check': 0})
            print(req_change.content.decode())
            print(">> change server status complete")
            request.session['email'] = email
            url = 'myapp/template/broadcast.html'
            page_title = 'Broadcast'
            name = first_name + ' ' + last_name
            return render_to_response(url, {'username': request.session['email'],
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
    return render(request, "myapp/template/logout.html", {})


# def maps(request):
#     return render(request, "myapp/template/maps.html", {})


# def send(request):
#     if request.is_ajax():
#         # extract your params (also, remember to validate them)
#         param = request.POST.get('param', None)
#         another_param = request.POST.get('another param', None)

#         # construct your JSON response by calling a data method from elsewhere
#         items, summary = build_my_response(param, another_param)

#         return JsonResponse({'result': 'OK', 'data': {'items': items, 'summary': summary}})
#     return HttpResponseBadRequest()


# def location(request):
#     if request.method == 'POST':
#         address = request.POST.get('address', '')
#         request.session['address'] = address
#     temp = 'myapp/template/hello.html'
#     return render_to_response(temp, {'address': request.session['address']})


# class HomeView(generic.ListView):
#     # name of the object to be used in the index.html
#     context_object_name = 'user_list'
#     template_name = 'myapp/template/uploadfileapp/home_page.html'

#     def get_queryset(self):
#         return User.objects.all()


# # view for the user entry page
# class UserEntry(CreateView):
#     model = User
#     fields = ['user_name', 'user_avatar']
#     template_name = 'myapp/template/uploadfileapp/user_form.html'


def upload_image(img):
    imgur_key = os.environ['IMGUR_CLIENT_SECRET']
    imgur_id = os.environ['IMGUR_CLIENT_ID']
    client = ImgurClient(imgur_id, imgur_key)
    try:
        response = client.upload_from_path(img, config=None, anon=True)
    except ConnectionError:
        return redirect('response/', {'no_record_check': 0})
    except ImgurClientError:
        return redirect('response/', {'no_record_check': 0})
    except ImgurClientRateLimitError:
        return redirect('response/', {'no_record_check': 0})
    # print(response)
    return response['link']


def mutate(request, item):
    mutable = request.POST._mutable
    request.POST._mutable = True
    link = upload_image(item)
    request.POST['img'] = link
    request.POST._mutable = mutable


def create_ad_dict(form, ads):
    temp = {}
    temp['title'] = form.data['title']
    temp['description'] = form.data['desc']
    temp['author'] = str(ads.author)
    temp['publish'] = str(ads.published_date)
    temp['lat'] = form.data['latitude']
    temp['long'] = form.data['longitude']
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
            mutate(request, img)
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
        redirect(register)
    return render(request, temp, {'form': form, 'username': tmp, 'title': page_title,
                                  'name': user_data['name'],
                                  'merchant_name': user_data['merchant_name'],
                                  'profile_picture': user_data['profile_picture']})


def index(request):
    return render(request, "myapp/template/index.html", {})


# def upload(request):
#     return render(request, "myapp/template/uploadfileapp/user_form.html", {})


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
