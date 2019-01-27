from django.urls import re_path, path
from .views import ImageView

urlpatterns = [
    re_path(r'upload', ImageView.as_view(), name='file-upload'),
]