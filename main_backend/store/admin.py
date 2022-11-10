from django.contrib import admin
from store.models import Product, Album, Review, Category

admin.site.register(Category)
admin.site.register(Album)
admin.site.register(Review)
admin.site.register(Product)
