from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class AddEvent(models.Model):
    author = models.ForeignKey('auth.User')
    data_intratii = models.DateField()
    data_ultimei_modificari = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=100)
    vizibilitate = models.BooleanField()
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title
