"""
URLs route for API v1
"""
from django.urls import path, include
from store.api.v1 import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),

]
