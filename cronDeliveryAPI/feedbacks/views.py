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

class OrderFeedbacksView(APIView):
    # parser_class = (FileUploadParser,)

    def get(self, request, id=None, *args, **kwargs):
        order = Order.objects.filter(pk=self.kwargs['order_id'])
        order_feedback = OrderFeedback.objects.filter(order=order, user=self.request.user)
        serializer = OrderFeedbackSerializer(order_feedback, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        #file_serializer = OrderFeedbackImageSerializer
        files = None
        if 'files' in request.data:
            try:
                files = request.FILES.getlist('files', None)
            except KeyError:
                raise ParseError('Файлы при запросе были переданы неправильно.')
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


    def delete(self, request):
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
        restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        feedbacks_qs = RestaurantFeedback.objects.filter(restaurant=restaurant, user=self.request.user)

        serializer = RestaurantFeedbackSerializer(feedbacks_qs, many=True, context = {"request": request})
        return Response(serializer.data)

    def post(self, request):
        files = None
        if 'files' in request.data:
            try:
                files = request.FILES.getlist('files', None)
            except KeyError:
                raise ParseError('Файлы при запросе были переданы неправильно.')
        restaurant = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        point = request.data['overallPoint']
        orders = Order.objects.filter(restaurant__icontains=restaurant.title, user=user)
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


    def delete(self, request):
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
