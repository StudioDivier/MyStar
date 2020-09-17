from django.urls import include, path, re_path
from rest_framework import routers
from .views import (
CustomerCreate, StarCreate, StarsList, StarsViewSet, RateStar, StarByCategory)

router = routers.DefaultRouter()
router.register(r'stars', StarsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('customer/create/', CustomerCreate.as_view(), name=None),
    path('star/create/', StarCreate.as_view(), name=None),
    path('star/getlist/', StarsList.as_view(), name=None),
    path('ratestar', RateStar.as_view(), name=None),
    re_path('starlist/category', StarByCategory.as_view(), name=None)

]
