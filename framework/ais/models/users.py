from django.db import models

class Users(models.Model):
    STUDENT = 1
    TEACHER = 2
    
    ROLE_CHOICES = (
    (STUDENT, 'Student'),
    (TEACHER, 'Teacher'),
)

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    role = models.IntegerField(choices=ROLE_CHOICES) 

def __str__(self):
    return self.username