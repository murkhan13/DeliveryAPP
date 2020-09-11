from catalog.serializers import UserSerializer, CartDishSerializer
from catalog.models import CartItem
from catalog.serializers import CategoriesSerializer, DishAdditivesSerializer, DishExtrasSerializer

from orders.models import *
from rest_framework import serializers


class OrderDishSerializer(serializers.ModelSerializer):

    category = CategoriesSerializer(many=True, read_only=True)
    additives = DishAdditivesSerializer(many=True, read_only=True)
    extra = DishExtrasSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'title',
            'price',
            'image',
            'description',
            'portionWeight',
            'category',
            'additives',
            'extra',
        )

class OrderItemSerilalizer(serializers.ModelSerializer):

    order_dish = serializers.SerializerMethodField('get_order_dish')

    class Meta:
        model = CartItem
        fields = (
            'order_dish',
            'quantity'
        )

    def get_order_dish(self, obj):

        cartitem = CartItem.objects.filter(id=obj.id)

        return OrderDishSerializer(cartitem, many=True).data[0]


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'id',
            "street",
            "building",
            "porch",
            "floor",
            "apartment",
            "comment",
            "created_at"
        )

"""
class OrderItemSerializer(serializers.ModelSerializer):
    order_dish = CartItemToOrderSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'order_dish',
            'quantity',
        )"""


class OrderSerializer(serializers.ModelSerializer):

    order_items = OrderItemSerilalizer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'phone',
            'total',
            'personsAmount',
            'orderStatus',
            'paymentMode',
            'order_items',
            # 'restaurant',
            'address',
            'comment',
            'deliverTo',
            'created_at',
        )

    def create(self, validated_data):

        validated_data: dict

        order = Order.objects.create(**validated_data)
        return order


class UserProfileSerializer(serializers.ModelSerializer):
    adresses = AddressSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'adresses', 'orders')