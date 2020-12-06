from django.contrib import admin

from .models import *
from catalog.models import Restaurant


class RestaurantFeedbackImagesInline(admin.TabularInline):
    fk_name='feedback'
    model = RestaurantFeedbackImage


class RestaurantFeedbackAdmin(admin.ModelAdmin):
    inlines = [
        RestaurantFeedbackImagesInline,
    ]
    def delete_model(self, request, obj):
        print('obj -',obj)
        restaurant = obj.restaurant
        restaurant.feedbacksAmount -= 1
        restaurant.save_model()
        print(restaurant.feedbacksAmount)
        restaurant.save()
        print(restaurant.feedbacksAmount)
        super().delete_model(self, request, obj)



admin.site.register(RestaurantFeedback, RestaurantFeedbackAdmin)
admin.site.register(OrderFeedback)
