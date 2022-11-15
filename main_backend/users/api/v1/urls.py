from django.urls import path, include
from users.api.v1 import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path("users/<str:username>", views.UserDetail.as_view(), name="api_user_detail")
]