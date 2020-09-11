
from __future__ import unicode_literals
import os
from django.db import models
from django.conf import settings

from django.utils import timezone

from accounts.models import User
from orders.models import Order
from PIL import Image


class Category(models.Model):
    # Model representing a dish category
    name    = models.CharField(("Название категории"),max_length=200, help_text='Введите категорию блюда(например, супы, салаты, пицца и т.д.')
    # image   = models.ImageField(("Картинка блюда"),upload_to="category_imgs", default = 'not_found.jpg')

    def __str__(self):
        # String for representing the Model object.
        return self.name

    def get_image_url(self, obj):
        return obj.image.url

    def get_category_name(self, obj):

        return obj.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Dish(models.Model):
    #Model representing a dish to order
    title           = models.CharField(("Навзание блюда"),max_length = 200, help_text='Назовите блюдо')
    price           = models.IntegerField(("Цена блюда"),help_text = 'Укажите цену')
    image           = models.ImageField(("Картинка блюда"),upload_to="dishes_imgs", default = 'not_found.jpg')
    description     = models.CharField(("Описание блюда"),max_length = 200, help_text = 'Опишите блюдо')
    portionWeight   = models.IntegerField(("Масса порции"),help_text = "укажите массу порции")
    category        = models.ManyToManyField(Category,
                                help_text="Удерживайте CTRL или COMMAND на Mac, чтобы выбрать больше чем одну категорию.",
                                related_name='dishes'
                    )

    class Meta:
        verbose_name_plural = "Блюда"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 600 or img.width > 600:
            output_size = (600, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_image_url(self, obj):
        return obj.image.url

    def __str__(self):
        # String for representing the Model object.
        return self.title

    def has_related_object(self):
        has_extra = False
        try:
            has_extra = (self.extra is not None)
        except DishExtra.DoesNotExist:
            pass
        return has_extra and (self.car is not None)


class DishAdditive(models.Model):
    dish        = models.ForeignKey(Dish, on_delete=models.CASCADE,related_name="additives", default='')
    name        = models.CharField(("Название добавки"),help_text="укажите название", max_length=200, default = "")
    addPrice    = models.IntegerField(("Цена"),help_text="укажите цену")
    active      = models.BooleanField(("Добавить"))

    class Meta:
         verbose_name_plural = "Добавки к блюду"

    def __str__(self):
        return self.name


class DishExtra(models.Model):
    dish    = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="extra", default='')
    name    = models.CharField(("Дополнительно"),help_text="укажите дополнительные продукты к блюду",  max_length=200)
    price   = models.IntegerField(("Цена"), help_text="укажите цену" )
    active  = models.BooleanField("Добавить")

    class Meta:
        verbose_name_plural = "Дополнительно к блюду"

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    """
    Model class that represent a restaurant model

    Args:
        models ([class]): [model class]

    Returns:
        [string]: [the title of restaurant and an image image.url]
    """
    title           = models.CharField(("Название ресторана"),max_length = 200)
    rating          = models.FloatField(("Рейтинг"),blank=True, null=True)
    logo            = models.ImageField(("Логотип Ресторана"),upload_to="logos", default = 'not_found.jpg')
    image           = models.ImageField(("Картинка ресторана"),upload_to="restaurant", default = 'not_found.jpg')
    workTime        = models.CharField(("График работы"),max_length = 200, help_text='укажите ')
    minOrder        = models.IntegerField(("Минимальный заказ"),help_text='Минимальный заказ')
    freeOrder       = models.IntegerField(("Бесплатная доставка с суммы заказа от:"))
    address         = models.CharField(("Адрес ресторана"),max_length = 200)
    delivery        = models.IntegerField(("Стоимость доставки"))
    deliveryTime    = models.IntegerField(("Среднее время доставки(мин)"), default=60)
    maxDeliverDist  = models.IntegerField(("Максимальное расстояние для доставки(km)"), default=20)
    info            = models.CharField(("Информация о ресторане"),max_length=200, help_text='Информация')
    # sumOfPoints sums everytime user give a feedback with point
    # and in the view the given sum is dividing by feedBacksAmount integer field
    # that also increasing everytime user gives a feedback
    feedbacksAmount = models.IntegerField(default=0)
    sumOfPoints     = models.IntegerField(default=0)


    # categories      = models.ManyToManyField(Category)
    # categories = models.(Category, related_name = 'categories', on_delete=models.SET_NULL, null = True)
    latitude        = models.FloatField(("Широта"), blank=True, null=True)
    longitude       = models.FloatField(("Долгота"), blank=True, null=True)
    likedUsers      = models.ManyToManyField(User, related_name="favoriteRestaurants")

    class Meta:
        verbose_name_plural = "Ресторан"

    def __str__(self):
        return self.title

    def get_image_url(self, obj):
        return obj.logo.url


class RestaurantMenu(models.Model):
    categories  = models.ManyToManyField(Category, related_name = 'restaurants')
    restaurant  = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null = True)

    class Meta:
        verbose_name_plural = "Меню Ресторанов"
        verbose_name = "Меню ресторана"

    def __str__(self):
        return self.restaurant.title


class Offer(models.Model):
    title       = models.CharField(("Название акции"),max_length=256)
    discount    = models.FloatField(("Процент скидки"), default=0.0)
    image       = models.ImageField(("Логотип Ресторана"),upload_to="offers", default = 'not_found.jpg')

    categories  = models.ManyToManyField(Category, help_text="Удерживайте CTRL или COMMAND на Mac, чтобы выбрать больше чем одну категорию.")

    class Meta:
        verbose_name_plural = "Акция"
        verbose_name = "Акции"

    def __str__(self):
        return "{0} -{1}%".format(self.title, str(self.discount) )


class Cart(models.Model):
    """
    Model class that represents a cart

    Args:
        models ([class]): [model class from django]
    """
    user = models.ForeignKey(
        User,
        related_name="cart",
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    device_token = models.CharField(max_length=256, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Корзина"


class CartItem(models.Model):
    """
    Model class that represents a cart item

    Args:
        models ([class]): [model class from django]

    Returns:
        [string]: [returns a strings of information about object]
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="items",
        verbose_name="Корзина"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name="Заказ"
    )
    dish_id         = models.IntegerField("ID блюда")
    title           = models.CharField(("Навзание блюда"),max_length = 200)
    price           = models.IntegerField(("Цена блюда"))
    image           = models.CharField(("Картинка Блюда"), max_length=400)
    description     = models.CharField(("Описание блюда"),max_length = 200)
    portionWeight   = models.IntegerField(("Масса порции"))
    category        = models.ManyToManyField(Category, verbose_name="Категории")
    additives       = models.ManyToManyField(DishAdditive, verbose_name="Добавки")
    extra           = models.ManyToManyField(DishExtra, verbose_name="Дополнительно")
    quantity        = models.PositiveIntegerField(default=1)
    created_at      = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    def __unicode__(self):
        return '%s: %s' %(self.title, self.quantity)
    class Meta:
        ordering = ['-created_at']