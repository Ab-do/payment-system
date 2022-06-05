from django.urls import path
from .views import BalanceView
from .views import *

urlpatterns = [
    path('balance/<uuid:uid>', BalanceView.as_view(), name='balance')
]
