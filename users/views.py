from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Customers, Stars
from .serializers import CustomerSerializer, StarSerializer



class CustomerCreate(APIView):
    """
    Create the customer
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


class StarsViewSet(viewsets.ModelViewSet):
    queryset = Stars.objects.all()
    serializer_class = StarSerializer


class StarsList(APIView):

    def get(self, request, format='json'):
        stars_list = Stars.objects.all()
        serializer = StarSerializer(stars_list, many=True)
        json = serializer.data
        return Response(json, status=status.HTTP_200_OK)









