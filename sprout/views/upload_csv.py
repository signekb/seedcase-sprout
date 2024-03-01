"""Uploading CSV"""

from django.http import HttpResponse
from django.shortcuts import render


def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csvFile")

        # Process the CSV file as needed
        # For example, you can save it to the server, parse the data, etc.

        # In this example, let's just return a simple response
        return HttpResponse("CSV file uploaded successfully!")

    return render(request, "upload.html")
