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

import jwt, datetime

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        # print(email)
        try:
            arr = json.loads(requests.get(temp).content.decode())
            arr = arr['user']
        except KeyError:
            return JsonResponse({'auth': False, 'token': None}, status=401)
        for i in range(len(arr)):
            if email == arr[i]['email']:
                temp = hashlib.sha1(password.encode('UTF8'))
                # print(arr[i]['password'])
                if temp.hexdigest() == arr[i]['password']:
                    # request.session['email'] = email
                    data = get_user_data(arr, email)
                    payload = {}
                    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
                    # payload['url'] = '/myapp/broadcast/'
                    payload['url'] = '/hello/broadcast/'
                    payload['title'] = 'Broadcast'
                    payload['username'] = email
                    payload['name'] = data['name']
                    payload['merchant_name'] = data['merchant_name']
                    payload['profile_picture'] = data['profile_picture']
                    # tmp = {}
                    # tmp['auth'] = True
                    # tmp['token'] = jwt.encode(payload, os.environ["SECRET"]).decode('UTF8')
                    # return HttpResponse(json.dumps(tmp))
                    tmp = jwt.encode(payload, os.environ["SECRET"]).decode('UTF8')
                    return JsonResponse({'auth': True, 'token': tmp}, status=200)
        return JsonResponse({'auth': False, 'token': None}, status=200) 
    return JsonResponse({'auth': False, 'message': "Failed to Login"}, status=404)

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

def register(request):
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
            link = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
            try:
                arr = json.loads(requests.get(link).content.decode())
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
            user = {"user": temp}
            try:
                req_change = requests.put(link, json=user)
            except ConnectionError:
                return JsonResponse({'no_record_check': 0}, status=404)
            # eb.main(temp, email)
            # request.session['email'] = email
            # eb.main(temp, email)
            # send_mail('Subject here', 'Here is the message.',
            # 'from@example.com', ['to@example.com'], fail_silently=False)
            payload = {}
            # payload['url'] = '/myapp/broadcast/'
            payload['url'] = '/hello/broadcast/'
            payload['title'] = 'Broadcast'
            payload['name'] = first_name + ' ' + last_name
            payload['username'] = email
            payload['merchant_name'] = merchant_name
            payload['profile_picture'] = profile_picture
            return JsonResponse({'code': 200,'message': "User registered successfully", 
            'token': jwt.encode(payload, os.environ["SECRET"]).decode('UTF8')})
        return JsonResponse({'code': 200,'message': "Password not same", 
        'token': None})
    return JsonResponse({'auth': False, 'message': "Failed to Register"}, status=500)

def logout(request):
    # del request.session['email']
    # return render(request, "myapp/template/logout.html", {})
    tmp = {}
    tmp['auth'] = False
    tmp['token'] = None
    return JsonResponse(tmp, status=200)

def show_profile(request):
    tmp = verify_token(request)
    response = json.loads(tmp.content)
    if response['auth'] == False:
        return tmp
    # url = "myapp/template/profile.html"
    url = "hello/templates/profile.html"
    page_title = 'My Profile'
    temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    arr = json.loads(requests.get(temp).content.decode())
    arr = arr['user']
    try:
        tmp = response['email']
    except KeyError:
        pass
    user_data = get_user_data(arr, tmp)
    if user_data['name'] == '':
        return JsonResponse({'code': 200,'message': "Name is empty"})
    return JsonResponse({'username': tmp, 'name': user_data['name'],
                                 'title': page_title,
                                 'first_name': user_data['first_name'],
                                 'last_name': user_data['last_name'],
                                 'merchant_name': user_data['merchant_name'],
                                 'email': user_data['email'],
                                 'profile_picture': user_data['profile_picture']})

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

def edit_profile(request):
    tmp = verify_token(request)
    response = json.loads(tmp.content)
    if response['auth'] == False:
        return tmp
    temp = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    arr = json.loads(requests.get(temp).content.decode())
    arr = edit_data(arr, request, response)
    jsondata = json.dumps(arr)
    headers = {'Content-type': 'application/json'}
    try:
        req_change = requests.put(temp, data=jsondata, headers=headers)
    except ConnectionError:
        return JsonResponse({'no_record_check': 0}, status=404)
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
            return JsonResponse({'no_record_check': 0}, status=404)
    ads = {}
    ads['author'] = response['email']
    ads['published_date'] = timezone.now()
    try:
        temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
        arr = json.loads(requests.get(temp).content.decode())
        arr = arr['advertisements']
    except KeyError:
        arr = []
    temp = create_ad_dict(request, ads)
    arr.append(temp)
    # print(arr)
    if tb.main(arr):
        return JsonResponse({"title": temp['title'], "description": temp['description'],
                 "image": temp['img'], "author": temp['author'], "publish": temp['publish'],
                 "lat": temp['lat'], "long": temp['long'], "tag": temp['tag']}, status=200)
    else:
        return JsonResponse({'no_record_check': 1}, status=404)

def statistic(request):
    tmp = verify_token(request)
    response = json.loads(tmp.content)
    if response['auth'] == False:
        return tmp
    # queryset = Ads.objects.all()
    temp = 'https://api.myjson.com/bins/' + os.environ['JSON_API_ID']
    arr = json.loads(requests.get(temp).content.decode())
    arr = arr['advertisements']
    tmp = []
    username = response['email']
    for v in arr:
        if v['author'] == username:
            tmp.append(v)
    # print(tmp)
    temp1 = 'https://api.myjson.com/bins/' + os.environ['ARR_API_ID']
    arr1 = json.loads(requests.get(temp1).content.decode())
    arr1 = arr1['user']
    temp = get_user_data(arr1, username)
    page_title = "Statistics"
    # url = "myapp/template/statistic.html"
    url = "hello/templates/statistic.html"
    return JsonResponse({'username': username, 'name': temp['name'],
                                 'title': page_title,
                                 'first_name': temp['first_name'],
                                 'last_name': temp['last_name'],
                                 'merchant_name': temp['merchant_name'],
                                 'profile_picture': temp['profile_picture'], 'ads': tmp}, status=200)

def verify_token(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        if token == '':
            return JsonResponse({ 'auth': False, 'message': 'No token provided.' }, status=500)
        else:
            try:
                payload = jwt.decode(token, os.environ["SECRET"], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                # Signature has expired
                return JsonResponse({ 'auth': False, 'message': 'Failed to authenticate token.' }, status=403)
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
            return JsonResponse({'auth': True, 'token': jwt.encode(payload, os.environ["SECRET"])
            .decode('UTF8'), 'email': payload['username']}, status=200)
    return JsonResponse({'auth': False, 'message': "Failed to Authenticate"}, status=500)
