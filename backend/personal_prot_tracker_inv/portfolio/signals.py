from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Portfolio

# The @receiver decorator connects this function to the post_save signal
# for the User model.
@receiver(post_save, sender=User)
def create_user_portfolio(sender, instance, created, **kwargs):
    """
    Automatically creates a Portfolio for a new user.
    """
    # The 'created' boolean is True only the first time the object is saved.
    if created:
        Portfolio.objects.create(user=instance)