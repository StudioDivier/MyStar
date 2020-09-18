from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Customers, Stars, Users, Ratings, Orders


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Users.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'phone', 'email', 'password')


class CustomerSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки даных Заказчиков
    Добавлены валидоры на создание и обновление основных полей при регистрации
    Переопределен меотод create
    """
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Users.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Customers
        fields = ('username', 'phone', 'email', 'password', 'date_of_birth')

    def create(self, validated_data):
        customer = Customers(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            date_of_birth=validated_data['date_of_birth']
        )
        customer.set_password(validated_data['password'])
        customer.save()
        return customer


class StarSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки данных звезд
    Добавлены валидоры на создание и обновление основных полей при регистрации
    Переопределены методы create и update
    """

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Stars.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Stars.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Stars.objects.all())]
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True
    )

    price = serializers.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    rating = serializers.IntegerField()

    class Meta:
        model = Stars
        fields = ('username', 'password', 'phone', 'email', 'price', 'cat_name_id', 'rating', 'is_star')

    def create(self, validated_data):
        star = Stars(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            price=validated_data['price'],
            cat_name_id=validated_data['cat_name_id'],
            rating=validated_data['rating'],
            is_star=validated_data['is_star']
        )
        star.set_password(validated_data['password'])
        star.save()
        return star

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки Рейтингов
    """

    class Meta:
        model = Ratings
        fields = ('rating', 'adresat', 'adresant')


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализер для обработки Заказов
    переопределен метод update для обновление статуса заказа
    """

    class Meta:
        model = Orders
        fields = ('customer_id', 'star_id', 'order_price', 'ordering_time', 'for_whom', 'comment', 'status_order')

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
