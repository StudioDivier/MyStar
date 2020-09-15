from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Customers


class CustomerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=Customers.objects.all())]
                                     )
    phone = serializers.IntegerField(
        validators=[UniqueValidator(queryset=Customers.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Customers.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    date_of_birth = serializers.DateField(
        validators=[UniqueValidator(queryset=Customers.objects.all())]
    )

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

    class Meta:
        model = Customers
        fields = ('id', 'username', 'phone', 'email', 'password', 'date_of_birth')
