from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
# from rest_framework.exceptions import ParseError, KeyError
from django.shortcuts import get_object_or_404
from knox.auth import TokenAuthentication


import json

from cronProjectAPI.settings import ALLOWED_HOSTS
from .serializers import *
from .models import *
from catalog.models import Restaurant
from orders.models import Order
from catalog.serializers import RestaurantDetailSerializer
from orders.serializers import OrderSerializer

class OrderFeedbacksView(APIView):
    # parser_class = (FileUploadParser,)

    def get(self, request, id=None, *args, **kwargs):
        order = Order.objects.filter(pk=self.kwargs['order_id'])
        order_feedback = OrderFeedback.objects.filter(order=order, user=self.request.user)
        order_serializer = OrderSerializer(order, many=True, context={'request': request})
        feedback_serializer = OrderFeedbackSerializer(order_feedback, many=True, context={'request':request})
        return Response(order_serializer.data,feedback_serializer)

    def post(self, request, *args, **kwargs):
        #file_serializer = OrderFeedbackImageSerializer
        files = None
        if 'files' in request.data:
            try:
                order = Order.objects.filter(pk=self.kwargs['order_id'], user=self.request.user)
                files = request.FILES.getlist('files', None)
            except KeyError:
                raise ParseError('Файлы при запросе были переданы неправильно.')
        order_feedback = OrderFeedback(order=order, user=self.request.user)
        if order_feedback.exists():
            return Response({
                'status': False,
                'detail': 'Вы уже оставили отзыва на данный заказ.'
            })
        else:
            try:
                feedback = OrderFeedback.objects.create(
                    user=self.request.user,
                    order=Order.objects.get(pk=self.kwargs['order_id']),
                    name=request.data['name'],
                    overallPoint=request.data['overallPoint'],
                    pros=request.data['pros'],
                    cons=request.data['cons']
                )
                feedback.save()
                if files != None:
                    for img in files:
                        OrderFeedbackImage.objects.create(
                            feedback=feedback,
                            image=img
                        )
                    return Response({
                        'status': True,
                        'detail': 'Отзыв успешно добавлен. Оставайтесь с нами.'
                    })
                else:
                    return Response({
                        'status': True,
                        'detail': 'Отзыв успешно добавлен. Оставайтесь с нами.'
                    })
            except:
                return Response({
                        'status': False,
                        'detail': 'Возникла ошибка при создании отзыва.'
                })


    def delete(self, request, *args, **kwargs):
        try:
            feedback_qs = OrderFeedback.objects.filter(pk=request.data['feedback'])
            if feedback_qs.exists():
                feedback_qs.delete()
                return Response({
                    "status": True,
                    "detail": "Отзыв удалён"
                    })
            else:
                return Response({
                    "status": False,
                    "detail": "Отзыв не найден"
                })
        except:
            return Response({
                "status": False,
                "detail": "Ошибка при удалении отзыва"
            })


class RestaurantFeedbacksView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    """
    A class for representing and adding feedbacks to restaurant

    Args:
        APIView ([class]): [class from rest_framework]
    """

    def get(self, request, *args, **kwargs):
        restaurant_qs = Restaurant.objects.filter(pk=self.kwargs['restaurant_id'])
        restaurant = Restaurant.objects.filter(pk=self.kwargs['restaurant_id'])
        feedback = RestaurantFeedback.objects.filter(restaurant=restaurant)
        restaurant_serializer = RestaurantDetailSerializer(restaurant_qs, many=True, context={'request': request})
        feedback_serializer = RestaurantFeedbackSerializer(feedback, many=True, context = {'request': request})
        return Response({
            'restaurant':restaurant_serializer.data,
            'feedbacks':feedback_serializer.data
        })

    def post(self, request, *args, **kwargs):
        files = None
        try:
            restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
            files = request.FILES.getlist('files', None)
        except KeyError:
            raise ParseError('Файлы при запросе были переданы неправильно.')
        print(restaurant)
        restaurant_feedback = RestaurantFeedback.objects.filter(restaurant=restaurant, user=self.request.user)
        if restaurant_feedback.exists():
            return Response({
                'status': False,
                'detail': 'Вы уже оставили отзыва на данный ресторан.'
            })
        else:
            point = request.data['overallPoint']
            orders = Order.objects.filter(restaurant__icontains=restaurant.title, user=self.request.user)
            print(orders)
            if len(orders) > 0:
                try:
                    feedback = RestaurantFeedback.objects.create(
                        user=self.request.user,
                        restaurant=restaurant,
                        name=request.data['name'],
                        overallPoint=point,
                        pros=request.data['pros'],
                        cons=request.data['cons']
                    )
                    feedback.save()
                    if files != None:
                        for img in files:
                            RestaurantFeedbackImage.objects.create(
                                feedback=feedback,
                                image=img
                            )
                    restaurant.feedbacksAmount += 1
                    restaurant.sumOfPoints += point
                    restaurant.save()
                    if restaurant.feedbacksAmount > 0:
                        restaurant.rating = restaurant.sumOfPoints / restaurant.feedbacksAmount
                        restaurant.save()
                    return Response({
                        'status': True,
                        'detail': 'Отзыв успешно добавлен. Оставайтесь с нами.'
                    })
                except:
                    return Response({
                        'status': False,
                        'detail': 'Ошибка при добавление отзыва'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Для оставления отзыва нужно совершить хотя бы один заказ в данном ресторане'
                })


    def delete(self, request, *args, **kwargs):
        try:
            feedback_qs = RestaurantFeedback.objects.filter(pk=request.data['feedback'])
            if feedback_qs.exists():
                feedback_qs.delete()
                return Response({
                    "status": True,
                    "detail": "Отзыв удалён"
                    })
            else:
                return Response({
                    "status": False,
                    "detail": "Отзыв не найден"
                })
        except:
            return Response({
                "status": False,
                "detail": "Ошибка при удалении отзыва"
            })
