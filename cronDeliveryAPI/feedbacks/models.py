from django.db import models
from catalog.models import Restaurant
from orders.models import Order
from accounts.models import User

# Create your models here.

class RestaurantFeedback(models.Model):

    user            = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        related_name='restaurantFeedbacks',
        default=None,
        verbose_name = 'Пользователь'
    )
    restaurant      = models.ForeignKey(
        Restaurant,
        on_delete = models.CASCADE,
        related_name = 'feedbacks',
        blank=True,
        null=True
    )
    name            = models.CharField(('Имя'), max_length=200)
    overallPoint    = models.IntegerField(verbose_name="Общее впечателение о ресторане")
    pros            = models.CharField(max_length=255, verbose_name='Плюсы', default='нет')
    cons            = models.CharField(max_length=255, verbose_name='Минусы', default='нет')

class OrderFeedback(models.Model):

    user            = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        related_name='orderFeedbacks',
        default=None,
        verbose_name = 'Пользователь'
    )
    order           = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        blank=True,
        null=True
    )
    name            = models.CharField(('Имя'), max_length=200)
    overallPoint    = models.IntegerField(verbose_name="Оценка заказа")
    pros            = models.CharField(max_length=255, verbose_name='Плюсы', default='нет')
    cons            =    models.CharField(max_length=255, verbose_name='Минусы', default='нет')


class RestaurantFeedbackImage(models.Model):
    feedback    = models.ForeignKey(
        RestaurantFeedback,
        on_delete=models.CASCADE,
        related_name='images',
        blank=True,
        null=True
    )
    image       = models.ImageField(("Картинка отзыва"),upload_to="feedbacks", default = 'not_found.jpg')

class OrderFeedbackImage(models.Model):
    feedback    = models.ForeignKey(
        OrderFeedback,
        on_delete=models.CASCADE,
        related_name='images',
        blank=True,
        null=True
    )
    image       = models.ImageField(("Картинка ресторана"),upload_to="feedbacks", default = 'not_found.jpg')
