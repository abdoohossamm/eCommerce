from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404
from store.models import Album, Product


@receiver(pre_delete, sender=Album)
def album_delete(sender, instance, **kwargs):
    """
    Delete the actual file when the image is deleted
    """
    storage, path = instance.image.storage, instance.image.path
    storage.delete(path)


@receiver(post_save, sender=Album)
def image_save(sender, instance, **kwargs):
    """
    generate thumbnail after the image is being added
    """
    product = get_object_or_404(Product, pk=instance.object_id)
    if product.thumbnail:
        return
    else:
        product.get_thumbnail
