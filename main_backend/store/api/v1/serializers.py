from rest_framework import serializers
from store.models import Category, Album, Review, Product
from django.contrib.auth import get_user_model

User = get_user_model()

created_by_field = {'created_by': {'default': serializers.CurrentUserDefault()}}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        readonly = ["modified_at", "created_at", 'created_by']
        extra_kwargs = created_by_field


class ImagesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Album
        fields = ["id", "image", "created_by"]
        extra_kwargs = created_by_field


class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Album
        fields = "__all__"
        extra_kwargs = created_by_field


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    created_by = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name="api_user_detail",
        lookup_field="username",
        required=False
    )

    class Meta:
        model = Review
        fields = '__all__'
        readonly = ["modified_at", "created_at"]
        extra_kwargs = created_by_field


class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        view_name="api_user_detail",
        lookup_field="username",
        required=False
    )

    class Meta:
        model = Product
        fields = '__all__'
        readonly = ["modified_at", "created_at", 'created_by']
        extra_kwargs = created_by_field

    def create(self, validated_data):
        validated_data['created_by'] = self.context["request"].user
        return super(ProductSerializer, self).create(validated_data=validated_data)


class ProductDetailSerializer(ProductSerializer):
    reviews = ReviewSerializer(many=True, required=False)
    images = ImagesSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)
        reviews = validated_data.pop("reviews", None)
        instance = super(ProductDetailSerializer, self).update(instance, validated_data)
        if reviews:
            for review_data in reviews:
                if review_data.get("id"):
                    # review has an ID so was pre-existing
                    continue
                review = Review(**review_data)
                review.created_by = self.context["request"].user
                review.content_object = instance
                review.save()
        if images:
            for image_data in images:
                if image_data.get("id"):
                    # image has an ID so was pre-existing
                    continue

                image64 = image_data.get('image')
                image = Album(**image_data)
                image.content_object = instance
                image.created_by = self.context["request"].user
                image.image = image64
                image.save()
                try:
                    image.content_object.get_thumbnail
                except Exception as e:
                    raise e
        return instance
