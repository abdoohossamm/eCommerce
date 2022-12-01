from django.contrib import admin
from store.models import Product, Album, Review, Category

admin.site.register(Category)


class AlbumAdmin(admin.ModelAdmin):
    list_display_links = ("id",)
    list_display = (
        "id",
        "image",
        "created_by",
        "content_type",
        "object_id",
        "content_object",
    )


admin.site.register(Album, AlbumAdmin)
admin.site.register(Review)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display_links = ("id", "title",)
    list_display = (
        "id",
        "title",
        "created_by",
        "thumbnail"
    )


admin.site.register(Product, ProductAdmin)
