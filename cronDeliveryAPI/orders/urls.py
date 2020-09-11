
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>', OrderSingleView.as_view()),
    path('order-repeat/', RepeatOrderView.as_view()),
    path('address/', AddressView.as_view()),
    path('profile/', UserProfileView.as_view())
]