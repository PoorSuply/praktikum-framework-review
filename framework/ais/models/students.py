from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from ais.models.teachers import Teachers

class Students(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    year = models.IntegerField()
    teacher = models.ForeignKey(Teachers,
    on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

@receiver(post_save, sender=Students)
def create_user_for_student(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(
            username=instance.nim,
            email=instance.email,
            password=instance.nim,
            )

        student_group,created =Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)