from rest_framework import serializers
from store.models import Category, Album, Review, Product
from django.contrib.auth import get_user_model

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        readonly = ["modified_at", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ImagesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Album
        fields = ["id", "image", "created_by"]


class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Album
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_by = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name="api_user_detail",
        lookup_field="username",

    )

    class Meta:
        model = Review
        fields = '__all__'
        readonly = ["modified_at", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name="api_user_detail",
        lookup_field="username"
    )
    thumbnail = Product.get_thumbnail

    class Meta:
        model = Product
        fields = '__all__'
        readonly = ["modified_at", "created_at"]


class ProductDetailSerializer(ProductSerializer):
    reviews = ReviewSerializer(many=True)
    images = ImagesSerializer(many=True)

    def update(self, instance, validated_data):
        images = validated_data.pop('images')
        reviews = validated_data.pop("reviews")
        instance = super(ProductDetailSerializer, self).update(instance, validated_data)

        for review_data in reviews:
            if review_data.get("id"):
                # review has an ID so was pre-existing
                continue
            review = Review(**review_data)
            review.created_by = self.context["request"].user
            review.content_object = instance
            review.save()

        for image_data in images:
            if image_data.get("id"):
                # image has an ID so was pre-existing
                continue

            image64 = image_data.get('image')
            image = Album(**image_data)
            image.content_object = instance
            image.created_by = image.content_object.created_by
            image.image = image64
            image.save()
            try:
                image.content_object.get_thumbnail
            except Exception as e:
                raise e
        return instance
