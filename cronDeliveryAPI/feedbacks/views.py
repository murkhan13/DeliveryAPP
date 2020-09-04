
# Create your views here.


from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from django.db.models import Prefetch
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from itertools import chain
from django.db.models import Prefetch, Q, FilteredRelation
from cronProjectAPI.settings import ALLOWED_HOSTS

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.shortcuts import get_object_or_404
from catalog.models import Restaurant
from orders.models import Order

import json
from rest_framework import filters



class RestaurantFeedbacksView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    """
    A class for representing and adding feedbacks to restaurant

    Args:
        APIView ([class]): [class from rest_framework]
    """

    def get(self, request, *args, **kwargs):
        restaurant = Restaurant.objects.get(title=self.request.GET['restaurant'])
        feedbacks_qs = RestaurantFeedback.objects.filter(restaurant=restaurant)

        serializer = RestaurantFeedbackSerializer(feedbacks_qs, many=True, context = {"request": request})
        return Response(serializer.data)

    def post(self, request):
        try:
            restaurant  = Restaurant.objects.get(title=request.data['restaurant'])
            point       = int(request.data['point'])
            pros        = request.data['pros']
            cons        = request.data['cons']
        except:
            return Response({
                "status": False,
                "detail": "Ошибка при добавлении отзыва"
            })

        feedback = RestaurantFeedback.objects.create(
        user=self.request.user,
        restaurant=restaurant,
        name=self.request.user.name,
        overallPoint=point,
        pros=pros,
        cons=cons
        )
        feedback.save()
        restaurant.feedbacksAmount += 1
        restaurant.sumOfPoints += point
        restaurant.save()
        if restaurant.feedbacksAmount > 0:
            restaurant.rating = restaurant.sumOfPoints / restaurant.feedbacksAmount
            restaurant.save()
        print(self.request.user.name)
        return Response({
            "status": True,
            "detail": "Отзыв успешно добавлен"
        })
        """except:
            return Response({
                "status": False,
                "detail": "Ошибка при добавлении отзыва"
            })"""

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
