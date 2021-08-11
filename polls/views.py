# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import hashlib
import json
import os
import requests

# from myapp import email as eb
# from myapp import broadcast as tb
from hello import email as eb
from hello import broadcast as tb
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from imgurpython.helpers.error import ImgurClientRateLimitError

import datetime

import pyrebase

from django.views.decorators.csrf import csrf_exempt
import jwt

config = {
    "apiKey": os.environ['FLYIT_FIREBASE_API_KEY'],
    "authDomain": os.environ['FLYIT_FIREBASE_PROJECT_ID'] + ".firebaseapp.com",
    "databaseURL": os.environ['FLYIT_FIREBASE_DATABASE_URL'],
    "storageBucket": os.environ['FLYIT_FIREBASE_PROJECT_ID'] + ".appspot.com",
}

firebase = pyrebase.initialize_app(config)

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt 
def login(request):
    authe = firebase.auth()
    # temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        # print(email)
        try:
            # arr = json.loads(requests.get(temp).content.decode())
            # arr = arr['user']
            logindata = authe.sign_in_with_email_and_password(email, password)
        # except KeyError:
        except requests.exceptions.HTTPError as e:
            return JsonResponse({'auth': False, 'token': None, 'error': e}
            , status=401)
        merchants = firebase.database().get().val()['merchants']
        # for i in range(len(arr)):
        #     if email == arr[i]['email']:
        for _, merchant in merchants.items():
            if merchant['username'] == logindata['email']:
                # temp = hashlib.sha1(password.encode('UTF8'))
                # print(arr[i]['password'])
                # if temp.hexdigest() == arr[i]['password']:
                    # request.session['email'] = email
                    # data = get_user_data(arr, email)
                payload = {}
                payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
                # payload['url'] = '/myapp/broadcast/'
                payload['url'] = '/hello/broadcast/'
                payload['title'] = 'Broadcast'
                payload['username'] = email
                payload['first_name'] = merchant['first_name']
                payload['last_name'] = merchant['last_name']
                payload['merchant_name'] = merchant['merchant_name']
                payload['profile_picture'] = merchant['profile_picture']
                payload['login_data'] = logindata
                # tmp = {}
                # tmp['auth'] = True
                # tmp['token'] = jwt.encode(payload, os.environ["SECRET"]).decode('UTF8')
                # return HttpResponse(json.dumps(tmp))
                tmp = jwt.encode(payload, os.environ["SECRET"])
                return JsonResponse({'auth': True, 'token': tmp, 'error': None}
                , status=200)
        return JsonResponse({'auth': False, 'token': None, 'error': "Wrong username / password"}
        , status=200) 
    return JsonResponse({'auth': False, 'token': None, 'error': "Failed to Login"}
    , status=404)

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

@csrf_exempt 
def register(request):
    authe = firebase.auth()
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        merchant_name = request.POST.get('merchant_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        # profile_picture = ""
        if password == repeat_password:
            # password = hashlib.sha1(password.encode('UTF8'))
            # password = password.hexdigest()
            # link = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
            # try:
            #     arr = json.loads(requests.get(link).content.decode())
            #     temp = arr['user']
            # except KeyError:
            #     temp = []
            arr = {}
            # arr['email'] = email
            # arr['password'] = password
            arr['first_name'] = first_name
            arr['last_name'] = last_name
            arr['merchant_name'] = merchant_name
            arr['username'] = email
            arr['profile_picture'] = ''
            # temp.append(arr)
            # user = {"user": temp}
            # try:
            #     req_change = requests.put(link, json=user)
            # except ConnectionError:
            try:
                regist_data = authe.create_user_with_email_and_password(email, password)
            except requests.exceptions.HTTPError as e:
                return JsonResponse({'code': 400, 'message': 'no_record_check',
                'token': None}, status=404)
            db = firebase.database().child('merchants')
            db.child(regist_data['localId']).set(arr)
            # eb.main(temp, email)
            # request.session['email'] = email
            # eb.main(temp, email)
            # send_mail('Subject here', 'Here is the message.',
            # 'from@example.com', ['to@example.com'], fail_silently=False)
            payload = {}
            # payload['url'] = '/myapp/broadcast/'
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
            payload['url'] = '/hello/broadcast/'
            payload['title'] = 'Broadcast'
            payload['username'] = email
            payload['first_name'] = first_name
            payload['last_name'] = last_name
            # payload['name'] = first_name + ' ' + last_name
            payload['merchant_name'] = merchant_name
            # payload['profile_picture'] = profile_picture
            payload['profile_picture'] = ''
            payload['login_data'] = regist_data
            return JsonResponse({'code': 200,'message': "User registered successfully", 
            'token': jwt.encode(payload, os.environ["SECRET"])})
        return JsonResponse({'code': 200,'message': "Password not same", 
        'token': None})
    return JsonResponse({'code': 500, 'message': "Failed to Register", 
    'token': None}, status=500)

def logout(request):
    # del request.session['email']
    # return render(request, "myapp/template/logout.html", {})
    tmp = {}
    tmp['auth'] = False
    tmp['token'] = None
    tmp['error'] = None
    return JsonResponse(tmp, status=200)

@csrf_exempt 
def show_profile(request):
    tmp = verify_token(request)
    response = json.loads(tmp.content)
    if response['auth'] == False:
        return tmp
    return JsonResponse(response, status = 200)
    # url = "myapp/template/profile.html"
    # url = "hello/templates/profile.html"
    # page_title = 'My Profile'
    # temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # arr = json.loads(requests.get(temp).content.decode())
    # arr = arr['user']
    # try:
    #     tmp = response['email']
    # except KeyError:
    #     pass
    # user_data = get_user_data(arr, tmp)
    # if user_data['name'] == '':
    #     return JsonResponse({'code': 200,'message': "Name is empty"})
    # return JsonResponse({'username': tmp, 'name': user_data['name'],
    #                              'title': page_title,
    #                              'first_name': user_data['first_name'],
    #                              'last_name': user_data['last_name'],
    #                              'merchant_name': user_data['merchant_name'],
    #                              'email': user_data['email'],
    #                              'profile_picture': user_data['profile_picture']})

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

def edit_data(arr, request, form):
    for i, v in enumerate(arr['user']):
        if v['email'] == form['email']:
            arr['user'][i]['first_name'] = request.POST.get('first_name', '')
            arr['user'][i]['last_name'] = request.POST.get('last_name', '')
            arr['user'][i]['merchant_name'] = request.POST.get('merchant_name', '')
            try:
                temppath = request.FILES['profpic'].temporary_file_path()
                link = upload_image(temppath)
                arr['user'][i]['profile_picture'] = link
            except (MultiValueDictKeyError, KeyError) as e:
                arr['user'][i]['profile_picture'] = ''
            break
    return arr

@csrf_exempt 
def edit_profile(request):
    tmp = verify_token(request)
    response = json.loads(tmp.content)
    if response['auth'] == False:
        return tmp
    img = ''
    try:
        img = request.FILES['fileupload'].temporary_file_path()
    except MultiValueDictKeyError:
        pass
    else:
        if not mutate(request, img):
            return JsonResponse({ 'auth': False, 'token': None, 'payload': None,
            'error': 'No record check.' }, status=404)
            # return JsonResponse({'no_record_check': 0}, status=404)
    db = firebase.database()
    old_data = db.get().val()['merchants']
    for _, merchant in old_data.items():
        if merchant['username'] == response['payload']['username']:
            new_data = {}
            new_data['first_name'] = request.POST.get('first_name', '')
            new_data['last_name'] = request.POST.get('last_name', '')
            new_data['merchant_name'] = request.POST.get('merchant_name', '')
            new_data['username'] = old_data['username']
            new_data['profile_picture'] = img
            db.child('merchants').child(response['payload']['login_data']['localId']).update(new_data)
    # temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # arr = json.loads(requests.get(temp).content.decode())
    # arr = edit_data(arr, request, response)
    # jsondata = json.dumps(arr)
    # headers = {'Content-type': 'application/json'}
    # try:
    #     req_change = requests.put(temp, data=jsondata, headers=headers)
    # except ConnectionError:
    #     return JsonResponse({'no_record_check': 0}, status=404)
    # print(req_change.content.decode())
            print(">> change server status complete")
    return show_profile(request)

def mutate(request, item):
    mutable = request.POST._mutable
    request.POST._mutable = True
    link = upload_image(item)
    if link == 'Error':
        return False
    request.POST['img'] = link
    request.POST._mutable = mutable
    return True

def create_ad_dict(request, ads):
    temp = {}
    temp['title'] = request.POST.get('title', '')
    temp['description'] = request.POST.get('desc', '')
    temp['author'] = ads['author']
    temp['publish'] = str(ads['published_date'])
    temp['lat'] = request.POST.get('latitude', '')
    temp['long'] = request.POST.get('longitude', '')
    temp['tag'] = request.POST.get('tag', '')
    try:
        temp['img'] = request.POST.get('img', '')
    except MultiValueDictKeyError:
        temp['img'] = ''
    return temp

@csrf_exempt 
def broadcast(request):
    tmp = verify_token(request)
    response = json.loads(tmp.content)
    if response['auth'] == False:
        return tmp
    # check if image has uploaded
    # check whether it's valid:
    img = ''
    try:
        img = request.FILES['fileupload'].temporary_file_path()
    except MultiValueDictKeyError:
        pass
    else:
        if not mutate(request, img):
            return JsonResponse({ 'auth': False, 'token': None, 'payload': None,
            'error': 'No record check.' }, status=404)
            # return JsonResponse({'no_record_check': 0}, status=404)
    ads = {}
    # ads['author'] = response['email']
    ads['author'] = response['payload']['username']
    ads['published_date'] = timezone.now()
    # try:
    #     temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
    #     arr = json.loads(requests.get(temp).content.decode())
    #     arr = arr['advertisements']
    # except KeyError:
    #     arr = []
    temp = create_ad_dict(request, ads)
    # arr.append(temp)
    # print(arr)
    # if tb.main(arr):
    #     return JsonResponse({"title": temp['title'], "description": temp['description'],
    #              "image": temp['img'], "author": temp['author'], "publish": temp['publish'],
    #              "lat": temp['lat'], "long": temp['long'], "tag": temp['tag']}, status=200)
    # else:
    #     return JsonResponse({'no_record_check': 1}, status=404)
    db = firebase.database().child('advertisements')
    try:
        db.push(temp)
    except requests.exceptions.HTTPError:
        return JsonResponse({ 'auth': False, 'token': None, 'payload': None,
            'error': requests.exceptions.HTTPError }, status=500)
        # return {'error': requests.exceptions.HTTPError}
    # return {'error': None}
    return JsonResponse(response, status=200)

@csrf_exempt 
def statistic(request):
    tmp = verify_token(request)
    response = json.loads(tmp.content)
    if response['auth'] == False:
        return tmp
    # queryset = Ads.objects.all()
    # temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
    # arr = json.loads(requests.get(temp).content.decode())
    # arr = arr['advertisements']
    # tmp = []
    data = {}
    page_title = "Statistics"
    data['title'] = page_title
    data_ads = firebase.database().get().val()['advertisements']
    ads = []
    username = response['payload']['username']
    # for v in arr:
    #     if v['author'] == username:
    #         tmp.append(v)
    for v in data_ads:
        if data_ads[v]['author'] == username:
            ads.append(data_ads[v])
    data['ads'] = ads
    # print(tmp)
    # temp1 = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    # arr1 = json.loads(requests.get(temp1).content.decode())
    # arr1 = arr1['user']
    # temp = get_user_data(arr1, username)
    # url = "myapp/template/statistic.html"
    # url = "hello/templates/statistic.html"
    # return JsonResponse({'username': username, 'name': temp['name'],
    #                              'title': page_title,
    #                              'first_name': temp['first_name'],
    #                              'last_name': temp['last_name'],
    #                              'merchant_name': temp['merchant_name'],
    #                              'profile_picture': temp['profile_picture'], 'ads': tmp}, status=200)
    response['data'] = data
    return JsonResponse(response, status = 200)

def verify_token(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        if token == '':
            return JsonResponse({ 'auth': False, 'token': None, 'payload': None,
            'error': 'No token provided.' }, status=500)
        else:
            try:
                payload = jwt.decode(token, os.environ["SECRET"], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                # Signature has expired
                return JsonResponse({ 'auth': False, 'token': None, 'payload': None,
                'error': 'Failed to authenticate token.' }, status=403)
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
            return JsonResponse({'auth': True, 'token': jwt.encode(payload, os.environ["SECRET"])
            , 'payload': payload, 'error': None}, status=200)
    return JsonResponse({'auth': False, 'token': None, 'payload': None,
    'error': "Failed to Authenticate"}, status=500)
