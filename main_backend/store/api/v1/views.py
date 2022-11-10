from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from store.api.v1.permissions import CreatorModifyOrReadOnly, IsAdminUserForObject
from store.api.v1.serializers import ProductSerializer, ProductDetailSerializer, UserSerializer, AlbumSerializer, \
    ReviewSerializer, CategorySerializer
from store.models import Product, Album, Category, Review

User = get_user_model()


@method_decorator(cache_page(300))
@method_decorator(vary_on_headers("Authorization"))
@method_decorator(vary_on_cookie)
@action(methods=["get"], detail=False, name="data owned by logged in user")
def mine(self, request):
    if request.user.is_anonymous:
        raise PermissionDenied("You must be logged in to see which Images are yours")
    data = self.get_queryset().filter(created_by=request.user)

    page = self.paginate_queryset(data)
    if page is not None:
        serializer = self.get_serializer_class()(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)
    serializer = self.get_serializer_class()(data, many=True, context={"request": request})
    return Response(serializer.data)


viewsets.ModelViewSet.mine = mine


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "username"
    queryset = User.objects.all()
    permission_classes = [CreatorModifyOrReadOnly | IsAdminUserForObject]
    serializer_class = UserSerializer

    @method_decorator(cache_page(300))
    def get(self, *args, **kwargs):
        return super(UserDetail, self).get(*args, *kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Product.objects.all()
    permission_classes = [CreatorModifyOrReadOnly | IsAdminUserForObject]

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return ProductSerializer
        return ProductDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = Category.objects.all()
    permission_classes = [CreatorModifyOrReadOnly | IsAdminUserForObject]
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [CreatorModifyOrReadOnly | IsAdminUserForObject]
    serializer_class = ReviewSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    permission_classes = [CreatorModifyOrReadOnly | IsAdminUserForObject]
    serializer_class = AlbumSerializer

