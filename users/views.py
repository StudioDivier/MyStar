from rest_framework import status, viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Customers, Stars, Ratings
from .serializers import CustomerSerializer, StarSerializer, RatingSerializer


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


# class RateStar(ListAPIView):
#     """
#     Вьюшка для выставления рейтинга
#     Этап:
#         забираем все записи по айдишнику звезды
#     Нужно:
#         суммировать все рейтинги по записям и вставлять данные в звезду
#     """
#
#     queryset = Ratings.objects.all()
#     serializer_class = RatingSerializer
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('adresant',)


class StarByCategory(ListAPIView):
    """
    Вьюшка для получения спсика звезд по айди категории
    """
    serializer_class = StarSerializer
    queryset = Stars.objects.all()
    filter_fields = ('cat_name_id',)
    lookup_field = 'cat_name_id'

    # def get_queryset(self):
    #     stars = self.kwargs['cat_name_id']
    #     return Stars.objects.filter(cat_name_id_id=stars)


class RateStar(APIView):
    """
    Вьюшка для обновления рейтинга звезды
    """
    def get(self, request):
        res: int() = 0
        serializtor = StarSerializer
        queryset = Ratings.objects.filter(adresant=request.data['adresant'])

















