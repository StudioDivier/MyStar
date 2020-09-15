from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Users(AbstractUser, models.Model):
    """
    Родительский класс для всех пользователей
    :param: username - имя пользователя
    :param: phone - мобильный телефон пользователя
    :param: email - эл.адрес пользователя
    :param: password - пароль пользователя
    """
    username = models.CharField(name='username', max_length=128, db_index=True, unique=True)
    phone = models.IntegerField(name='phone', unique=True)
    email = models.EmailField(name='email', unique=True)
    password = models.CharField(name='password', max_length=128)

    def __str__(self):
        return self.username


class Customers(Users):
    """
    :param: date_of_birth дата рождения заказчика
    :param:
    """
    date_of_birth = models.DateField(name='date_of_birth', db_index=True)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Executor(Users):
    """
    :param:
    """
    pass
