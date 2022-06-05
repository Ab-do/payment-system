from django.urls import path
from .views import *

app_name = 'payment'

urlpatterns = [
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transfer/<uuid:uid>', TransferDetailsView.as_view(), name='transfer-details'),
    path('ledger/', LedgerList.as_view(), name='ledgers'),
]
