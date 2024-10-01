from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ais.models.teachers import Teachers


class Students(models.Model):
    nim = models.CharField(max_length=10, unique=True)

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    year = models.IntegerField()  # Tahun angkatan atau tahun masuk
    # Relasi ke tabel Teachers
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
