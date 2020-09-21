from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from MyStar import config

class Users(AbstractUser, models.Model):
    """
    Родительский класс для всех пользователей
     username - имя пользователя
     phone - мобильный телефон пользователя
     email - эл.адрес пользователя
     password - пароль пользователя
     avatar - аватар пользователя
     is_star - флаг для чека звезды (0,1)
    """
    username = models.CharField(name='username', max_length=128, db_index=True, unique=True)
    phone = models.BigIntegerField(name='phone', unique=True)
    email = models.EmailField(name='email', unique=True)
    password = models.CharField(name='password', max_length=128)
    avatar = models.FilePathField(name='avatar', path=settings.AVATAR_ROOT, default='/1.jpg')
    is_star = models.BooleanField(name='is_star', default=0)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'BaseUser'
        verbose_name_plural = 'BaseUsers'


class Customers(Users):
    """
    Модель для заказчиков
     date_of_birth - дата рождения заказчика

    """
    date_of_birth = models.DateField(name='date_of_birth')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Categories(models.Model):
    """
    Модель категорий
     cat_name - наименование категории
    """
    cat_name = models.CharField(name='cat_name', unique=True, db_index=True, max_length=128)

    def __str__(self):
        return "{}".format(self.cat_name)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Ratings(models.Model):
    """
    Модель рейтинга
     rate - рейтинг
     adresat - От кого (заказчик)
     adresant - Кому (Звезда)
    """
    rating = models.IntegerField(name='rating')
    adresat = models.ForeignKey(Customers, name='adresat', on_delete=models.CASCADE)
    adresant = models.IntegerField(name='adresant', default=None)

    def __str__(self):
        return "{}".format(self.rating)

    class Meta:
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'


class Stars(Users):
    """
    Модель для Исполнителей (звезд)
     price - цена звезды
     cat_name_id - id Катгории
     rating - отсылка к модели Рейтинга
     video_hi - видео приветствие от звезды
    """
    price = models.DecimalField(name='price', max_digits=9, decimal_places=2)
    cat_name_id = models.ForeignKey(Categories, to_field='id', on_delete=models.CASCADE)
    rating = models.IntegerField(name='rating')
    video_hi = models.FilePathField(name='video_hi', path=settings.VIDEO_ROOT, default='/1.jpg')

    class Meta:
        verbose_name = 'Star'
        verbose_name_plural = 'Stars'


class Orders(models.Model):
    """
    Модель для Заказов
      customer_id - id заказчика
      star_id - id звезды
      order_price - цена заказа
      ordering_time - время заказа
      for_whom - для кого
      comment - колмментарий к заказы
      status_order - статус заказа (0 - New, 1 - Accepted, 2 - Completed)
    """
    ORDER_STATUS = (
        ('New', 'Новый заказ'),
        ('Accepted', 'Заказ принят'),
        ('Completed', 'Заказ завершен')
    )

    customer_id = models.ForeignKey(Customers, name='customer_id', on_delete=models.CASCADE)
    star_id = models.ForeignKey(Stars, name='star_id', on_delete=models.CASCADE)
    order_price = models.DecimalField(name='order_price', max_digits=9, decimal_places=2)
    ordering_time = models.DateTimeField(name='ordering_time', default=timezone.now)
    for_whom = models.CharField(name='for_whom', max_length=128)
    comment = models.TextField(name='comment')
    status_order = models.IntegerField(name='status_order', default=0)


    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "http://127.0.0.1:8000{}confirm/?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )



