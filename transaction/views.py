from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework import status
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def stock_update(user):
    wallets = Wallet.objects.filter(user__exact=user)
    new_stock = 0
    for wallet in wallets:
        new_stock += wallet.stock
    user.stock = new_stock
    user.save()

# ---------------------------------------------------------------------------------------------------------------------------
# Create-Read-Update-Delete(CRUD) for Users(CustomUser)
class CreateUserAPIView(APIView):
    def post(self, request):
        try:
            serializedData = serializers.CreateUserSerializer(data=request.data)
            if serializedData.is_valid():
                username = serializedData.data.get('username')
                email = serializedData.data.get('email')
                password = serializedData.data.get('password')
                avatar = request.FILES['avatar'] if serializedData.data.get('avatar') else None
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username, email=email, password=password)
            custom_user = CustomUser()
            custom_user.user = user 
            custom_user.avatar = avatar
            custom_user.save()
            token = Token.objects.create(user=user)
            return Response({'status':'OK!', 'token': token.key}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReadUserAPIView(APIView):
    pass

class UpdateUserAPIView(APIView):
    pass 

class DeleteUserAPIView(APIView):
    pass 

# ---------------------------------------------------------------------------------------------------------------------------
# Login-Logout for Users(CustomUser)
class LoginUserAPIView(APIView):
    def post(self, request):
        try:
            serializedData = serializers.LoginUserSerializer(data=request.data)
            if serializedData.is_valid():
                username = serializedData.data.get('username')
                password = serializedData.data.get('password')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if user is not None:
                if Token.objects.filter(user=user) is not None:
                    Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                return Response({'status':'OK!', 'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'status':'User not found!'}, status=status.status_404_NOT_FOUND)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            Token.objects.filter(user=user).delete()
            return Response({'status':'OK!', 'token': token.key}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------------------------------------------------------------------------------------------------------------------------
# Create-Read-Update-Delete(CRUD) for Transaction
class CreateTransactionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializedData = serializers.CreateTransactionSerializer(data=request.data)
            if serializedData.is_valid():
                title = serializedData.data.get('title')
                price = serializedData.data.get('price')
                date_time = serializedData.data.get('date_time')
                category_id = serializedData.data.get('category')
                wallet_id = serializedData.data.get('wallet')
                user_id = serializedData.data.get('user')
                type = serializedData.data.get('type')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(id=user_id)
            custom_user = CustomUser.objects.get(user=user)
            category = Category.objects.get(id=category_id)
            wallet = Wallet.objects.get(id=wallet_id)
            transaction = Transaction()
            transaction.title = title
            transaction.price = price
            transaction.date_time = date_time
            transaction.user = custom_user
            transaction.category = category
            transaction.wallet = wallet
            transaction.type = type
            transaction.save()
            wallet_old_stock = wallet.stock
            wallet_new_stock = wallet_old_stock - price if type=='E' else wallet_old_stock + price
            wallet.stock = wallet_new_stock
            wallet.save()
            stock_update(custom_user)
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReadTransactionAPIView(APIView):
    pass

class UpdateTransactionAPIView(APIView):
    pass 

class DeleteTransactionAPIView(APIView):
    pass 

# ---------------------------------------------------------------------------------------------------------------------------
# Create-Read-Update-Delete(CRUD) for Category
class CreateCategoryAPIView(APIView):
    pass

class ReadCategoryAPIView(APIView):
    pass

class UpdateCategoryAPIView(APIView):
    pass 

class DeleteCategoryAPIView(APIView):
    pass 

# ---------------------------------------------------------------------------------------------------------------------------
# Create-Read-Update-Delete(CRUD) for Wallet
class CreateWalletAPIView(APIView):
    pass

class ReadWalletAPIView(APIView):
    pass

class UpdateWalletAPIView(APIView):
    pass 

class DeleteWalletAPIView(APIView):
    pass 
