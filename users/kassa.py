from rest_framework.response import Response
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
import uuid

from yandex_checkout import Configuration, Payment

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from MyStar.config import ID_KASSA, SK_KASSA
from users.serializers import OrderSerializer
from users.models import Orders


Configuration.account_id = ID_KASSA
Configuration.secret_key = SK_KASSA


class YandexPayment(APIView):
    """
    Создание платежа
    """
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        """
        Принимаем payment_id
        :param request:
        :param format:
        :return:
        """
        payment_id = request.data['payment_id']
        value = request.data['value']
        # payment_id = request.GET.get('payment_id')
        # value = request.GET.get('value')
        # order_set = Orders.objects.get(payment_id=payment_id)
        # order_serial = OrderSerializer(order_set)
        # json = order_serial.data
        # value = order_set.order_price

        payment = Payment.create({
            "id": payment_id,
            "amount": {
                "value": value,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": 'bank_cart'
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://192.168.1.131:8080"
            },
            "capture": 'false',
            "description": "Заказ №1"
        })
        """
        Добавить информацию value в таблицу Order
        """

        return HttpResponseRedirect(payment.confirmation.confirmation_url)


class YandexNotification(APIView):
    """
    Обработка платежа
    """

    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        """
        Подтверждение платежа и смена статуса заказа
        :param request:
        :return:
        """
        payment_id = request.data['payment_id']
        Payment.capture(payment_id)

        order = Orders.objects.get(payment_id=payment_id)
        order.status_order = 2
        order.save()

        return Response(status=200)
