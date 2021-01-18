from django.db import models
from catalog.models import Restaurant
from orders.models import Order
from accounts.models import User
from django.utils import timezone
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True




class RestaurantFeedback(models.Model):
    IS_EDITED = (
        (u'N', u'Не отредактирован'),
        (u'Y', u'Отредактирован'),
    )
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
    editing         = models.CharField(('Статус редактирования'),max_length=100, choices=IS_EDITED, default='N')
    name            = models.CharField(('Имя'), max_length=200)
    overallPoint    = models.IntegerField(verbose_name="Общее впечателение о ресторане")
    pros            = models.CharField(max_length=255, verbose_name='Плюсы', default='нет')
    cons            = models.CharField(max_length=255, verbose_name='Минусы', default='нет')
    created_at      = models.DateTimeField(("Отзыв добавлен создан"),  default=timezone.now())

    class Meta:
        verbose_name_plural = "Отзывы к ресторанам"

    def __str__(self):
        return '%s отставил отзыв к %s' %(self.name, self.restaurant)

class OrderFeedback(models.Model):

    user                = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        related_name='orderFeedbacks',
        default=None,
        verbose_name='Пользователь'
    )
    order               = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        blank=True,
        null=True
    )
    name                = models.CharField(('Имя'), max_length=200)
    overallPoint        = models.IntegerField(verbose_name="Оценка заказа")
    pros                = models.CharField(max_length=255, verbose_name='Плюсы', default='нет')
    cons                = models.CharField(max_length=255, verbose_name='Минусы', default='нет')
    created_at      = models.DateTimeField(("Заказ создан"),default=timezone.now())
    class Meta:
        verbose_name_plural = "Отзывы к заказам"

    def __str__(self):
        return '%s отставил отзыв к %s' %(self.name, self.order)


class RestaurantFeedbackImage(models.Model):
    feedback    = models.ForeignKey(
        RestaurantFeedback,
        on_delete=models.CASCADE,
        related_name='images',
        blank=True,
        null=True
    )
    image       = models.ImageField(("Картинка отзыва"),upload_to="feedbacks", default = 'not_found.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)

        if image.height > 1024 or image.width > 1024:
            output_size = (1024, 1024)
            image.thumbnail(output_size)
            image.save(self.image.path)

class OrderFeedbackImage(models.Model):
    feedback    = models.ForeignKey(
        OrderFeedback,
        on_delete=models.CASCADE,
        related_name='images',
        blank=True,
        null=True
    )
    image       = models.FileField(("Картинка ресторана"),upload_to="feedbacks", default = 'not_found.jpg')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)

        if image.height > 1024 or image.width > 1024:
            output_size = (1024, 1024)
            image.thumbnail(output_size)
            image.save(self.image.path)
