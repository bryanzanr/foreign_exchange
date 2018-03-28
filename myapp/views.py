from django.shortcuts import redirect, render, render_to_response
from .forms import RegisterForm, LoginForm

import hashlib
import json
import os
import requests
# from django.core.context_processors import csrf

# Create your views here.


def hello(request):
    return render(request, "myapp/template/hello.html", {})


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


def header(request):
    return render(request, "myapp/template/header.html", {})


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


def footer(request):
    return render(request, "myapp/template/footer.html", {})

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
        arr = json.load(open('website/myapp/static/text/user.txt'))
        if email in arr['email']:
            temp = hashlib.sha1(password.encode('UTF8'))
            if temp.hexdigest() in arr['password']:
                request.session['email'] = email
                url = 'myapp/template/loggedin.html'
                return render_to_response(url, {'username': email})
    return redirect('login')


def registered(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        merchant_name = request.POST.get('merchant_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == repeat_password:
            password = hashlib.sha1(password.encode('UTF8'))
            password = password.hexdigest()
            arr = json.load(open('static/text/user.txt'))
            arr['email'].append(email)
            arr['password'].append(password)
            arr['first_name'].append(first_name)
            arr['last_name'].append(last_name)
            arr['merchant_name'].append(merchant_name)
            print(arr)
            location = 'static/text/user.txt'
            with open(location, 'w') as file:
                file.write(json.dumps(arr))
            user = {"user": arr}
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
        else:
            return redirect('register')
    url = 'myapp/template/loggedin.html'
    return render_to_response(url, {'username': request.session['email']})


def invalid_login(request):
    return render_to_response('invalid_login.html')


def logout(request):
    return render(request, "myapp/template/logout.html", {})
