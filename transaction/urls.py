from . import views 
from django.urls import path 

urlpatterns = [
    path('api/add-transaction', views.AddTransactionAPIView.as_view(), name='add_transaction_api'),
]