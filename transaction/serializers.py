from rest_framework import serializers
import datetime

from rest_framework.views import set_rollback

class AddTransactionSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=128, allow_null=False, allow_blank=False)
    price = serializers.IntegerField(default=0)
    date_time = serializers.DateTimeField(default=datetime.datetime.now)
    category = serializers.IntegerField(required=True, allow_null=False)
    wallet = serializers.IntegerField(required=True, allow_null=False)
    user = serializers.IntegerField(required=True, allow_null=False)
    type = serializers.CharField(required=True, max_length=1, allow_null=False, allow_blank=False)