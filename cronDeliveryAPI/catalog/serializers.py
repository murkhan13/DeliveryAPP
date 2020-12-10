# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from accounts.models import User
from feedbacks.models import RestaurantFeedback
from feedbacks.serializers import RestaurantFeedbackSerializer

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            'id',
            'title',
            'price',
            'image',
            'description',
            'portionWeight',
            'category',
        )


class DishAdditivesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DishAdditive
        fields = ('id', 'name', 'addPrice', 'active')


class DishExtrasSerializer(serializers.ModelSerializer):

    class Meta:
        model = DishExtra
        fields = ('id', 'name', 'price', 'active')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'name'
        )


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id','name',)


class SearchingCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchingCategory
        fields = ('id', 'name', 'image')



class DishDetailSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=True, read_only=True)
    additives = DishAdditivesSerializer(many=True, read_only=True)
    extra = DishExtrasSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields =  ('id', 'title', 'image', 'price',  'portionWeight','description', 'category', 'restaurant', 'additives', 'extra')

    def get_image_url(self, obj):
        return obj.image.url


class CategoryItemsSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField('get_name')
    dishes = DishDetailSerializer(many=True, read_only = True)

    class Meta:
        model = Category
        fields =  ['id', 'name', 'dishes']

    def get_name(self, obj):
        index = obj.name.index('-')
        name = obj.name[:index-1]
        return name


class CategoryItemsSearchSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_name')
    dishes = DishDetailSerializer(source='filtered_dishes', many=True, read_only=True)

    class Meta:
        model = Category
        fields =  ['id', 'name', 'dishes']

    def get_name(self, obj):
        index = obj.name.index('-')
        name = obj.name[:index-1]
        return name


class RestaurantDetailSerializer(serializers.ModelSerializer):
    feedbacksAmount = serializers.SerializerMethodField('get_amount')
    rating = serializers.SerializerMethodField('int_rating')

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'title',
            'logo',
            'image',
            'worksFrom',
            'worksTo',
            'minOrder',
            'freeOrder',
            'address',
            'delivery',
            'deliveryTime',
            'maxDeliverDist',
            'info',
            'feedbacksAmount',
            'rating'
        )

    def get_amount(self, obj):
        amount = len(RestaurantFeedback.objects.filter(restaurant=obj))
        return amount
    def int_rating(self, obj):
        return None




"""
class RestaurantMenuSerializer(serializers.ModelSerializer):
    categories = CategoryItemsSerializer(many=True, read_only=True)
    restaurant = serializers.SerializerMethodField('get_restaurant')

    class Meta:
        model = Restaurant
        fields = (
            'categories',
            'restaurant'
        )

    def get_restaurant(self, obj):
        queryset = Restaurant.objects.filter(id=obj.id)

        return RestaurantDetailSerializer(queryset).data
"""


class RestaurantMenuSerializer(serializers.ModelSerializer):
    # categories = CategoryItemsSerializer(source='filtered_categories', many=True, read_only=True)

    categories = CategoryItemsSerializer(many=True, read_only=True)
    restaurant = RestaurantDetailSerializer(read_only=True)

    class Meta:
        model = RestaurantMenu
        fields = (
            'categories',
            'restaurant'
        )


class GlobalSearchSerializer(serializers.ModelSerializer):
    # categories = CategoryItemsSerializer(source='filtered_categories', many=True, read_only=True)

    # categories = CategoryItemsSearchSerializer(source='filtered_categories', many=True, read_only=True)
    restaurant = RestaurantDetailSerializer(read_only=True)

    class Meta:
        model = RestaurantMenu
        fields = (
            'categories',
            'restaurant'
        )


class UserFavoriteRestaurants(serializers.ModelSerializer):

    favoriteRestaurants = RestaurantDetailSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'favoriteRestaurants',
        )


class OfferSerializer(serializers.ModelSerializer):

    categories = CategoryItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = (
            'title',
            'discount',
            'image',
            'categories'
        )


class CartDishSerializer(serializers.ModelSerializer):
    category    = CategoriesSerializer(many=True, read_only=True)
    additives   = DishAdditivesSerializer(many=True,read_only=True)
    extra       = DishExtrasSerializer(many=True,read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id',
            'dish_id',
            'title',
            'price',
            'image',
            'description',
            'portionWeight',
            'category',
            'restaurant',
            'additives',
            'extra',
        )


class CartItemSerializer(serializers.ModelSerializer):

    dishDetail = serializers.SerializerMethodField('get_dish_details')

    class Meta:
        model = CartItem
        fields = (
            'dishDetail',
            'quantity'
        )

    def get_dish_details(self, obj):

        cartitem = CartItem.objects.filter(id=obj.id)

        return CartDishSerializer(cartitem, many=True).data

    '''def to_representation(self, instance):
        return {
            'dishDetail': {
                'id': instance.id,
                'title': instance.title,
                'price': instance.price,
                'image': instance.image.url,
                'description': instance.description,
                'portionWeight': instance.portionWeight,
                'category': instance.category,
                'additives': instance.additives,
                'extra': instance.extra
            },
            'quantity': instance.quantity
        }'''


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items')