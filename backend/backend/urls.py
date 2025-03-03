from django.urls import path, include
from rest_framework.routers import DefaultRouter
from collection.views import LegoSetViewSet, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'legosets', LegoSetViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', obtain_auth_token),
]
