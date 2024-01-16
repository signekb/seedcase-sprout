from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello go to /hello to render a template")


def hello_world(request):
    now = datetime.now()
    return render(request, "hello.html", {"now": now})
