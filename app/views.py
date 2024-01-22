from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def data_import(request):
    return render(request, "data-import.html")

class FileUploadVariables:
    upload_error = ''
    table_name = 'NoTableSelected'

def file_upload(request):
    file_upload_data = {'table_name': 'Philip', 'upload_error': ''}
    if request.method == 'GET':
        return render(request, "file-upload.html", file_upload_data)

    # File is missing
    if 'uploaded_file' not in request.FILES:
        file_upload_data["upload_error"] = "Missing"
        return render(request, "file-upload.html", file_upload_data)

    uploaded_file = request.FILES['uploaded_file']

    print("CSV headers", uploaded_file.readline())
    return render(request, "file-upload.html", file_upload_data)

