"""
URLs route for API v1
"""
from django.urls import path, include
from store.api.v1 import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("albums", views.AlbumViewSet)
router.register("categories", views.CategoryViewSet)
router.register("reviews", views.ReviewViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
