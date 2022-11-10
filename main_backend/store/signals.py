from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from store.models import Album


@receiver(pre_delete, sender=Album)
def album_delete(sender, instance, **kwargs):
    """
    Delete the actual file when the image is deleted
    """
    storage, path = instance.image.storage, instance.image.path
    storage.delete(path)

