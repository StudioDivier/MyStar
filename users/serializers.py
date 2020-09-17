from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Customers, Stars, Users, Ratings


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
        fields = ('username', 'phone', 'email', 'password')


class CustomerSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = Stars
        fields = ('username', 'phone', 'email', 'password', 'price', 'cat_name_id', 'rating_id')

    def create(self, validated_data):
        star = Stars(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            price=validated_data['price'],
            cat_name_id=validated_data['cat_name_id'],
            rating_id=validated_data['rating_id']
        )
        star.set_password(validated_data['password'])
        star.save()
        return star


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ratings
        fields = ('rating', 'adresat', 'adresant')
