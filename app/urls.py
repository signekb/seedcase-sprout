from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data-import', views.data_import, name='data_import')
]
