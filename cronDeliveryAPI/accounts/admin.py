
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *
User = get_user_model()

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminChangeForm, UserAdminCreationForm
from orders.models import Order, Address


# from .models import Profile, PhoneOTP

# class Profile(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'

class OrderInline(admin.TabularInline):
    fk_name = 'user'
    model = Order
    readonly_fields = ('user', 'phone', 'total', 'deliverTo', 'address', 'personsAmount', 'paymentMode', 'created_at')

class AddressInline(admin.TabularInline):
    fk_name = 'user'
    model = Address
    readonly_fields = ('user', 'street', 'building', 'porch', 'floor', 'apartment', 'comment', 'created_at')


class UserAdmin(BaseUserAdmin):
    # form = UserAdminChangeForm 
    add_form = UserAdminCreationForm

    # The fields to be use in displayin in the User model
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User
    inlines = [AddressInline, OrderInline]

    list_display = [  'phone', 'name','admin' ]
    list_filter = [ 'staff', 'active', 'admin',]
    fieldsets = (
        (None, {
            "fields": (
                'phone', 
            ),
        }),
        ('Personal info', {
            'fields': (
            'name',
        )}),
        # ('Permissions', {
        #     'fields': (
        #     'admin', 'staff', 'active'
        # )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to user attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2') # 
        }),
    )

    search_fields = ('phone',)
    ordering = ('phone','name')
    list_filter = ('phone', 'name')
    filter_horizontal = ()
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP)

# Removing Group Model from admin. We're not using it.
admin.site.unregister(Group)


