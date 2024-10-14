from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('crud', HotelViewSet)

app_name = 'hotel'

urlpatterns = [
    path('', include(router.urls)),
]