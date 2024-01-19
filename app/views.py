from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def data_import(request):
    return render(request, "data-import.html")
