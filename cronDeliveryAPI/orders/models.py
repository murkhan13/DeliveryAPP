from django.db import models
from django.contrib.auth import get_user_model
# from catalog.models import CartItem
from django.core.validators import RegexValidator

User = get_user_model()


class Address(models.Model):
    """
    The model class that represent an user addresses

    Args:
        models ([class]): [description]
    """
    user            = models.ForeignKey(
                        User,
                        related_name='adresses',
                        on_delete=models.CASCADE,
                        null=True,
                        blank=True,
    )
    street          = models.CharField(("Улица"),max_length=255)
    building        = models.CharField(("Дом"), max_length=255)
    porch           = models.CharField(("Подъезд"), max_length=255, blank=True,null=True)
    floor           = models.CharField(("Этаж"), max_length=255, blank=True, null=True)
    apartment       = models.CharField(("Квартира"), max_length=255, blank=True, null=True)
    comment         = models.CharField(("Комментарий"),max_length=255, blank=True, null=True)
    created_at      = models.DateTimeField(("Дата создания"), auto_now_add=True)

    class Meta:
        verbose_name_plural = "Адрес"

class Order(models.Model):
    """
    The model class that represents an order

    Args:
        models ([class]): [description]

    Returns:
        [string]: [the string of user and date of creation]
    """

    PAYMENT_CHOICES = (
        (u'H', u'Наличными курьеру'),
        (u'K', u'Оплата картой курьеру'),
        (u'G', u'Оплатить с помощью Google Pay'),
        (u'A', u'Оплатить с помощью Apple Pay')
    )
    ORDER_STATUSES = (
        (u'N', u'Новый'),
        (u'P', u'В Пути'),
        (u'D', u'Доставлен'),
    )

    user            = models.ForeignKey(
                        User,
                        related_name='orders',
                        on_delete=models.CASCADE,
                        verbose_name='Пользователь',
                        null=True,
                        blank=True
    )
    orderStatus     = models.CharField(("Статус Заказа"), max_length=100, choices=ORDER_STATUSES, default='N')
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{11,25}$',
                        message="Номер телефона должен быть в формате: '+999999999'.Разрешено до 20 символов.")
    phone           = models.CharField(("Номер телефона"), validators = [phone_regex], max_length=25)
    total           = models.DecimalField(("Итоговая сумма"), max_digits=8, decimal_places=2, null=True, blank=True)
    deliverTo       = models.CharField(("Доставить к"), max_length=255)

    # order_items     = models.ManyToManyField(CartItem, verbose_name="Заказанные блюда")
    restaurant      = models.CharField(max_length=200, verbose_name="Ресторан", default="нет")
    address         = models.CharField(("Адрес"), max_length=255)

    comment         = models.CharField(("Комментарий"), max_length=255, null=True, blank=True)

    personsAmount   = models.IntegerField(("Количество персон"), default=1)

    paymentMode     = models.CharField(("Способ оплаты"), max_length=100, default='Наличными курьеру')

    created_at      = models.DateTimeField(("Заказ создан"),auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return "%s заказал %s" %(self.user, self.created_at)

"""
class OrderItem(models.Model):
    A model that contains data for an item in an order.
    order           = models.ForeignKey(
                        Order,
                        related_name='order_items',
                        on_delete=models.CASCADE
                )
    order_dish      = models.ForeignKey(
                        CartItem,
                        on_delete=models.CASCADE,
                        verbose_name="Блюда",
                        null=True,
                        blank=True,
                )
    quantity        = models.PositiveIntegerField(("Количество"),null=True, blank=True)


    class Meta:
        verbose_name = "Заказанное блюдо"
        verbose_name_plural = "Заказанные блюда"

    def __str__(self):
        return ''#"%s : %s" % (self.order_dish.title, self.quantity)

    def __unicode__(self):
        return '%s: %s' % (self.order_dish.title, self.quantity)"""