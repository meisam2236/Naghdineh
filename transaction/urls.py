from . import views 
from django.urls import path 

urlpatterns = [
    path('api/create-user', views.CreateUserAPIView.as_view(), name='create_user_api'),
    path('api/delete-user', views.DeleteUserAPIView.as_view(), name='delete_user_api'),
    path('api/login-user', views.LoginUserAPIView.as_view(), name='login_user_api'),
    path('api/logout-user', views.LogoutUserAPIView.as_view(), name='logout_user_api'),
    path('api/create-transaction', views.CreateTransactionAPIView.as_view(), name='create_transaction_api'),
    path('api/read-transaction', views.ReadTransactionAPIView.as_view(), name='read_transaction_api'),
    path('api/update-transaction', views.UpdateTransactionAPIView.as_view(), name='update_transaction_api'),
    path('api/delete-transaction', views.DeleteTransactionAPIView.as_view(), name='delete_transaction_api'),
    path('api/create-category', views.CreateCategoryAPIView.as_view(), name='create_category_api'),
    path('api/read-category', views.ReadCategoryAPIView.as_view(), name='read_category_api'),
    path('api/update-category', views.UpdateCategoryAPIView.as_view(), name='update_category_api'),
    path('api/delete-category', views.DeleteCategoryAPIView.as_view(), name='delete_category_api'),
    path('api/create-wallet', views.CreateWalletAPIView.as_view(), name='create_wallet_api'),
    path('api/read-wallet', views.ReadWalletAPIView.as_view(), name='read_wallet_api'),
    path('api/update-wallet', views.UpdateWalletAPIView.as_view(), name='update_wallet_api'),
    path('api/delete-wallet', views.DeleteWalletAPIView.as_view(), name='delete_wallet_api'),
]