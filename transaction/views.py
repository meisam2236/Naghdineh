from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework import status
from .models import *

def stock_update(user):
    wallets = Wallet.objects.filter(user__exact=user)
    new_stock = 0
    for wallet in wallets:
        new_stock += wallet.stock
    user.stock = new_stock
    user.save()

class AddTransactionAPIView(APIView):
    def post(self, request):
        # authentication required!
        try:
            serializedData = serializers.AddTransactionSerializer(data=request.data)
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

class AddWalletAPIView(APIView):
    pass

class AddCategoryAPIView(APIView):
    pass