from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Users(AbstractUser, models.Model):
    """
    Родительский класс для всех пользователей
     username - имя пользователя
     phone - мобильный телефон пользователя
     email - эл.адрес пользователя
     password - пароль пользователя
    """
    username = models.CharField(name='username', max_length=128, db_index=True, unique=True)
    phone = models.BigIntegerField(name='phone', unique=True)
    email = models.EmailField(name='email', unique=True)
    password = models.CharField(name='password', max_length=128)

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
        return self.cat_name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Rating(models.Model):
    """
    Модель рейтинга
     rate - рейтинг
    """
    rate = models.IntegerField(name='rate', db_index=True, default=5)

    def __str__(self):
        return str(self.rate)

    class Meta:
        verbose_name = 'rate'
        verbose_name_plural = 'rates'



class Stars(Users):
    """
    Модель для Исполнителей (звезд)
     price - цена звезды
     cat_name - отсылка к модели Катгории
     rate - отсылка к модели Рейтинга
    """
    price = models.DecimalField(name='price', max_digits=9, decimal_places=2)
    cat_name = models.ForeignKey(Categories, to_field='id', on_delete=models.CASCADE)
    rate = models.ForeignKey(Rating, to_field='id', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Star'
        verbose_name_plural = 'Stars'




