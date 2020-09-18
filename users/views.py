from rest_framework import status, viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Customers, Stars, Ratings, Users
from .serializers import CustomerSerializer, StarSerializer, RatingSerializer, UserSerializer

from math import ceil


class CustomerCreate(APIView):
    """
    Вьюшка для создания пользователя(заказчика) с токеном
    """
    def post(self, request, format='json'):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            if customer:
                token = Token.objects.create(user=customer)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StarCreate(APIView):
    """
    Вьюшка для создания звезды с токеном
    """
    def post(self, request, format='json'):
        serializer = StarSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            if customer:
                token = Token.objects.create(user=customer)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StarsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для routers
    Основная вьюшка для рутинга
        - получить всех звезд
        - получить звезду по айди
        - PUT
        - DELETE
    """
    queryset = Stars.objects.all()
    serializer_class = StarSerializer


class StarsList(APIView):
    """
    Получаем список звезд
        (отличается выводом данных)
    """
    def get(self, request, format='json'):
        stars_list = Stars.objects.all()
        serializer = StarSerializer(stars_list, many=True)
        json = serializer.data
        return Response(json, status=status.HTTP_200_OK)


class StarByCategory(APIView):
    """
    Вьюшка для получения спсика звезд по айди категории
    """
    def get(self, request, format='json'):
        """
        Получаем request вида:

        :param request:
        :param format:
        :return:
        """
        strarsest = Stars.objects.filter(cat_name_id=request.data['cat_name_id'])
        serialstar = StarSerializer(strarsest, many=True)

        stardata = serialstar.data
        return Response(stardata, status=status.HTTP_200_OK)


class RateStar(APIView):
    """
    Вьюшка для обновления рейтинга звезды 
    """
    def put(self, request, format='json'):
        """
        Получаем Request вида:
        {
            "rating": "5",
            "adresat": 1,
            "adresant": 3
        }, где
            :param rating: int - сама оценка
            :param adresat: int - id заказчика, который поставил оценку
            :param adresant: int - id звезды, которой поставили оценку
        1. Получаем QuerySet из таблицы Рейтинга по айди звезды
           Суммируем все оценки и получаем среднее с округлением в большую сторону
        2. Получаем QuerySet из таблицы Звезд по айди звезды
           Записываем новый рейтинг
        3. Response в зависимости от исхода
        :return: 201 - успещная запись
                 418 - не валидные данные
                 404 - не валидные id
        """
        res: int() = 0
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            rating = serializer.save()
            if rating:
                # json = serializer.data
                queryset = Ratings.objects.filter(adresant=request.data['adresant'])
                serializtor = RatingSerializer(queryset, many=True)
                json = serializtor.data

                for i in range(len(json)):
                    res += json[i]['rating']
                uprate = ceil(res / len(json))

                strarsest = Stars.objects.filter(users_ptr_id=request.data['adresant'])
                serialstar = StarSerializer(data={'rating': uprate}, partial=True)
                if serialstar.is_valid():
                    return Response(status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestView(APIView):
    """
    Временная тестовая вьюшка
    """

    def put(self, request, format='json'):
        strarsest = Stars.objects.filter(cat_name_id=request.data['adresant'])
        serialstar = StarSerializer(data={'rating': 3}, partial=True)


        return Response(status=status.HTTP_200_OK)
