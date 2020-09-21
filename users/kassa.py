from rest_framework.response import Response
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
import uuid

from yandex_checkout import Configuration, Payment
from django.utils import timezone, dateformat

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from MyStar.config import ID_KASSA, SK_KASSA

Configuration.account_id = ID_KASSA
Configuration.secret_key = SK_KASSA


class YandexPayment(View):
    """Создание платежа"""

    def get(self, request, format='json'):

        value = self.request.GET.get('value')
        paytype = self.request.GET.get('paytype')

        payment = Payment.create({
            "amount": {
                "value": str(value),
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": paytype
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/"
            },
            "capture": False,
            "description": "Заказ №1",
        }, uuid.uuid4())
        """
        Добавить информацию value и paytype  в таблицу Order
        """

        return HttpResponseRedirect(payment.confirmation.confirmation_url)


class YandexNotification(APIView):
    """Обработка платежа"""

    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        """
        Подтверждение платежа и смена статуса заказа
        :param request:
        :return:
        """
        # payment_id = request.data['']
        Payment.capture(payment_id)

        return Response(status=200)