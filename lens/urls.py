from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^create_dataset$', views.create_dataset),
]
