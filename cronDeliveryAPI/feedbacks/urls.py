from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('feedback-restaurant/<int:restaurant_id>', RestaurantFeedbacksView.as_view()),
    path('feedback-order/<int:order_id>', OrderFeedbacksView.as_view())
]