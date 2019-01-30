from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^create_dataset$', views.create_dataset),
    re_path(r'^trainer$', views.trainer),
    re_path(r'^detect$', views.detect),
]
