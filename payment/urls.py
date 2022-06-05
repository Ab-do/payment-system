from django.urls import path
from .views import *

urlpatterns = [
    path('transfer/', TransferView.as_view(), name='transfer'),
]
