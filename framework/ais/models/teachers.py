from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Teachers(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=Teachers)
def create_user_for_teacher(sender, instance, created,**kwargs):
    if created:
        user = User.objects.create_user(
            username=instance.nip,
            email=instance.email,
            password=instance.nip,
        )

        teacher_group, created =Group.objects.get_or_create(name='Teacher')
        user.groups.add(teacher_group)