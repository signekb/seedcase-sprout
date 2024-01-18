from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def data_import(request):
    return render(request, "data-import.html")


def create_new_table(request):

    return render(request, "create-new-table.html", {'table_name': 'Philip'})
