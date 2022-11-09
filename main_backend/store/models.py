"""
A Model for Store app
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from versatileimagefield.fields import VersatileImageField, PPOIField

# Getting the user model, Change if the main model changed
User = get_user_model()


class Category(models.Model):
    """
    Category Model -> Store the category for the products
    Fields:
        name -> The category name
        slug -> the slug for the category # that is used in URL
        created_at -> the date the category was created
        modified_at -> Last modified date
        created_bt -> a reference for User model for user created it
    Properties:
        get_absolute_url -> the sub url for the category
    """
    name = models.CharField(max_length=255, db_index=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='category_created', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        """
        return the sub url for the category
        """
        return self.slug


def image_rename(instance, filename):
    """
    Rename the image when store in media root
    """
    return f'user_{instance.content_object.created_by.id}/{filename}'


class Album(models.Model):
    """
    Album Model -> Store the images of the products, each image is stored alone then gathered by Product Model
    Fields:
        image -> The image that the user upload for the product
        ppoi -> The PPOI for the image
        content_type ->

    """

    image = VersatileImageField(upload_to=image_rename, ppoi_field="ppoi")
    ppoi = PPOIField(null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    @property
    def get_absolute_url(self):
        """
        return the sub url for the image
        """
        return self.image.url


class Review(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rate = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, related_name='product_creator', on_delete=models.CASCADE)

    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    thumbnail = models.ImageField(upload_to='thumbnail/', blank=True, null=True)

    images = GenericRelation(Album)
    reviews = GenericRelation(Review)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return self.slug

    def generate_thumbnail(self):
        if self.images:
            self.thumbnail = self.images.all()[0].image

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
