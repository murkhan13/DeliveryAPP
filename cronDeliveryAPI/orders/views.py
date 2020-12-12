from __future__ import unicode_literals

import os
import requests

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django.shortcuts import render
from django.db.models import FloatField, F, Sum
from cronProjectAPI.settings import TG_BOT_TOKEN

from knox.auth import TokenAuthentication

from catalog.models import Cart, CartItem
from .models import *
from .serializers import *

TELEGRAM_URL = "https://api.telegram.org/bot"
# TELEGRAM_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "error_token")



class OrderView(APIView):
    """
    Class Based View that making actions like adding and parsing existing orders by user token

    Args:
        APIView ([class]): [class from rest framework views]

    Raises:
        serializers.ValidationError: [the error that appears when theres's no way to get a user and get a cart of ther user]

    Returns:
        [json object]: [ json object of order model]
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=self.request.user)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


    def post(self, request, pk=None):
        try:
            cart        = Cart.objects.get(user=self.request.user)
        except :
            raise serializers.ValidationError(
                'Пользователь не найден')
        if 'deliverTo' in request.data:
            deliverTo   = request.data['deliverTo']
        else:
            deliverTo   = 'Как можно быстрее'
        if 'restaurant' in request.data:
            restaurant  = request.data['restaurant']
        else:
            restaurant  = None
        phone           =request.data['phone']
        total           =request.data['total']
        address         = request.data['address']
        comment         = request.data['comment']
        personsAmount   =request.data['personsAmount']
        paymentMode     =request.data['paymentMode']
        order = Order(
            user=self.request.user,
            phone=phone,
            total=total,
            deliverTo=deliverTo,
            restaurant=restaurant,
            address = address,
            comment = comment,
            personsAmount=request.data['personsAmount'],
            paymentMode=request.data['paymentMode']
            )
        order.save()
        url = '{0}{1}/sendMessage'.format(TELEGRAM_URL, TG_BOT_TOKEN)
        text ='Новый заказ: \n'

        for cart_item in cart.items.all():
            cart_item.order = order
            # cart_item.cart = None
            text += str(cart_item.title) + '\nКоличество: ' + str(cart_item.quantity)
            if len(cart_item.additives.all()) > 0:
                text += '\n Добавка: '
                for add in cart_item.additives.all():
                    text += add.name
            if len(cart_item.extra.all()) > 0:
                text += '\n Дополнительно: '
                for ext in cart_item.extra.all():
                    text += ext.name
            cart_item.save()
        text += '\nАдрес доставки: {0}\nКомментарий: {1}'.format(address, comment)
        text += '\nРесторан: {0}\nКоличество персон: {1}\nCпособ оплаты: {2},\nдоставить к: {3}'.format(restaurant, personsAmount, paymentMode, deliverTo)
        text += '\nТелефон: {0}\nИтог: {1}руб.\n'.format(phone, total)
        print(url)
        print(text)
        data = {"chat_id": '-463655212',  "text": text}
        requests.post(url, data)

        """
        order_items = []

        for cart_item in cart.items.all():
            order_items.append(OrderItem(order=order, order_dish=cart_item, quantity=cart_item.quantity,))

        OrderItem.objects.bulk_create(order_items)"""

        cart.items.clear()

        user_order = Order.objects.filter(id=order.id)

        serializer = OrderSerializer(user_order, many=True)

        return Response(serializer.data)


class RepeatOrderView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request,*args,**kwargs):
        try:
            order = Order.objects.get(pk=request.data['order_id'], user=self.request.user)
            cart = Cart.objects.get(user=self.request.user)
        except Order.DoesNotExist:
            return Response({
                "status": False,
                "detail": "Такого заказа не существует"
            })
        # repeated_order = Order.objects.create(
        #     user=self.request.user,
        #     phone=order.phone,
        #     total=order.total,
        #     deliverTo=order.deliverTo,
        #     address = order.address,
        #     comment = order.comment,
        #     personsAmount=order.personsAmount,
        #     paymentMode=order.paymentMode
        # )
        try:
            cart.items.clear()
            for item in order.order_items.all():
                item.pk = None
                item.save()
                item.order=None
                item.cart = cart
                item.save()
            return Response({
                'status': True,
                'detail': 'Все позиции из данного заказа добавлены в корзину'
            })
        except:
            return Response({
                'status': False,
                'detail': 'Ошибка при повторении заказа.'
            })


class OrderSingleView(RetrieveAPIView):
    """
    Class Based View to represent a single order by passing primary key of the order to url .../orders/<int:pk>

    Args:
        RetrieveAPIView ([class]): [class from rest framework for get a single model object]
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class AddressView(APIView):
    """
    The Class Based View that handles actions like add addresses and GET existed addresses of the user using user token

    Args:
        APIView ([class]): [class from rest framework]

    Returns:
        [json object]: [json object of model address]
    """

    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk=None):

        try:
            user_addresses = Address.objects.filter(user=self.request.user)

            serializer = AddressSerializer(user_addresses, many=True)
            return Response(serializer.data)
        except:
            return Response({
                "status": False
            })

    def post(self, request, pk=None):

        try:
            street = request.data['street']
            building = request.data['building']
        except:
            return Response({
                "status": False
            })
        if 'porch' in request.data:
            porch = request.data['porch']
        else:
            porch = None
        if 'floor' in request.data:
            floor = request.data['floor']
        else:
            floor = None
        if 'apartment' in request.data:
            apartment = request.data['apartment']
        else:
            apartment = None
        if 'comment' in request.data:
            comment = request.data['comment']
        else:
            comment = None

        try:
            new_address = Address.objects.create(
                user=self.request.user,
                street=street,
                building=building,
                porch=porch,
                floor=floor,
                apartment=apartment,
                comment=comment
            )
            new_address.save()
            return Response({
                "status": True
            })
        except:
            return Response({
                "status": False
            })

    def delete(self, request, *args, **kwargs):
        try:
            address_id = self.request.GET['address_id']
        except:
            return Response({
                "status": False,
                "detail": "Ошибка при удалении адреса."
            })
        try:
            Address.objects.filter(id=address_id,user=self.request.user).delete()
            return Response({
                "status": True,
                "detail": "Адрес удалён."
            })
        except:
            return Response({
                "status": False,
                "detail": "Адрес не найден"
            })

class UserProfileView(APIView):
    """
    Class Base View to represent a user information like orders, addresses, phone etc.

    Args:
        APIView ([class]): [class from rest framework]

    Returns:
        [json object]: [json object of user model]
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk=None):
        user = self.request.user

        user_queryset = User.objects.filter(pk=user.id)

        serializer = UserProfileSerializer(user_queryset, many=True)

        return Response(serializer.data)
