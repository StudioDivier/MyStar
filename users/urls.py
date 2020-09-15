from django.urls import include, path

from .views import CustomerCreate


urlpatterns = [
    path('create', CustomerCreate.as_view(), name="account-create"),
]