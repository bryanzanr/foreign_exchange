from django.shortcuts import render


# Create your views here.
def hello(request):
    return render(request, "myapp/template/hello.html", {})


def broadcast(request):
    return render(request, "myapp/template/broadcast.html", {})
