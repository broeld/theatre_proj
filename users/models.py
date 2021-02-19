from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=150, unique=True)

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email)
    instance.customer.save()
