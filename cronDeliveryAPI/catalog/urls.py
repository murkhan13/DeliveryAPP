
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('dishes/<int:pk>', DishDetailView.as_view()),
    path('find-in-restaurant/', SearchInRestaurantView.as_view()),
    path('restaurants/', RestaurantView.as_view()),
    path('find-all/', GlobalSearchView.as_view()),
    # path('restaurants/<int:pk>', RestaurantMenuView.as_view()),
    path('restaurants/menu/', RestaurantMenuView.as_view()),
    path('favorite-restaurants/', FavoriteRestaurantsView.as_view() ),
    path('menu/', MenuPageView.as_view()),
    path('cart/add/', CartItemAddView.as_view()),
    path('cart/edit/', CartItemEditView.as_view()),
    path('cart/delete/', CartItemDeleteView.as_view()),
    path('cart/deleteall/', CartDeleteView.as_view())
]