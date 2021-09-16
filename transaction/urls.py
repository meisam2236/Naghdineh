from . import views 
from django.urls import path 

urlpatterns = [
    path('api/create-user', views.CreateUserAPIView.as_view(), name='create_user_api'),
    path('api/login-user', views.LoginUserAPIView.as_view(), name='login_user_api'),
    path('api/logout-user', views.LogoutUserAPIView.as_view(), name='logout_user_api'),
    path('api/create-transaction', views.CreateTransactionAPIView.as_view(), name='create_transaction_api'),
]