from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.signing import Signer

from datetime import datetime

# Create your models here.

class PublicKey(models.Model):
    """
    Stores, all public keys and
    assigns as id a pregenerated
    hash.
    """
    id = models.CharField(
        max_length=256,
        primary_key=True,
        blank=True
    )
    key = models.TextField()


@receiver(pre_save, sender=PublicKey)
def create_pk(sender, **kwargs):
    """A signal to generate primary key
    usign signer object from django
    core."""

    signer = Signer()

    # Extracting key instance that will be saved
    key_obj = kwargs.get('instance') 
    signed_id = signer.sign('%s%s' % 
            (key_obj.key[:len(key_obj.key)/2],
            datetime.now().microsecond))
    
    # Splits to obtain only signed hash to be defined
    # as primary key
    key_obj.id = signed_id.split(':')[1]
