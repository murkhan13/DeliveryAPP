from django.contrib import admin
import nested_admin
# from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from .models import Order, Address
from catalog.models import CartItem, DishAdditive, DishExtra

class DishAdditiveInline(nested_admin.NestedTabularInline):
    fk_name = 'dish'
    model = DishAdditive

class DishExtraInline(nested_admin.NestedTabularInline):
    fk_name = 'dish'
    model = DishExtra

class CartItemInline(nested_admin.NestedStackedInline):
    fk = 'order'
    model = CartItem
    # extra = 0
    readonly_fields = (
        'title',
        'price',
        'description',
        'portionWeight',
        'image',
        'additives',
        'extra',
        'category',
        'cart',
        'order',
        'quantity',
        'dish_id',
        'created_at'
    )


"""
class OrderItemInline(nested_admin.SortableHiddenMixin,
                       nested_admin.NestedStackedInline):
    #
    model = OrderItem
    inlines = (CartItemInline,)
    # extra = 0
    list_display = [
                    'quantity' ,
                   ]
    readonly_fields = (
                        'order_dish',   
                        'quantity',
                      )"""


class OrderAdmin(nested_admin.NestedModelAdmin):
    
    
    inlines =[
        CartItemInline,
    ]
    # inlines = ['CartItem']
    list_display = [
        'user',
        'phone',
        'total',
        'deliverTo',
        'address',
        'personsAmount',
        'orderStatus',
        'created_at' 
    ]
    readonly_fields = [
        'user', 
        'phone', 
        'total', 
        'deliverTo',
        'address', 
        'personsAmount',
        # 'order_items',
        'paymentMode',
        'created_at'
    ]

admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)