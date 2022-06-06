from django.urls import path
from .views import BalanceView, AccountsList

app_name = 'account'

urlpatterns = [
    path('list/', AccountsList.as_view(), name='accounts-list'),
    path('balance/<uuid:uid>', BalanceView.as_view(), name='balance')
]
