from rest_framework import serializers
from .models import *

from rest_framework import serializers

class PointHistorySerializer(serializers.Serializer):
    action = serializers.CharField()
    point = serializers.IntegerField()
    isUsed = serializers.BooleanField(required=False)
    content = serializers.CharField(required=False)
    provider = serializers.CharField(required=False)
    getDate = serializers.DateField(required=False)
    useDate = serializers.DateField(required=False, allow_null=True)
