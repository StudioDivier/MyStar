from math import ceil
import uuid

from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Customers, Stars, Ratings, Orders, Users, Categories
from .serializers import LoginSerializer, UserSerializer, RegistrationSerializer, CategorySerializer
from .serializers import CustomerSerializer, StarSerializer, RatingSerializer, OrderSerializer


class CustomerCreate(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )
    # """
    # Вьюшка для создания пользователя(заказчика) с токеном
    # """
    # def post(self, request, format='json'):
    #     """
    #     Принимаем request Вида:
    #     {
    #         "username": "ValyMalya",
    #         "phone": 9942638783,
    #         "email": "ValyMalya@rambler.com",
    #         "password": "ValyMalya666",
    #         "date_of_birth": "1968-08-05"
    #     }, где
    #         :param username: - ник пользователя
    #         :param phone: - номер телефона
    #         :param email: - электронная почта пользователя
    #         :param password: - пароль (в бд храним хэш)
    #         :param date_of_birth: - дата рождения пользователя
    #     1. Создаем запись в бд из данных request через сериализер
    #     2. Добавляем токен ьпользователю
    #     :return: Response 201, если запись создана. Response 400, если данные не валидные
    #     """
    #     serializer = CustomerSerializer(data=request.data)
    #     if serializer.is_valid():
    #         customer = serializer.save()
    #         if customer:
    #             token = Token.objects.create(user=customer)
    #             json = serializer.data
    #             json['token'] = token.key
    #             return Response(json, status=status.HTTP_201_CREATED)
    #         # return Response(serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cust_set = Customers.objects.get(email=request.data['email'])
            json = {
                'username': cust_set.username,
                'phone': cust_set.phone,
                'is_star': cust_set.is_star,
                'email': cust_set.email,
                'avatar': cust_set.avatar,
                'token': cust_set.token
            }
            return Response(json, status=status.HTTP_200_OK)


class StarCreate(APIView):
    """
    Вьюшка для создания звезды с токеном
    """
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        """
        Принимаем request Вида:
        {
            "username": "niletto",
            "phone": 9787892356,
            "email": "niletto@star.com",
            "password": 1598753426,
            "price": "15000.00",
            "rating": 0,
            "cat_name_id": "1",
            "is_star": 1
        }, где
            :param username: - ник звезды
            :param phone: - номер телефона
            :param email: - электронная почта пользователя
            :param password: - пароль (в бд храним хэш)
            :param price: - дата рождения пользователя
            :param rating: - рейтинг звезды ( по умолчанию 0)
            :param cat_name_id: - id категории
            :param is_star: - флаг звезды (1)
        1. Создаем запись в бд из данных request через сериализер
        2. Добавляем токен ьпользователю
        :return: Response 201, если запись создана. Response 400, если данные не валидные
        """
        serializer = StarSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            if customer:
                token = Token.objects.create(user=customer)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StarById(APIView):
    """
    Вьюшка для получения звезды по айди
    """
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        stars_set = Stars.objects.get(users_ptr_id=request.data['star_id'])
        serializer_class = StarSerializer(stars_set)
        json = serializer_class.data
        return Response(json, status=status.HTTP_200_OK)


class StarsList(APIView):
    """
    Получаем список всех звезд
    """
    permission_classes = [AllowAny]

    def get(self, request, format='json'):
        stars_list = Stars.objects.all()
        serializer = StarSerializer(stars_list, many=True)
        json = serializer.data
        return Response(json, status=status.HTTP_200_OK)


class StarByCategory(APIView):
    """
    Вьюшка для получения спсика звезд по айди категории
    """
    permission_classes = [AllowAny]
    def get(self, request, format='json'):
        """
        Получаем request вида:
        {
            "cat_name_id": "1"
        }, где
            :param cat_name_id: - id категории
        1. Получаем QuerySet из таблицы звезд по id категории
        2. Переводим в дату и отдаем с 200 response
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
    permission_classes = [AllowAny]
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

                starset = Stars.objects.get(users_ptr_id=request.data['adresant'])
                starset.rating = str(uprate)
                starset.save()
                # serialstar = StarSerializer(data=starset, partial=True)
                # if serialstar.is_valid():
                return Response(status=status.HTTP_201_CREATED)

                # return Response(serializer.errors, status=status.HTTP_418_IM_A_TEAPOT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    """
    Вьюшка для регистрации заказа и отправки уведомления на почту звезды
    """
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        """
        Получаем request вида:
        {
            "customer_id": "1",
            "star_id": "5",
            "order_price": "15000.00",
            "for_whom": "Для Мамы",
            "comment": "Хочу поздравить маму с днем рождения",
            "status_order": "New"
        }, где
            :param customer_id: - id заказчика
            :param star_id: - id звезды
            :param order_price: - цена заказа
            :param for_whom: - Для кого заказ
            :param comment: - комментарий к заказу
            :param status_order: - стасус заказа (0 - New, 1 - Accepted, 2 - Completed)
        1. Создаем запись в бд заказа
        2. Если данные валидные, то забираем QuerySet по id звезды.
        3. Сериализуем данные и выцыпляем данные: 'email', 'username', 'price'
        4. Отправляем письмо на почту звезде с уведомлением о заказе
        :return: Response 201, если все хорошо. Response 400, если данные не валидные
        """
        # payment_id = str(uuid.uuid4())
        # json = request.data
        # json['payment_id'] = payment_id
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            if order:
                star_queryset = Stars.objects.filter(users_ptr_id=request.data['star_id'])
                star_serializer = StarSerializer(star_queryset, many=True)

                star = star_serializer.data
                star_email = star[0]['email']
                star_username = star[0]['username']
                star_price = star[0]['price']
                SUBJECT = 'MySTAR: Уведомление!'
                TEXT_MESASGE = 'Уважаемый {}, вам пришел заказ поздравления на сумму {}'.format(
                    star_username, star_price
                )
                send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [star_email])
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_418_IM_A_TEAPOT)


class StarOrderAccepted(APIView):
    """
    Вьюшка принятия или отклонения заяки на заказ со стороны звезды
    """
    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        """
        {
            'order_id'
            'accept' accept/reject
        }
        :param request:
        :param format:
        :return:
        """
        order_set = Orders.objects.get(id=request.data['order_id'])
        customer = Customers.objects.get(users_ptr_id=order_set.customer_id)
        customer_email = customer.email
        customer_username = customer.username
        if request.data['accept'] == 'accept':
            order_set.payment_id = str(uuid.uuid4())
            order_set.status_order = 1
            order_set.save()
            SUBJECT = 'MySTAR: Уведомление!'
            TEXT_MESASGE = 'Уважаемый {}, ваш заказ был принят. ' \
                           'Приходите в MySTAR, чтобы оплатить его.'.format(
                customer_username
            )
        elif request.data['accept'] == 'reject':
            order_set.payment_id = ''
            order_set.status_order = -1
            order_set.save()
            SUBJECT = 'MySTAR: Уведомление!'
            TEXT_MESASGE = 'Уважаемый {}, ваш заказ был отклонён.' \
                           'Приходите заказывать еще поздравления в MySTAR'.format(
                customer_username
            )
        else:
            return Response({'Order status is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        send_mail(SUBJECT, TEXT_MESASGE, settings.EMAIL_HOST_USER, [customer_email])
        return Response(status=status.HTTP_201_CREATED)


class ListCategory(APIView):

    permission_classes = [AllowAny]

    def get(self, request, format='json'):

        cat_set = Categories.objects.all()
        cat_serial = CategorySerializer(cat_set, many=True)
        json = cat_serial.data
        return Response(json, status=status.HTTP_200_OK)


class PersonalAccount(APIView):
    """
    Вьюшка личного кабинета
    """
    permission_classes = [AllowAny]
    def get(self, request, format='json'):
        """
        Получаем request вида:
        {
            "user_id": "1",
            "is_star": 0
        }, где
            :param user_id: - id пользователя
            :param is_star: - статус звезды (0,1)

        :return:
        """
        if request.data['is_star'] == False:
            cust_sest = Customers.objects.filter(users_ptr_id=request.data['user_id'])
            serial_cust = CustomerSerializer(cust_sest, many=True)
            json = serial_cust.data

            order_set = Orders.objects.filter(customer_id=request.data['user_id'])
            serial_orders = OrderSerializer(order_set, many=True)

            orders = {
                'orders': serial_orders.data
            }

            json.append(orders)

        elif request.data['is_star'] == True:
            star_set = Stars.objects.filter(users_ptr_id=request.data['user_id'])
            star_cust = StarSerializer(star_set, many=True)
            json = star_cust.data

            order_set = Orders.objects.filter(star_id_id=request.data['user_id'])
            serial_orders = OrderSerializer(order_set, many=True)

            orders = {
                'orders': serial_orders.data
            }

            json.append(orders)
        else:
            return Response("No data invalid", status=status.HTTP_400_BAD_REQUEST)
        return Response(json, status=status.HTTP_200_OK)


class TestView(APIView):
    """
    Временная тестовая вьюшка
    """
    permission_classes = [AllowAny]
    def get(self, request, format='json'):
        """
        Вьюшка для проверки гипотиз и доказательства теорем
        """
        payment_id = request.data['payment_id']
        value = request.data['value']
        return Response(data = str(value))




