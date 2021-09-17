from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework import status
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_id = request.GET['id']
            user = User.objects.get(id=user_id)
            custom_user = CustomUser.objects.get(user=user)
            serializedData = serializers.ReadUserSerializer(custom_user, many=True)
            data = serializedData.data
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdatePasswordUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            username = Token.objects.get(key=token).user.username
            serializedData = serializers.CreateUserSerializer(data=request.data)
            if serializedData.is_valid():
                old_password = serializedData.data.get('old_password')
                new_password = serializedData.data.get('new_password')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=old_password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                return Response({'status': 'OK!'}, status=status.HTTP_200_OK)
            else:
                return Response({'status':'User not found!'}, status=status.status_404_NOT_FOUND)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class UpdateAvatarUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            serializedData = serializers.UpdateAvatarUserSerializer(data=request.data)
            if serializedData.is_valid():
                if serializedData.data.get('avatar'):
                    avatar = request.FILES['avatar']
                else:
                    return Response({'status':'No File Provided!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            custom_user.update(avatar=avatar)
            return Response({'status': 'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class DeleteUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            username = Token.objects.get(key=token).user.username
            serializedData = serializers.UpdateAvatarUserSerializer(data=request.data)
            if serializedData.is_valid():
                password = serializedData.data.get('password')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if user is not None:
                Token.objects.filter(user=user).delete()
                user.delete()
                return Response({'status':'OK!'}, status=status.HTTP_200_OK)
            else:
                return Response({'status':'User not found!'}, status=status.status_404_NOT_FOUND)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
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
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            transactions = Transaction.objects.filter(user=custom_user).order_by('-date_time')
            data = []
            for transaction in transactions:
                data.append({
                    'title': transaction.title,
                    'price': transaction.price,
                    'date_time': transaction.date_time, 
                    'category': transaction.category.title,
                    'wallet': transaction.wallet.title,
                    'type': transaction.type
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateTransactionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializedData = serializers.UpdateTransactionSerializer(data=request.data)
            if serializedData.is_valid():
                id = serializedData.data.get('id')
                title = serializedData.data.get('title')
                price = serializedData.data.get('price')
                date_time = serializedData.data.get('date_time')
                category_id = serializedData.data.get('category')
                wallet_id = serializedData.data.get('wallet')
                type = serializedData.data.get('type')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            category = Category.objects.get(id=category_id)
            wallet = Wallet.objects.get(id=wallet_id)
            transaction = Transaction.objects.filter(id=id)
            if transaction.user == custom_user:
                wallet_old_stock = wallet.stock
                wallet_old_stock_reversed = wallet_old_stock + transaction.price if transaction.type=='E' else wallet_old_stock - transaction.price
                transaction.update(title=title, price=price, date_time=date_time, category=category, wallet=wallet, type=type)
                wallet_new_stock = wallet_old_stock_reversed - price if type=='E' else wallet_old_stock_reversed + price
                wallet.stock = wallet_new_stock
                wallet.save()
                stock_update(custom_user)
                return Response({'status':'OK!'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'You Are Not Authorized!'}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class DeleteTransactionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            transaction_id = request.POST.get('transaction')
            transaction = Transaction.objects.filter(id=transaction_id)
            if transaction.user == custom_user:
                transaction.delete()
            else:
                return Response({'status': 'You Are Not Authorized!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------------------------------------------------------------------------------------------------------------------------
# Create-Read-Update-Delete(CRUD) for Category
class CreateCategoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializedData = serializers.CreateCategorySerializer(data=request.data)
            if serializedData.is_valid():
                title = serializedData.data.get('title')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            category = Category()
            category.title = title
            category.user = custom_user
            category.save()
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReadCategoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            categories = Category.objects.filter(user=custom_user)
            data = []
            for category in categories:
                data.append({
                    'title': category.title
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateCategoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializedData = serializers.UpdateCategorySerializer(data=request.data)
            if serializedData.is_valid():
                id = serializedData.data.get('id')
                title = serializedData.data.get('title')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            category = Category.objects.filter(id=id)
            if category.user == custom_user:
                category.update(title=title)
            else:
                return Response({'status': 'You Are Not Authorized!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class DeleteCategoryAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            category_id = request.POST.get('category')
            category = Category.objects.filter(id=category_id)
            if category.user == custom_user:
                category.delete()
            else:
                return Response({'status': 'You Are Not Authorized!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------------------------------------------------------------------------------------------------------------
# Create-Read-Update-Delete(CRUD) for Wallet
class CreateWalletAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializedData = serializers.CreateWalletSerializer(data=request.data)
            if serializedData.is_valid():
                title = serializedData.data.get('title')
                stock = serializedData.data.get('stock')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            wallet = Wallet()
            wallet.title = title
            wallet.stock = stock
            wallet.user = custom_user
            wallet.save()
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReadWalletAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            wallets = Wallet.objects.filter(user=custom_user)
            data = []
            for wallet in wallets:
                data.append({
                    'title': wallet.title,
                    'stock': wallet.stock
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateWalletAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializedData = serializers.UpdateWalletSerializer(data=request.data)
            if serializedData.is_valid():
                id = serializedData.data.get('id')
                title = serializedData.data.get('title')
                stock = serializedData.data.get('stock')
            else:
                return Response({'status':'Bad Request!'}, status=status.HTTP_400_BAD_REQUEST)
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            wallet = Wallet.objects.filter(id=id)
            if wallet.user == custom_user:
                wallet.update(title=title, stock=stock)
            else:
                return Response({'status': 'You Are Not Authorized!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteWalletAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            user = Token.objects.get(key=token).user
            custom_user = CustomUser.objects.get(user=user)
            wallet_id = request.POST.get('wallet')
            wallet = Wallet.objects.filter(id=wallet_id)
            if wallet.user == custom_user:
                wallet.delete()
            else:
                return Response({'status': 'You Are Not Authorized!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'status':'OK!'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'Internal Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
