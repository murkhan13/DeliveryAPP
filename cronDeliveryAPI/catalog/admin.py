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

class CategoryInline(admin.TabularInline):
    model = RestaurantMenu.categories.through


class RestaurantMenuAdmin(admin.ModelAdmin):
    exclude = ( 'categories', )
    inlines = (CategoryInline,)

    def save_model(self, request, obj, form , change):
        for category in obj.categories.all():
            if obj.restaurant.title not in category.name:
                category.name = '{0} - {1}'.format(category.name, obj.restaurant.title)
                category.save()
            else:
                pass


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
    '''
    def save_model(self, request, obj, form, change):
        dish = super().save_model(request, obj, form, change)
        obj.save()
        print(dish)
        category = Category.objects.filter(dishes=dish)
        print(category)
        restaurant_menu = RestaurantMenu.objects.filter(categories__in=category).first()
        print(restaurant_menu)
        obj.restaurant = str(restaurant_menu.restaurant.title)
        super().save_model(request, obj, form, change)'''


admin.site.register(Dish, DishAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(SearchingCategory)
admin.site.register(Restaurant, RestaurantAdmin)


admin.site.register(RestaurantMenu, RestaurantMenuAdmin)

admin.site.register(Offer)