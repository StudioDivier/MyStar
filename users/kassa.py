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

    def get(self, request):
        """
        Принимаем payment_id
        :param request:
        :param format:
        :return:
        """
        idempotence_key = request.GET.get("payment_id", "")
        value = request.GET.get("value", "")
        order = Orders.objects.get(payment_id=idempotence_key)
        status = int(order.status_order)
        if status == 1:
            payment = Payment.create({
                "amount": {
                    "value": value,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "http://192.168.1.131:8080/"
                },
                "capture": False,
                "description": "Заказ №1",
                "metadata": {
                    "order_id": "37"
                }
            }, idempotence_key)

            # get confirmation url
            confirmation_url = payment.confirmation.confirmation_url
            order.status_order = 2
            order.save()
            return HttpResponseRedirect(confirmation_url)

        else:
            return Response(status=400)




class YandexNotification(APIView):
    """
    Обработка платежа
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Подтверждение платежа и смена статуса заказа
        :param request:
        :return:
        """
        payment_id = request.GET.get("payment_id", "")
        # payment_id = '26fd1b35-000f-5000-a000-14c3cdc3d6c1'
        Payment.capture(payment_id)

        order = Orders.objects.get(payment_id=payment_id)
        order.status_order = 3
        order.save()

        return Response(status=200)
