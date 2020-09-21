from django.urls import include, path, re_path
from rest_framework import routers
from .views import (
CustomerCreate, StarCreate, StarsList, StarsViewSet, RateStar, StarByCategory, TestView, OrderView, PersonalAccount)

from MyStar import settings
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'stars', StarsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('customer/create/', CustomerCreate.as_view(), name=None),
    path('star/create/', StarCreate.as_view(), name=None),
    path('star/getlist/', StarsList.as_view(), name=None),
    path('ratestar', RateStar.as_view(), name=None),
    path('starlist/category', StarByCategory.as_view(), name=None),
    path('order/', OrderView.as_view(), name=None),
    path('personal', PersonalAccount.as_view(), name=None),

    path('test', TestView.as_view(), name=None)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
