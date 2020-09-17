from django.urls import include, path, re_path
from rest_framework import routers
from .views import CustomerCreate, StarsList, StarsViewSet

router = routers.DefaultRouter()
router.register(r'stars', StarsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('create/', CustomerCreate.as_view(), name=None),
    path('star/getlist/', StarsList.as_view(), name=None),

]
