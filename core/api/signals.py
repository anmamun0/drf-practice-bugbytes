from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import User
from django.core.cache import cache


@receiver([post_save, post_delete], sender=User)
def invalidate_user_cache(sender, instance, **kwargs):
    """
    Invalidate user list caches when a user is created, updated, or deleted
    """
    print("Clearing user cache")
    
    # Clear user list caches
    cache.delete_pattern('*user_list*')