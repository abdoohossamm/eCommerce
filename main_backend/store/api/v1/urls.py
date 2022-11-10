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
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path("", include(router.urls)),
    path("users/<str:username>", views.UserDetail.as_view(), name="api_user_detail")

]

# urlpatterns += [
#     path("products/", views.product_list, name="api_product_list"),
#     path("products/<int:pk>/", views.product_detail, name="api_product_detail"),
# ]
