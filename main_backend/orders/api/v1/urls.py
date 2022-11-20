from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.api.v1 import views
router = DefaultRouter()
router.register("orders", views.OrderViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
