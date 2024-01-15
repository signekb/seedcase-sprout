from django.shortcuts import render
from datetime import datetime

def home(request):
    return render(request, "home.html")


def data_import(request):
    now = datetime.now()
    return render(request, "data-import.html")
