from rest_framework import serializers
import datetime

class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    email = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    avatar = serializers.FileField(allow_null=True, allow_empty_file=True)

class ReadUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    email = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    avatar = serializers.FileField(allow_null=True, allow_empty_file=True)

class UpdatePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    new_password = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)

class UpdateAvatarUserSerializer(serializers.Serializer):
    avatar = serializers.FileField(allow_null=True, allow_empty_file=True)

class DeleteUserSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    password = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)

class CreateTransactionSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    price = serializers.IntegerField(default=0)
    date_time = serializers.DateTimeField(default=datetime.datetime.now)
    category = serializers.IntegerField(required=True, allow_null=False)
    wallet = serializers.IntegerField(required=True, allow_null=False)
    type = serializers.CharField(required=True, max_length=1, allow_null=False, allow_blank=False)

class UpdateTransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, allow_null=False)
    title = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    price = serializers.IntegerField(default=0)
    date_time = serializers.DateTimeField(default=datetime.datetime.now)
    category = serializers.IntegerField(required=True, allow_null=False)
    wallet = serializers.IntegerField(required=True, allow_null=False)
    type = serializers.CharField(required=True, max_length=1, allow_null=False, allow_blank=False)

class CreateCategorySerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)

class UpdateCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, allow_null=False)
    title = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)

class CreateWalletSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    stock = serializers.IntegerField(default=0)

class UpdateWalletSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True, allow_null=False)
    title = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    stock = serializers.IntegerField(default=0)