from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from accounts.models import User

from .models import *


class OrderFeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeedbackImage
        fields = (
            'image',
        )


class RestaurantFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantFeedback
        fields = (
            'id',
            'name',
            'overallPoint',
            'pros',
            'cons'
        )

class OrderFeedbackSerializer(serializers.ModelSerializer):
    images = OrderFeedbackImageSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = (
            'id',
            'name',
            'overallPoint',
            'pros',
            'cons',
        )