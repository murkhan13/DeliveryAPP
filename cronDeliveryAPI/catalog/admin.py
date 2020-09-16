from django.contrib import admin
from .models import *


class DishAdditiveInline(admin.TabularInline):
    fk_name = 'dish'
    model = DishAdditive

class DishExtraInline(admin.TabularInline):
    fk_name = 'dish'
    model = DishExtra

class DishInline(admin.TabularInline):
    model = Dish.category.through


class CategoryAdmin(admin.ModelAdmin):
    fk = 'category'
    inlines =[
        DishInline,
    ]

"""class RestauranAdmin(admin.ModelAdmin):

    fields = (
        'title',
        'logo',
        'image',
        'workTime',
        'minOrder',
        'freeOrder',
        'address',
        'delivery',
        'maxDeliveryDist',
        'info',
        'rating'
    )"""
class RestaurantAdmin(admin.ModelAdmin):

    exclude = (
        'feedbacksAmount',
        'sumOfPoints',
        'likedUsers'
    )
    readonly_fields = (
        'rating',
    )

class DishAdmin(admin.ModelAdmin):
    inlines = [DishAdditiveInline, DishExtraInline]

    def save_model(self, request, obj, form, change):
        dish = super().save_model(request, obj, form, change)
        obj.save()
        categories = Category.objects.filter(dishes=dish)
        restaurant_menu = RestaurantMenu.objects.filter(categories__in=categories).first()
        obj.restaurant = str(restaurant_menu.restaurant.title)
        super().save_model(request, obj, form, change)


admin.site.register(Dish, DishAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Restaurant, RestaurantAdmin)


admin.site.register(RestaurantMenu)

admin.site.register(Offer)