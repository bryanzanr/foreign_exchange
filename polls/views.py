# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import hashlib
import json
import os
import requests

from myapp import email as eb

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
                    payload['url'] = '/myapp/broadcast/'
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
    return JsonResponse("Failed to Login", status=404)

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
            payload['url'] = '/myapp/broadcast/'
            payload['title'] = 'Broadcast'
            payload['name'] = first_name + ' ' + last_name
            payload['username'] = email
            payload['merchant_name'] = merchant_name
            payload['profile_picture'] = profile_picture
            return JsonResponse({'code': 200,'message': "User registered successfully", 
            'token': jwt.encode(payload, os.environ["SECRET"]).decode('UTF8')})
    return JsonResponse("Failed to Register", status=500)

def logout(request):
    # del request.session['email']
    # return render(request, "myapp/template/logout.html", {})
    tmp = {}
    tmp['auth'] = False
    tmp['token'] = None
    return JsonResponse(tmp, status=200)

def verify_token(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        if token is None:
            return JsonResponse({ auth: False, message: 'No token provided.' }, status=500)
        else:
            try:
                payload = jwt.decode(token, os.environ["SECRET"], algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                # Signature has expired
                return JsonResponse({ auth: False, message: 'Failed to authenticate token.' }, status=403)
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
            return JsonResponse({'auth': True, 'token': jwt.encode(payload, os.environ["SECRET"])
            .decode('UTF8')}, status=200)
