from django.dispatch import receiver
from django.db.models.signals import post_save

from funds.models import Fund
from .models import User


@receiver(post_save, sender=User)
def create_provider_fund(sender, instance: User, created: bool, *args, **kwargs):
    """Create a new fund for new provider users"""

    is_provider = instance.user_type == "PROVIDER"
    if created and is_provider:
        Fund.objects.create(user=instance)
