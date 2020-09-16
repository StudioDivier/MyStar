from django.urls import include, path

from .views import CustomerCreate, CustomersList


urlpatterns = [
    path('create', CustomerCreate.as_view(), name='customer-create'),
    path('customer/getlist/', CustomersList.as_view()),
]
