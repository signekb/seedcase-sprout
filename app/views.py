from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def data_import(request):
    print(request.method)
    return render(request, "data-import.html")

